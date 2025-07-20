import json
import asyncio
import aiohttp
from copy import deepcopy
from bson import ObjectId
from utils import config
from utils.config import logger
import utils.aws_services as aws
from utils.mongodb import MongoDB
from model.model import OpenAI_Extract
from azure.eventhub.exceptions import EventHubError
from azure.eventhub.aio import EventHubConsumerClient
from tenacity import AsyncRetrying, stop_after_attempt, wait_random_exponential
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

async def get_consumer_client():
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        conn_str = config.storage_ac_conn_str,
        container_name = config.eventhub_checkpoint_container,
    )
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str = config.eventhub_conn_str_listen, 
        consumer_group = "$Default", 
        eventhub_name = config.eventhub_name,
        checkpoint_store = checkpoint_store,
    )
    return consumer_client

async def async_range(start, stop):
    """
    Function to run 'for loop' in async
    """
    for i in range(start, stop):
        yield(i)
        await asyncio.sleep(0)

async def on_event(partition_context, event, mongo):
    """
    Method to handle events
    
    partition_context: contains partition context 
    event: the received event
    """
    
    logger.info(f"{event=}")
    event_body = event.body_as_json(encoding='UTF-8')
    logger.info(f"Processing event...")
    # logger.info(f"doc_id: {event_body['doc_id']}")
    # logger.info(f"file_name: {event_body['file_name']}")
    logger.info(f"{event_body=}")
    
    # payload = deepcopy(event_body)

    flag_status = False

    async with aiohttp.ClientSession() as session:
        try:
            async for attempt in AsyncRetrying(
                wait=wait_random_exponential(multiplier=config.retry_exp_wait_multiplier,
                                            max=config.retry_wait_max),
                stop=stop_after_attempt(config.max_api_tries),
                reraise=True):
                #file_name = event_body['file_name']
                file_name = event_body['file_name'].split(".com/")[1]
                
                with attempt:
                    # Get object of file in S3 bucket
                    file_obj = await aws.get_file_object_s3(
                        s3_client=config.boto3_client,
                        bucket=config.s3_bucket_input,
                        object_name=file_name
                    )

                    # Case: File not found in bucket
                    if file_obj is None:
                        logger.info(f"{file_obj=}")

                        # Update MongoDB
                        response_mdb = mongo.update_document(
                        collection_name=config.mdb_collection_data,
                        query={
                            "_id": ObjectId(event_body['_id']),
                            "doc_id":event_body['doc_id']
                            },
                        new_values={
                            "doc_status": "error",
                            "msg": "File Not Found"
                            })
                        
                        flag_status = True if response_mdb.acknowledged else False
                        if flag_status:
                            await partition_context.update_checkpoint(event)

                    else: 

                        # Call OpenAI API
                        openai = OpenAI_Extract(session)
                        response_llm = await openai.get_llm_output(file_name, file_obj)
                        logger.info(f"op:\n{json.dumps(response_llm, indent=2, ensure_ascii=False)}")
                        if not response_llm :
                            doc_status = "failed"
                        else:
                            doc_status = "completed"
                        # dict_op = {
                        #     "doc_id": event_body['doc_id'],
                        #     "file_name": event_body['file_name'],
                        #     "doc_status": "completed",
                        #     "extracted_details": response
                        # }
            async for attempt in AsyncRetrying(
                wait=wait_random_exponential(multiplier=config.retry_exp_wait_multiplier,max=config.retry_wait_max),
                stop=stop_after_attempt(config.max_api_tries),
                reraise=True
            ):
                with attempt:                
                    # Appian-API Call
                
                    payload = {
                        "uid": event_body['uid'],
                        "doc_id": event_body['doc_id'],
                        "file_name": event_body['filename'],
                        "doc_status": doc_status,
                        "extracted_details": response_llm
                    }                        
                    headers = {
                        "Content-Type": "application/json",
                        "API-Key": config.appian_api_key
                    }

                    try:
                        response_appian = await session.post(
                            config.appian_api_url, 
                            headers=headers, 
                            # data=json.dumps(dict_data)
                            json=payload
                        )
                        
                        # Check if the request was successful
                        #response_appian.raise_for_status()
                        
                        # Print the response
                        logger.info(f"Response status code: {response_appian.status_code}")
                        logger.info(f"Response content: {await response_appian.json()}")

                    except aiohttp.ClientError as e:
                        logger.error(f"Exception while sending data to AppianAPI: {e}")
                        
                        
                        # Update MongoDB
                        response_mdb = mongo.update_document(
                            collection_name=config.mdb_collection_data,
                            query={
                                "_id":ObjectId(event_body['doc_id']) 
                            },
                            new_values={
                                "doc_status": doc_status,
                                "extracted_details": response_llm,
                                "status_output_response": response_appian.status_code,
                                "msg_output_response" : response_appian.text
                            }
                        )

                        flag_status = True if response_mdb.acknowledged else False
                        if flag_status:
                            await partition_context.update_checkpoint(event)

        except Exception as exp:
            logger.error(f"Exception while processing event: {exp}")
            # Update MongoDB
            response_mdb = mongo.update_document(
            collection_name=config.mdb_collection_data,
            query={
                "_id": ObjectId(event_body['_id']),
                "doc_id":event_body['doc_id']
                },
            new_values={
                "doc_status": "error",
                "msg": str(exp)
                })
            
            flag_status = True if response_mdb.acknowledged else False
            if flag_status:
                await partition_context.update_checkpoint(event)

    return flag_status
    
async def on_event_batch(partition_context, event_batch):
    """
    Method to handle events in event_batch

    partition_context: contains partition context 
    event_batch<List>: event_batch could be an empty list if max_wait_time is not None nor 0 and no event is received after max_wait_time
    """
    logger.info(f"len evant_batch: {len(event_batch)}")
    mongo = MongoDB(config.mdb_db, config.mdb_conn_str)

    logger.info("f{mongo=}")
    

    if len(event_batch)>0:
        tasks = [
            await on_event(partition_context, event, mongo) for event in event_batch
        ]
        responses = await asyncio.gather(*tasks)

    else:
        logger.info(f"No new event found!")

async def on_error(partition_context, error):
    """ 
    This method is handling errors
    parameters: partition_context, error
    """
    logger.error(f"Error in Consumer: {error}")
    await partition_context.update_checkpoint()


async def main():
    try:
        # consumer_client = await azure_managed_identity_authentication()
        consumer_client = await get_consumer_client()

        async with consumer_client:
            
            # Process an event at a time. Read from the beginning of the partition (starting_position: "-1")
            # await consumer_client.receive(on_event=on_event,
            #         starting_position="-1",
            #         on_error=on_error)

            # Process a batch of events
            await consumer_client.receive_batch(
                on_event_batch = on_event_batch,
                starting_position = "-1",
                max_batch_size = config.max_event_batch_size,
                on_error = on_error
            )
    except EventHubError as error:
        logger.error(error)
                
    except Exception as error:
        logger.error(f"Caught exception: {error}")
