import os
import json
import asyncio
import aiohttp
from unidecode import unidecode

from model.model import OpenAI_Extract
from utils import config
from utils.config import logger
import utils.aws_services as aws

async def delete_file(file_path):
    os.remove(file_path)
async def post_process_sanitization(self, response):
    #code to right here 

    Tax_KeyWords = ["Accommodation - Service Charge (P)","Accommodation - GST (P)",
                   "STANDARD STATE & CO. SALES TAX", "COUNTY TRANSIENT ROOM TAX",
                   "CITY TRANSIENT ROOM TAX","STATE TRANSIENT ROOM TAX", 
                   ""
                   ]
    return response
async def process_doc(doc_body, session):
    try:
        # Get object of file in S3 bucket
        file_obj = aws.get_file_object_s3(
            s3_client=config.boto3_client,
            bucket=config.s3_bucket_input,
            object_name=doc_body['filename']
        )

        # Call OpenAI API
        # with open(file_path, "rb") as f:
        openai = OpenAI_Extract(session)
        response = await openai.get_llm_output(file_obj)
        logger.info(f"op:\n{json.dumps(response, indent=2)}")
        # output sanitization
        response = await post_process_sanitization(response)
        dict_op = {
            "doc_id": doc_body['doc_id'],
            "filename": doc_body['filename'],
            "doc_status": "completed",
            "extracted_details": response
        }
        
        # # Delete the downloaded file
        # await delete_file(file_path)

        return dict_op

    except Exception as e:
        logger.error(f"Exception occured: {e}")
