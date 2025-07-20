import os
import aiohttp
import asyncio
import json
import pandas as pd 

from dotenv import load_dotenv
load_dotenv()

from model.model import OpenAI_Extract
from utils import config
from utils.config import logger

async def main(file_path):
    print("File Path ::::::::::: %s", file_path)
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            openai = OpenAI_Extract(session)
            response_llm = await openai.get_llm_output(file_path, file_bytes)
            logger.info(f"response_llm_final:::::::::::::::::::::::::::::::::::::: ::::::: {response_llm}")
            print("op:", json.dumps(response_llm, indent=2, ensure_ascii=False))
            
            if not response_llm :
                        doc_status = "failed"
            else:
                doc_status = "completed"

            logger.info(f"response_llm ::::::: {doc_status}")
            payload = {
                        "uid": "6691ebb337b27b3ee4f779ad",
                        "doc_id": "a11bdb01-d574-4a7f-9e6a-811151676cd2",
                        "file_name": "expenses/La Tomate.pdf",
                        "doc_status": doc_status,
                        "extracted_details": response_llm
                    }                 
            #for Appian 
            # headers = {
            #     "Content-Type": "application/json",
            #     "API-Key": config.appian_api_key

            #for local run 
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.appian_api_key}"
            }

            try:
                response = await session.post(
                    config.appian_api_url, 
                    headers=headers, 
                    # data=json.dumps(dict_data)
                    json=payload
                )
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Print the response
                logger.info(f"Response status code::::::::: {response.status}")
                logger.info(f"Response content::::::: {await response.json()}")

            except aiohttp.ClientError as e:
                logger.error(f"Exception while sending data to AppianAPI: {e}")

    file_name = "{0}".format(file_path.split('\\')[-1])

    op = {
        "doc_id": "a11bdb01-d574-4a7f-9e6a-811151676cd2", 
        "file_name": file_name, 
        "doc_status": doc_status, 
        "extracted_details": response_llm
    }

    json_dir = r"/home/yogi/Desktop/GenAI_Solutions/Demo Samples/Output"
    # Remove specific suffixes
    for suffix in ['.pdf', '.jpeg', '.jpg', '.png']:
        if file_name.endswith(suffix):
            file_name = file_name.removesuffix(suffix)
    
    json_file_name = json_dir+"\\"+file_name + ".json"
    
    with open(json_file_name, "w") as f:
        f.write(json.dumps(op, indent=2, ensure_ascii=False))

    df = pd.DataFrame(op)
# %%
    df = pd.DataFrame.from_records(pd.DataFrame(op["extracted_details"])["Invoice line-items"])
    df["file_name"] = op["file_name"]
    df["doc_status"] = op["doc_status"]

    # Remove specific suffixes
    for suffix in ['.pdf', '.jpeg', '.jpg', '.png']:
        if file_name.endswith(suffix):
            file_name = file_name.removesuffix(suffix)
  
    csvfilnename = json_dir+"\\"+file_name + ".csv"
    #csvfilnename = file_name.removesuffix(".json") + ".csv"
    df.to_csv(csvfilnename,index=False)

if __name__ == "__main__":
   
    dir_path = r"/home/yogi/Desktop/GenAI_Solutions/Demo Samples"
    
    file_name = "05_Air Sample.pdf"
    file_path = os.path.join(dir_path, file_name)
    asyncio.run(main(file_path))
