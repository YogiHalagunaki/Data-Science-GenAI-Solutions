import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

## LangChain imports
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

## HuggingFace imports  
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub


from dotenv import load_dotenv
load_dotenv()

#db_url = "./tmp/lancedb"

## 1. LLM Model With HuggingFaceEmbeddings

llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.0, "max_length": 512}
)

## Sentence Transformers for embeddings basiclly for test to vector 
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

## 2. Load Documents input data 

with open("./home/yogi/Desktop/GenAI_Solutions/OCR_OUTPUT/test_ocr.json", "r") as file:
    data = json.load(file)

documents = [Document(page_content=str(item)) for item in data]

## 3.Vector DB
vectorstore = FAISS.from_documents(documents, embedder)

# 4. Retrieval with Scoring 

def retrieve_and_score(query: str, top_k: int = 5):
    # Embed query
    query_vec = embedder.embed_query(query)

    # Retrieve candidates
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    retrieved_docs = retriever.get_relevant_documents(query)

    # Embed retrieved docs
    doc_embeddings = [embedder.embed_query(doc.page_content) for doc in retrieved_docs]

    # Cosine similarity scoring
    scores = cosine_similarity([query_vec], doc_embeddings)[0]

    # Attach scores to docs
    scored_docs = list(zip(retrieved_docs, scores))
    scored_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

    return scored_docs

## 5. Question

question = """
Existence definition:
Determines whether or not the control is in place, regardless of the proportion of devices or the quality of the control. 

Control Name: Authorized Software

Description:
A list of authorized software is maintained by the organisation so that they can compare it to a software inventory and identify (then remove) unauthorized software. 
This control assesses the existence of the unauthorized software (Existence), the reviewing / comparison of installed software (Other), 
and the removal of unauthorized software (Other).

Can you check Existence based on above information? 
Just give yes or no with explanation, and cite file name if relevant.
"""

## 6. Retrieve + Score

scored_docs = retrieve_and_score(question, top_k=5)

print("\n--- Retrieved & Scored Documents ---")
for doc, score in scored_docs:
    print(f"Score: {score:.4f} | Content: {doc.page_content[:200]}...")

## 7. Build Context with system Prompt

context = "\n".join([doc.page_content for doc, _ in scored_docs[:2]])

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a compliance assistant. Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer with "Yes" or "No" and a short explanation. Cite the file name if possible.
"""
)

prompt = prompt_template.format(context=context, question=question)

## 8. Run LLM

response = llm.invoke(prompt)

print(response)
