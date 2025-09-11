import os
import json
import logging
import requests
import datetime
from utils import config
from pydantic import BaseModel
from utils.config import logger
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from fastapi import FastAPI, BackgroundTasks
from codes.finance_doc_processing_rag_agent import structured_output_agent
from codes.prompts import system_prompt, additional_prompts
from codes.pydantic_models import ControlEvaluations
from codes.validate_results import validate_result

app = FastAPI()

class GenCntxRequest(BaseModel):
    #doc_id: str
    filepath: str
    
@app.post("/skense/insurance_finance_doc_processing")
async def doc_processing(request_data: GenCntxRequest, background_tasks: BackgroundTasks):
   
    filepath = request_data.filepath

    if not filepath:
        return {"detail": "filepath not found", "status": "FAILURE"}, 400
   
    logger.info(f"filename::::::::::{filepath}")

    try:       
        # Add the background task to process the data
        background_tasks.add_task(
            process_extraction,
            filepath
        )
        
        # Return a response immediately
        return {"status": 200, "message": "Processing started in background", "filepath": filepath}
        
    except Exception as e:
        logger.error(f"Error while fetching file to Data Extraction::{e}")
        return {"filepath": filepath, "error": str(e), "status": "FAILURE"}, 500

# Define the background task function
async def process_extraction(doc_id, filename):
    try:
        logger.info(f"Background processing started")
        ## call the LLM here 
        
        question="""
        extract the pydantic data from document and use this prompt :{system_prompt} and {additional_prompts}

        """
        
        result = structured_output_agent.print_response(question)

        #structured_output_agent.print_response("extract info ControlEvaluations")
        #responce_data = json.loads(result)
        if result:
            ## write code to compaire the to json file 
            responce_data = validate_result(result)

            return responce_data
        else:

            logger.info(f"No result from LLM")
        
        logger.info(f"Background processing completed")
        
    except Exception as e:
        logger.error(f"Error in background processing")
