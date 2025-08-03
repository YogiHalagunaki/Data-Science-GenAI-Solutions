import json
import asyncio
from phi.agent import Agent
from phi.model.google import Gemini
from phi.document.base import Document
from phi.vectordb.lancedb import LanceDb
from phi.vectordb.search import SearchType
from phi.model.azure import AzureOpenAIChat
from phi.knowledge.document import DocumentKnowledgeBase
from phi.embedder.azure_openai import AzureOpenAIEmbedder
from phi.document.chunking.agentic import AgenticChunking
from phi.document.chunking.document import DocumentChunking

from dotenv import load_dotenv
load_dotenv()

db_url = "./tmp/lancedb"

# llm_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# llm_model="gpt-4-omni"
# model=AzureOpenAIChat(id=llm_model)

model=Gemini(id="gemini-1.5-pro-002")

embedder=AzureOpenAIEmbedder(model="text-embedding-ada-002")

with open('./home/yogi/Desktop/GenAI_Solutions/OCR_OUTPUT/test_ocr.json', 'r') as file:
    data = json.load(file)
    
async def create_document(fact):
    return Document(content=fact)

async def read_docs():
    tasks = [create_document(fact) for fact in data]
    documents = await asyncio.gather(*tasks)
    return documents
  
documents=asyncio.run( read_docs())

knowledge_base = DocumentKnowledgeBase(
    documents=documents,   
    chunking_strategy=AgenticChunking(model=model,max_chunk_size=5000),
    vector_db=LanceDb(
        table_name="json_documents",
        uri=db_url,
        search_type=SearchType.hybrid,
        embedder=AzureOpenAIEmbedder(model="text-embedding-ada-002"),
        
    ),
    # chunking_strategy=DocumentChunking(overlap=1000),
    num_documents=10,  # Number of documents to return on search
)

## Comment out after first run
# knowledge_base.load(recreate=False)

agent = Agent(
    model=model,
    knowledge=knowledge_base,
    # show_tool_calls=True,
    search_knowledge=True,
    # reasoning=True
)

question = """
Existence   definition:
Determines whether or not the control is in place, regardless of the proportion of devices or the quality of the control. \n
for for given question related to control \n

Control Name: Authorized Software

Description:
A list of authorized software is maintained by the orgnaisation so that they can compare it to a software inventory and identify (then remove) unauthorized software. This control assesses the existence of the unauthorized software (Existence), the reviewing / comparison of installed software (Other), and the removal of unauthorized software (Other).

/n Can you check Existence based on above information, just give yes or no with explanation nothing much,need citation from file name, if relvant info is present 
 """
 
agent.print_response(question , markdown=True)