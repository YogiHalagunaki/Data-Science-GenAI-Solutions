# 🧠 SLM Inference Streamlit UI

A lightweight, interactive Streamlit-based UI to manage and chat with small language models (SLMs) running via a local inference API.

## 🚀 Features

- ✅ List and manage downloaded models
- 📥 Download SLMs from predefined list
- 💬 Chat interface with selected model
- ⚙️ Customize inference parameters (temperature, top_p, top_k, penalties, etc.)
- 🧹 Clear chat history with a button click

## 📦 Models Available for Download

The following models can be downloaded and used via the UI:
- `llama-3.2-1b` – LLaMA 3.2B (1B variant)
- `qwen-2.5-1.5b` – Qwen 2.5 (1.5B)
- `qwen-2.5-0.5b` – Qwen 2.5 (0.5B)
- `gemma-2-2b` – Gemma 2 (2B)

## 🧰 Prerequisites

- Python 3.9+
- A backend REST API running locally at `http://localhost:8000` (must expose endpoints for model management and chat)

## 📁 Project Structure
```bash 
.
├── streamlit_app.py # Main Streamlit app
├── UI_items.py # UI components like headers
├── fastapi_server.py #backend server API
├── requirements.txt # Python dependencies
└── README.md # You're here

```

## 🔧 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Small LM Chat Bot Streamlit App  # or the correct path to your Chat Bot

```
### 2. Create a virtual environment:
```bash 
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```
### 3. Install dependencies:
```bash
pip install -r requirements.txt

```
### 4. Running the FastAPI Server
```bash
python fastapi_server.py

```
By default, the API runs on:
http://localhost:8000

### 5. Running the App
```bash 
streamlit run streamlit_app.py

Note :  Ensure your backend API is running at http://localhost:8000.
```
---
## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 
