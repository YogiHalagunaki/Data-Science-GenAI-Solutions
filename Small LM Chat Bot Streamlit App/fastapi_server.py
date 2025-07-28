import os
import json
import httpx
import shutil
import asyncio
import uvicorn
from pathlib import Path
from llama_cpp import Llama
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException

from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Get HF token from environment variable, with a default of None
HF_TOKEN = "HUGGINGFACE_TOKEN"

app = FastAPI(title="Small LM API")

# Constants
BASE_DIR = Path.cwd() / "small_lm_models"
BASE_DIR.mkdir(exist_ok=True)
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for downloading

# Pydantic Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model_name: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000
    stream: Optional[bool] = False
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = 40
    repeat_penalty: Optional[float] = 1.1
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    
    model_config = {
        'protected_namespaces': ()
    }

class ModelRequest(BaseModel):
    model_name: str
    model_url: HttpUrl
    
    model_config = {
        'protected_namespaces': ()
    }

class ModelInfo(BaseModel):
    name: str
    path: str
    size_mb: float
    last_used: str
    status: str

# Add this model class for request validation
class DownloadModelRequest(BaseModel):
    model_name: str
    repo_id: str
    filename: str
    
    model_config = {
        'protected_namespaces': ()
    }

# Add this before the ModelManager class
model_config = {
    "llama-3.2-1b": {
        "repo_id": "bartowski/Llama-3.2-1B-Instruct-GGUF",
        "filename": "Llama-3.2-1B-Instruct-Q6_K_L.gguf"
    },
    "qwen-2.5-1.5b": {
        "repo_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "filename": "qwen2.5-1.5b-instruct-fp16.gguf"
    },
    "qwen-2.5-0.5b": {
        "repo_id": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "filename": "qwen2.5-0.5b-instruct-fp16.gguf"
    },
    "gemma-2-2b": {
        "repo_id": "bartowski/gemma-2-2b-it-GGUF",
        "filename": "gemma-2-2b-it-Q6_K_L.gguf"
    }
}

# Global state management
class ModelManager:
    def __init__(self):
        self.loaded_models: Dict[str, Llama] = {}
        self.model_locks: Dict[str, asyncio.Lock] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def get_model(self, model_name: str) -> Llama:
        if model_name not in self.model_locks:
            self.model_locks[model_name] = asyncio.Lock()
        
        async with self.model_locks[model_name]:
            if model_name not in self.loaded_models:
                try:
                    # Download/get model path first
                    model_path = await download_model_to_local(model_name)
                    
                    # Load model from local path
                    model = await asyncio.get_event_loop().run_in_executor(
                        self.executor,
                        lambda: Llama(
                            model_path=str(model_path),
                            n_ctx=2048,
                            n_threads=4,
                            n_batch=512
                        )
                    )
                    self.loaded_models[model_name] = model
                except Exception as e:
                    logger.error(f"Error loading model {model_name}: {e}")
                    raise HTTPException(status_code=500, detail=str(e))
            
            return self.loaded_models[model_name]
    
    async def unload_model(self, model_name: str):
        if model_name in self.loaded_models:
            async with self.model_locks[model_name]:
                del self.loaded_models[model_name]

model_manager = ModelManager()

# Utility functions
async def download_file(url: str, path: Path):
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', str(url)) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with open(path, 'wb') as f:
                async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE):
                    f.write(chunk)

# Add this near the top with other utility functions
async def download_model_to_local(model_name: str) -> Path:
    if model_name not in model_config:
        raise HTTPException(status_code=404, detail="Model not found")
    
    config = model_config[model_name]
    model_dir = BASE_DIR / model_name
    model_path = model_dir / config["filename"]
    
    # If model already exists locally, just return the path
    if model_path.exists():
        return model_path
    
    # Create directory if it doesn't exist
    model_dir.mkdir(exist_ok=True)
    
    # Download from Hugging Face
    try:
        model = Llama.from_pretrained(
            repo_id=config["repo_id"],
            filename=config["filename"],
            token=HF_TOKEN,
            local_dir=str(model_dir)
        )
        return model_path
    except Exception as e:
        if model_dir.exists():
            shutil.rmtree(model_dir)
        raise e


@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "status": "online",
        "service": "Small LM API",
        "version": "1.0.0"
    }
    
# API Endpoints
@app.post("/models/download")
async def download_model(request: DownloadModelRequest):
    try:
        model = await model_manager.get_model(request.model_name)
        return {"status": "success", "message": f"Model {request.model_name} loaded successfully"}
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models() -> List[ModelInfo]:
    models = []
    # Add loaded models from model_manager
    for model_name in model_manager.loaded_models:
        models.append(ModelInfo(
            name=model_name,
            path=str(BASE_DIR / model_name),
            size_mb=0,  # You might want to calculate this
            last_used=datetime.now().isoformat(),
            status="loaded"
        ))
    return models

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        model = await model_manager.get_model(request.model_name)
        
        # Create completion parameters dictionary
        completion_params = {
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream,
            "top_p": request.top_p,
            "top_k": request.top_k,
            "repeat_penalty": request.repeat_penalty,
            "presence_penalty": request.presence_penalty,
            "frequency_penalty": request.frequency_penalty
        }
        
        if request.stream:
            async def generate_responses():
                response = model.create_chat_completion(**completion_params)
                for chunk in response:
                    yield json.dumps(chunk) + "\n"
            
            return StreamingResponse(generate_responses(), media_type="text/event-stream")
        else:
            response = await asyncio.get_event_loop().run_in_executor(
                model_manager.executor,
                lambda: model.create_chat_completion(**completion_params)
            )
            return response
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    model_dir = BASE_DIR / model_name
    
    # Check both loaded models and directory
    if not model_dir.exists() and model_name not in model_manager.loaded_models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # First unload if it's loaded
        if model_name in model_manager.loaded_models:
            await model_manager.unload_model(model_name)
        
        # Then delete the directory
        if model_dir.exists():
            shutil.rmtree(model_dir)
        
        return {"message": f"Model {model_name} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/{model_name}/unload")
async def unload_model(model_name: str):
    try:
        await model_manager.unload_model(model_name)
        return {"message": f"Model {model_name} unloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
