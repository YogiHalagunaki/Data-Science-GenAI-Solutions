import io
import os
import fitz 
import json
import time
import base64
import asyncio
import logging
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from litellm import completion

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

AZURE_API_KEY = ""
AZURE_API_BASE = ""
AZURE_API_VERSION = ""

def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def ensure_output_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

system_prompt = """
You are an OCR Extraction agent that extracts tables from PDFs into Markdown format.
Follow these rules strictly:

1. Extract all tables on each page in **Markdown format** always properly without missing.
2. Identify if tables continue across pages, including cases where headers are missing or columns span multiple pages.
3. Handle scenarios where a column remains empty across multiple pages while ensuring table structure integrity.
4. Do not include additional text outside tables unless needed for table continuity.
5. Provide structured output so that tables can be merged intelligently if necessary.
"""

async def multimodal_llm_azure(image, semaphore, page_num):
    async with semaphore:
        encoded_data = image_to_base64(image)
        query = system_prompt
        
        resp = completion(
            model="azure/gpt-4-omni",
            temperature=0,
            max_tokens=3000,
            api_base= AZURE_API_BASE,
            api_version= AZURE_API_VERSION,
            api_key= AZURE_API_KEY,
            top_p=0.9,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_data}"}}
                ]
            }]
        )
        
        content = resp.choices[0].message.content
        logger.info(f"Processed page {page_num}")
        return {"page": page_num, "tables_markdown": content}

async def process_pdf(pdf_path, max_parallel):
    images = pdf_to_images(pdf_path)
    semaphore = asyncio.Semaphore(max_parallel)
    tasks = [multimodal_llm_azure(image, semaphore, i+1) for i, image in enumerate(images)]
    results = await asyncio.gather(*tasks)
    return results

async def merge_tables_with_llm(pages_data):
    """Send extracted tables to LLM for intelligent merging."""
    prompt = """
    You are an AI designed to intelligently merge tables extracted from a multi-page document.
    Given the tables in Markdown format from different pages, identify and merge tables that continue across pages.
    Ensure the merged tables maintain proper structure and remove redundancies.
    Handle cases where headers are missing, columns span multiple pages, and some columns remain empty across pages.
    Return the final structured tables in Markdown format.
    Normalize dates also.
    """
    
    extracted_tables = "\n\n".join([f"Page {p['page']}\n{p['tables_markdown']}" for p in pages_data])
    
    resp = completion(
        model="azure/gpt-4-omni",
        temperature=0,
        max_tokens=5000,
        api_base= AZURE_API_BASE,
        api_version= AZURE_API_VERSION,
        api_key=AZURE_API_KEY,
        top_p=0.9,
        messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "text", "text": extracted_tables}]}
        ]
    )
    
    return resp.choices[0].message.content

def save_to_excel(markdown_text, output_file):
    """Converts Markdown tables into Excel format."""
    tables = []
    current_table = []
    for line in markdown_text.split('\n'):
        if '|' in line:
            current_table.append(line)
        elif current_table:
            df = pd.read_csv(io.StringIO('\n'.join(current_table)), delimiter='|').dropna(axis=1, how='all')
            tables.append(df)
            current_table = []
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for idx, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f'Table_{idx+1}', index=False)
    
    logger.info(f"Excel saved: {output_file}")

async def main(pdf_path):
    
    start_time = time.time()
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join("output", pdf_name)
    ensure_output_folder_exists(output_folder)
    
    output_json = os.path.join(output_folder, "tables_extracted.json")
    output_excel = os.path.join(output_folder, "merged_tables.xlsx")
    
    logger.info(f"Processing PDF: {pdf_path}")
    extracted_data = await process_pdf(pdf_path, max_parallel=5)
    
    # Save extracted tables in JSON format
    with open(output_json, 'w') as f:
        json.dump(extracted_data, f, indent=2)
    logger.info(f"Markdown tables saved in JSON: {output_json}")
    
    # Get merged tables from LLM
    merged_tables_markdown = await merge_tables_with_llm(extracted_data)
    logger.info(merged_tables_markdown)
    # Save merged tables to Excel
    save_to_excel(merged_tables_markdown, output_excel)
    
    end_time = time.time()
    logger.info(f"Total processing time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    pdf_path = r"/home/yogi/Desktop/GenAI_Solutions/AFR_TABLE_EXTRACTION/Sample files/Sample files/2024-10-24-d874903ff099.pdf"
    asyncio.run(main(pdf_path))
