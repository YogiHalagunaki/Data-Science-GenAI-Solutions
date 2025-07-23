import json
import pandas as pd
from utils import config
from ast import literal_eval
from utils.config import logger
from model.ocr_engine import OCR_Engine
import model.llm_prompts_1 as prompts

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings

# from dotenv import load_dotenv
# load_dotenv()

llm=AzureOpenAI(
            engine=config.llm_model_name,
            api_key = config.azure_openai_api_key,
    azure_endpoint = config.azure_openai_api_base,
    api_version = config.azure_openai_api_version
            )
embed_model = AzureOpenAIEmbedding(
    model = "text-embedding-ada-002",
    deployment_name = "text-embedding-ada-002",
    api_key = config.azure_openai_api_key,
    azure_endpoint = config.azure_openai_api_base,
    api_version = config.azure_openai_api_version,
)
Settings.llm=llm
Settings.embed_model = embed_model
Settings.chunk_size = 512

class OpenAI_Extract:
    def __init__(self, session):
        self.session = session

    async def data_index(self, file_name, file_bytes):
        documents = []
        # ocr_out = await ocr_output(file)
        # op_ocr = await OCR_Engine.get_ocr_output(file, self.session)
        ocr_engine = OCR_Engine()
        op_ocr = await ocr_engine.get_ocr_output(file_bytes, self.session)
        
        for page_num, content in op_ocr.items():
            documents.append(Document(text=content, metadata={"filename": file_name, "page_num": page_num}))
        return documents
    
    async def get_query_engine(self, documents):
        pipeline = IngestionPipeline(
            transformations=[MarkdownNodeParser(), embed_model]
        )
        nodes = await pipeline.arun(documents=documents, num_workers=8)
        
        index = VectorStoreIndex(nodes)
        storage_context = StorageContext.from_defaults()
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )
        query_engine = index.as_query_engine(similarity_top_k=30)
        return  query_engine
        
    async def get_llm_output(self, file_name, file_bytes):
        if not ( file_name.lower().endswith(".pdf") or file_name.lower().endswith(".jpeg") or file_name.lower().endswith(".jpg") or file_name.lower().endswith(".png")):
            raise Exception(status_code=400, detail="Only PDF, JPEG,JPG and PNG files are allowed")

        # with NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(await file.read())
        #     temp_file.seek(0)
        logger.info("Started indexing")
        documents= await self.data_index(file_name, file_bytes)
            
        logger.info("Creating Query Engine")
        query_engine= await self.get_query_engine(documents)
            
        logger.info("Querying from Index")
        full_query = f"{prompts.system_prompt}\n\nExtraction Guidelines : {prompts.additional_prompts}"
        # out_name =await llm_out(query_engine)
        out_name = await query_engine.aquery(full_query)
        out_name = out_name.response
            
        # final_out_2=fix_final_json(out_name)
        logger.info(f"response:{out_name}")

        try:
            op = json.loads(out_name)
            logger.info(f"op_1::::::::::::::::::{op}")
        except:
            try:
                op = out_name.json()
                logger.info(f"op_2::::::::::::::::::{op}")
            except:
                try:
                    op = literal_eval(out_name)
                    logger.info(f"op_3::::::::::::::::::{op}")
                except:
                    op = None
        logger.info(f"Final_op::::::::::::::::::{op}")
        return op
