# import requests
import time
from functools import cache
import json
import asyncio

from utils import config
from utils.config import logger

class OCR_Engine:
    def __init__(self):
        self._vision_subscription_key = config.cognitive_services_subscription_key
        self._vision_base_url = config.cognitive_services_base_url
        self._vision_endpoint = config.cognitive_services_endpoint

    
    @cache
    async def get_ocr_output(self, input_file, session):
        # with open(tmp_file, "rb") as f:
        #     # subscription_key = os.getenv("key")
        #     # vision_base_url = os.getenv("service_url")
        text_recognition_url = self._vision_base_url + self._vision_endpoint
        headers = {
            "Ocp-Apim-Subscription-Key": self._vision_subscription_key,
            "Content-Type": "application/octet-stream",
        }
        response = await session.post(text_recognition_url, headers=headers, data=input_file)
        response.raise_for_status()
        logger.info(response.text)
        
        operation_url = response.headers["Operation-Location"]
        analysis = {}
        poll = True
        counter = 0
        while poll:
            response_final = await session.get(operation_url, headers=headers)
            # analysis = response_final.json()
            analysis = json.loads(await response_final.content.read())
            if "analyzeResult" in analysis:
                poll = False
            if ("status" in analysis) and (analysis["status"] == "Failed"):
                counter += 1
                if counter > 1:
                    poll = False
            if poll:
                await asyncio.sleep(0.5)

        op = analysis["analyzeResult"]["readResults"]       # Page wise segregation
        count = 0
        op_dict = {}
        for i in op:
            info = " ".join([line["text"] for line in i["lines"]])      # Page wise text corpus
            count += 1
            op_dict[f"Page_{count}"] = info

        return op_dict
