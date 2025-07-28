# 🧠 Small LM Chatbot API
    - FastAPI
    - streamlit application 

* This project provides a FastAPI-based interface for running Small Language Models (SLMs) like Qwen, LLaMA, and Gemma locally. You can download, load, chat with, unload, and delete models using simple REST API endpoints.

---

## 📦 Features

- 🚀 Serve small open-source LLMs from Hugging Face (GGUF format)
- 💬 Chat completions via POST /chat
- 🔁 Stream or non-stream responses
- 📥 Dynamic model download from Hugging Face
- 🧹 Unload models from memory
- 🗑️ Delete local model files
- 🔌 Simple test client using `requests`

---

## 🏗️ Project Structure
```bash
.
├── fastapi_server.py     # FastAPI backend to load and chat with models
├── fastapi_client.py     # Python test client using `requests`
├── .env                  # Environment file (for HF token)
└── README.md             # You are here

```

---

## 🛠 Requirements

- Python 3.8+
- `llama-cpp-python`
- `fastapi`, `uvicorn`
- `httpx`, `requests`, `loguru`, `pydantic`, `python-dotenv`

Install them using:

```bash
pip install -r requirements.txt

```
## 📁 Model Configurations
```python 
model_config = {
    "qwen-2.5-0.5b": {
        "repo_id": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "filename": "qwen2.5-0.5b-instruct-fp16.gguf"
    }
}

```

### 🔐 1. Environment Variables
```env
HUGGINGFACE_TOKEN=your_hf_token_here

```
---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Small LM Chat Bot FastAPI  # or the correct path to your Chat Bot

```

### 2. API Endpoints
```table
| Method | Endpoint                 | Description                         |
| ------ | ------------------------ | ----------------------------------- |
| GET    | `/`                      | Health check                        |
| POST   | `/models/download`       | Download and load a model           |
| GET    | `/models`                | List all loaded models              |
| POST   | `/chat`                  | Chat with a loaded model            |
| POST   | `/models/{model}/unload` | Unload a specific model from memory |
| DELETE | `/models/{model}`        | Delete model from disk              |

```
### 3. Chat Request Payload

```json
{
  "model_name": "qwen-2.5-0.5b",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 100,
  "stream": false
}

```
### 4. Running the FastAPI Server
```bash
python fastapi_server.py

```
By default, the API runs on:
http://localhost:8000

### 5.Testing with the Python Client
```bash 
python fastapi_client.py

```
Inside the script, you can enable/disable tests:
```bash 
# test_root()
# test_download_model()
test_chatBot("Tell me a joke.")
test_chatBot("My name is Yogi. Can you help me write a formal leave application for my office?")
# test_unload_model()
# test_delete_model()

```

## 💡 Example Chat
```text
Yogi: "How many states are in India?"
ChatBot: "India has 28 states and 8 Union Territories as of 2025."
```

---
## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 
