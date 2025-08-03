# [A] Async MultiModal RAG with ColPali and Gemini

This project implements an **Asynchronous MultiModal Retrieval-Augmented Generation (RAG)** system that combines **ColPali** (a vision-language model-VLM) and **Gemini Pro Vision** (via Google's API) to extract insights from PDFs using a multimodal document processing pipeline.

---

## 🧠 Features

- 🔍 **PDF to Image Conversion** (async)
- 🖼️ **Image Embedding using ColPali**
- 🔎 **Query Embedding and Similarity Search**
- 🌐 **Final Answer Generation via Gemini Pro Vision**
- ⚡ **Fully Async Architecture** for high-performance

---

## 📦 Components Used

| Component          | Purpose                                              |
|--------------------|------------------------------------------------------|
| `ColPali`          | Embeds images and text into a shared latent space    |
| `Gemini Pro Vision`| LLM that handles visual + text context queries       |
| `LlamaIndex`       | Embedding-based document indexing and querying       |
| `pdf2image`        | Converts PDF pages into PIL images                   |
| `asyncio`          | Handles concurrent tasks like embedding and indexing |
| `loguru`           | Structured logging                                   |

---
## File Structure
```bash
multi_modal_rag.py           # Main Python script
.env                         # Environment file with API key
requirements.txt             # Python dependencies
test.pdf                     # Sample document to test with

```
---
## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git lone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Computer Vision Multimodal RAG

```
### 2. Create a Python Environment
```bash 
python3 -m venv venv
source venv/bin/activat

```
### 3. Install Dependencies
```bash 
pip install -r requirements.txt

```
### 4. Install System Dependencies
```bash 
sudo apt install poppler-utils  # Required by pdf2image

```
### 4. Set Up API Key

Create a .env file with the following:
```bash 
GOOGLE_API_KEY=your_actual_gemini_api_key

```
### 5. Run the Main Script
```bash 
python multi_modal_rag.py

```
Example query:
```bash 
Control Name: Authorized Software
Can you check if the control exists based on the PDF content?

```
---
# [B] 🧠 Structured Document Control Evaluation with Phi, Claude, and OCR (Computer Vision)

This project uses a **multi-agent LLM pipeline** built with the [Phi framework](https://github.com/phi-lang/phi) to extract structured control evaluation data from documents. It combines OCR processing, Claude/Gemini/Azure LLMs, vector-based retrieval, and pydantic models to generate clean, machine-readable outputs.

---

## 📌 Features

- 🧾 **OCR Integration** — Converts scanned PDFs into text
- 📚 **Document Knowledge Base** — Chunked, embedded, and stored using LanceDB
- 🧠 **Claude / GPT-4 / Gemini Models** — Choose your preferred model for reasoning
- 🧠 **Agentic Chunking** — Automatically splits documents for intelligent processing
- ✅ **Structured Pydantic Output** — Ensures predictable schema-compliant results

---

## 📁 Folder Structure

```bash
.
├── ocr_computer_vision.py           # OCR function to extract data from PDF
├── prompts.py                       # Prompt templates (optional)
├── pydantic_models.py               # Defines ControlEvaluations model
├── phi_vision_rag_agent.py          # Main script (your provided code)
├── .env                             # For storing environment variables
├── tmp/lancedb/                     # LanceDB vector database files
├── test.pdf                         # Input PDF document

```
---
## 🔧 Setup Instructions

### 1. Clone and Setup Environment
```bash
git lone https://github.com/YogiHalagunaki/Data-Science-GenAI-Solutions.git
cd Computer Vision Multimodal RAG

python3 -m venv venv
source venv/bin/activate

```
### 2. Install Dependencies
Install Python packages:
```bash 
pip install -r requirements.txt

```
### 3. Setup .env File
Create a .env file with your keys:
```bash 
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_google_api_key

```
### 4. Input
The system expects a PDF file at:
```bash
file_name = "./home/yogi/Desktop/GenAI_Solutions/test.pdf"

```
### 5. Running the Project
To run the main script:
```bash 
python phi_vision_rag_agent.py

```
Sample interaction:
```text
structured_output_agent.print_response("extract info ControlEvaluations")

```
### 6. Output Example

```text
{
  "control_name": "Authorized Software",
  "status": "Yes",
  "evidence": "Detected software list comparison in section 2",
  "citation": "test.pdf page 3"
}
```
---

## 📌 Notes
* Ensure your API keys are active and have access to the required models.

* Claude 3.5 requires Anthropic API setup.

* You may comment out knowledge_base.load(recreate=False) after the first run to persist LanceDB.

---
## 🙌 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) – Multimodal language models from Google, used for vision-language understanding.
- [ColPali Vision-Language Model](https://huggingface.co/vidore/colpali-v1.3) – Open-source VLM for document-level image-text embedding and retrieval.
- [LlamaIndex](https://www.llamaindex.ai/) – Framework for building context-augmented applications with LLMs and data.
- [Phi Framework](https://github.com/phi-lang/phi) – Modular agent framework for building LLM-based workflows.
- [Anthropic Claude](https://www.anthropic.com/index/claude) – Powerful LLM by Anthropic used for reasoning and structured output.
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview) – Azure-hosted access to OpenAI models like GPT-4, GPT-4o, and embeddings.
- [LanceDB](https://lancedb.github.io/lancedb/) – Fast, local, vector database for semantic search.

---
## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 

