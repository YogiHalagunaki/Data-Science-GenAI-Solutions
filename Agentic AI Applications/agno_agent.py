import json
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.document.base import Document
from agno.models.azure import AzureOpenAI
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.knowledge.document import DocumentKnowledgeBase
from agno.embedder.azure_openai import AzureOpenAIEmbedder
from agno.document.chunking.agentic import AgenticChunking
from agno.playground import Playground, serve_playground_app
from agno.document.chunking.document import DocumentChunking

from dotenv import load_dotenv
load_dotenv()

db_url = "./tmp/lancedb"

# llm_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
llm_model="gpt-4-omni"
model=AzureOpenAI(id=llm_model)

# model=Gemini(id="gemini-2.0-flash-exp")

embedder=AzureOpenAIEmbedder(id="text-embedding-ada-002")

with open('./OCR_OUT/combined_ocr.json', 'r') as file:
    data = json.load(file)
    

def create_document(fact):
    return Document(content=fact)

def read_docs():
    documents = [create_document(fact) for fact in data]
    # documents = await asyncio.gather(*tasks)
    return documents
  
# documents= asyncio.run(read_docs())

documents= read_docs()

# try:
#     documents = asyncio.run(read_docs())
# except RuntimeError:
#     loop = asyncio.get_event_loop()
#     documents = loop.run_until_complete(read_docs())

# documents= read_docs()

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
    # debug_mode=True
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("agno_agent:app", reload=True)

# agent.print_response(question , markdown=True)