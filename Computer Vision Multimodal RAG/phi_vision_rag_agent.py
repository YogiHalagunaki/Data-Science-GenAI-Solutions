import json
import asyncio
from prompts import *
from loguru import logger
from phi.agent import Agent
from phi.model.google import Gemini
from phi.document.base import Document
from phi.model.aws.claude import Claude
from phi.vectordb.lancedb import LanceDb
from ocr_computer_vision import ocr_output
from phi.vectordb.search import SearchType
from phi.model.azure import AzureOpenAIChat
from pydantic_models import ControlEvaluations
from phi.knowledge.document import DocumentKnowledgeBase
from phi.embedder.azure_openai import AzureOpenAIEmbedder
from phi.document.chunking.agentic import AgenticChunking

from dotenv import load_dotenv
load_dotenv()

db_url = "./tmp/lancedb"

# llm_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"

llm_model="gpt-4-omni"
# model=AzureOpenAIChat(id=llm_model)

model=Claude(id="anthropic.claude-3-5-sonnet-20240620-v1:0")

# model=Gemini(id="gemini-1.5-pro-002")

embedder=AzureOpenAIEmbedder(model="text-embedding-ada-002")

# with open('./OCR_OUT/combined_ocr.json', 'r') as file:
#     data = json.load(file)

file_name="./home/yogi/Desktop/GenAI_Solutions/test.pdf"
data=[ocr_output(file_name)]
# logger.info(small)
# data = json.load(data)
# logger.info(data[:10])

async def create_document(fact):
    return Document(content=fact,embedder=embedder)

async def read_docs():
    tasks = [create_document(fact) for fact in data]
    documents = await asyncio.gather(*tasks)
    logger.info(len(documents))
    return documents
  
documents=asyncio.run(read_docs())

knowledge_base = DocumentKnowledgeBase(
    documents=documents,   
    chunking_strategy=AgenticChunking(model=model,max_chunk_size=5000),
    vector_db=LanceDb(
        table_name="json_documents",
        uri=db_url,
        search_type=SearchType.hybrid,
        embedder=embedder,
        
    ),
    # chunking_strategy=DocumentChunking(overlap=1000),
    num_documents=20,  # Number of documents to return on search
)

## Comment out after first run
knowledge_base.load(recreate=False)

# class InfoData(BaseModel):
#     """extract info"""
#     summary: str = Field(..., description="Provide Document Summary")
#     rules: str = Field(..., description="rules mentioned in document about form")

structured_output_agent  = Agent(
    model=model,
    knowledge=knowledge_base,
    # show_tool_calls=True,
    search_knowledge=True,
    # instructions=["you are useful pydantic extraction agent, which will never break give some results"],
    response_model=ControlEvaluations,
    structured_outputs=True,
    # debug_mode=True,
    # reasoning=True
)

question="""
extract the pydantic data from document

"""
# structured_output_agent.print_response(question)

structured_output_agent.print_response("extract info ControlEvaluations")