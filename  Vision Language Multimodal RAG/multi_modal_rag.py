import os
import torch
import asyncio
import tempfile
from PIL import Image
from typing import List
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from colpali_engine.models import ColPali, ColPaliProcessor
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.embeddings.huggingface  import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class AsyncMultiModalRAG:
    def __init__(self, google_api_key: str):
        # Set up Google API key
        google_api_key= "YOUR_GEMINI_API_KEY"

        # Initialize thread pool for CPU-bound tasks
        self.executor = ThreadPoolExecutor()

        # Initialize models
        self.setup_models()

    def setup_models(self):
        """Initialize all models"""
        # Initialize Gemini
        self.gemini = GeminiMultiModal(model_name="models/gemini-pro-vision")

        # Initialize Colpali
        self.colpali_model = ColPali.from_pretrained(
            "vidore/colpali-v1.3",
            torch_dtype=torch.bfloat16,
            device_map="cuda:0"  # Use "mps" for Apple Silicon
        ).eval()

        self.processor = ColPaliProcessor.from_pretrained("vidore/colpali-v1.3")

        # Configure LlamaIndex settings
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="vidore/colpali-v1.3"
        )

    async def pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Asynchronously convert PDF pages to images"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            convert_from_path,
            pdf_path
        )

    async def process_images_with_colpali(self, images: List[Image.Image]):
        """Process images with Colpali asynchronously"""
        loop = asyncio.get_event_loop()
        batch_images = await loop.run_in_executor(
            self.executor,
            lambda: self.processor.process_images(images).to(self.colpali_model.device)
        )

        async with asyncio.Lock():
            with torch.no_grad():
                image_embeddings = self.colpali_model(**batch_images)

        return image_embeddings

    async def create_temp_images(self, images: List[Image.Image]):
        """Create temporary image files asynchronously"""
        temp_paths = []
        loop = asyncio.get_event_loop()
        for i, img in enumerate(images):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                await loop.run_in_executor(self.executor, img.save, tmp.name)
                temp_paths.append(tmp.name)
        return temp_paths

    async def process_document(self, pdf_path: str):
        """Process PDF document and create index asynchronously"""
        # Convert PDF to images
        images = await self.pdf_to_images(pdf_path)
        logger.info("images created")

        # Process images with Colpali
        image_embeddings = await self.process_images_with_colpali(images)
        logger.info("image_embeddings created")

        # Create temporary image files for LlamaIndex
        temp_paths = await self.create_temp_images(images)

        # Create documents for LlamaIndex
        documents = []
        for path, emb in zip(temp_paths, image_embeddings):
            doc = {
                "image_path": path,
                "embedding": emb.cpu().numpy(),
                "metadata": {"type": "image"}
            }
            documents.append(doc)

        # Create vector index
        self.index = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            VectorStoreIndex.from_documents,
            documents
        )

        # Cleanup temporary files
        for path in temp_paths:
            os.unlink(path)

        return self.index

    async def process_query(self, question: str):
        """Process query with Colpali asynchronously"""
        loop = asyncio.get_event_loop()
        batch_query = await loop.run_in_executor(
            self.executor,
            lambda: self.processor.process_queries([question]).to(self.colpali_model.device)
        )

        async with asyncio.Lock():
            with torch.no_grad():
                query_embedding = self.colpali_model(**batch_query)

        return query_embedding

    async def query(self, question: str):
        """Query the document asynchronously"""
        # Process query
        query_embedding = await self.process_query(question)

        # Get relevant documents using vector search
        query_engine = self.index.as_query_engine()
        retrieved_docs = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            query_engine.query,
            question
        )

        # Use Gemini for final answer generation
        context_images = [doc.metadata["image"] for doc in retrieved_docs.source_nodes]

        response = await self.gemini.acomplete(
            prompt=f"Question: {question}\nContext: {retrieved_docs.response}",
            image_documents=context_images
        )

        return response

    async def aclose(self):
        """Cleanup resources"""
        self.executor.shutdown()

async def main():
    # Initialize
    rag = AsyncMultiModalRAG(google_api_key="your_google_api_key")

    try:
        # Process document
        pdf_path = "./home/yogi/Desktop/GenAI_Solutions/test.pdf"
        index = await rag.process_document(pdf_path)
        
        question = """
        Existence   definition:
        Determines whether or not the control is in place, regardless of the proportion of devices or the quality of the control. \n
        for for given question related to control \n

        Control Name: Authorized Software

        Description:
        A list of authorized software is maintained by the orgnaisation so that they can compare it to a software inventory and identify (then remove) unauthorized software. This control assesses the existence of the unauthorized software (Existence), the reviewing / comparison of installed software (Other), and the removal of unauthorized software (Other).

        /n Can you check Existence based on above information, just give yes or no with explanation nothing much,need citation from file name, if relvant info is present 
        """

        # Query
        questions = [
           question
        ]

        # Process queries concurrently
        tasks = [rag.query(q) for q in questions]
        responses = await asyncio.gather(*tasks)

        for question, response in zip(questions, responses):
            # print(f"Question: {question}")
            print(f"Response: {response}\n")

    finally:
        await rag.aclose()

if __name__ == "__main__":
    asyncio.run(main())