import os
import time
import json
import requests
from pathlib import Path
from utils.config import subscription_key, vision_base_url
from dotenv import load_dotenv
load_dotenv()

def ocr_output(fileName):
    fileName = Path(fileName)
    with open(fileName, "rb") as file:
        data = file.read()
    # print(data)
    subscription_key = subscription_key
    vision_base_url = vision_base_url
    
    text_recognition_url = vision_base_url + "vision/v3.2/read/analyze"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':'application/octet-stream'}
    response = requests.post(text_recognition_url, headers=headers, data=data)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]    
    analysis = {}
    poll = True
    while poll:
        response_final = requests.get(operation_url, headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if "analyzeResult" in analysis:
            poll = False
        if "status" in analysis and analysis['status'] == 'Failed':
            poll = False

    op = analysis["analyzeResult"]["readResults"]  # Page wise segregation
    count = 0
    op_dict = {}
    for i in op:
        info = " ".join([line['text'] for line in i['lines']])  # Page wise text corpus
        count += 1
        op_dict[f"Page_{count}"] = info
        
    # with open("OCR_OUTPUT/data_701.json", 'w') as json_file:
    #      json.dump(op_dict, json_file)
    # return str(op_dict)
    return str(op_dict)

def ocr_output_bytes(data):
    subscription_key = "key"
    vision_base_url = "service_url"
    text_recognition_url = vision_base_url + "vision/v3.2/read/analyze"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':'application/octet-stream'}
    response = requests.post(text_recognition_url, headers=headers, data=data)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]    
    analysis = {}
    poll = True
    while poll:
        response_final = requests.get(operation_url, headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if "analyzeResult" in analysis:
            poll = False
        if "status" in analysis and analysis['status'] == 'Failed':
            poll = False

    op = analysis["analyzeResult"]["readResults"]  # Page wise segregation
    count = 0
    op_dict = {}
    for i in op:
        info = " ".join([line['text'] for line in i['lines']])  # Page wise text corpus
        count += 1
        op_dict[f"Page_{count}"] = info
        
    return op_dict

