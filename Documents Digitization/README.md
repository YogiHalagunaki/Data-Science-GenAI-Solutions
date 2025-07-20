# 🧾 SmartDocument AI — Bill & Receipt Digitization API

SmartDocument AI is a powerful Fast API service that processes various types of scanned receipts and bills (e.g. hotel, bus, train, flight, food, cab, etc.) and transforms them into structured digital formats (JSON & Excel). It uses **Azure Cognitive Services OCR**, **Azure OpenAI LLM**, and integrates with **MongoDB** and **AWS S3** for full pipeline automation.

---

## 🌟 Key Features

- 📸 **OCR**: Extracts text from scanned PDFs, JPEG, PNG using Azure Read API  
- 🤖 **LLM-based Parsing**: Uses Azure OpenAI GPT to extract line items, vendor, dates, amounts  
- 📁 **Output Formats**: JSON and XLSX  
- ☁️ **Cloud Integration**:  
  - MongoDB for storing structured data  
  - S3 for storing original files and digital outputs  

---

## 🧰 Tech Stack

| Component           | Tool/Service                         |
|--------------------|---------------------------------------|
| OCR Engine          | Azure Cognitive Services (Read API)  |
| LLM Parsing         | Azure OpenAI (GPT model)             |
| Embedding Model     | `text-embedding-ada-002`             |
| Backend             | Python (asyncio, aiohttp, FastAPI)   |
| Storage             | MongoDB, AWS S3                      |
| Output Format       | JSON, Excel (XLSX)                   |

---
## 📬 API Workflow
* Client sends POST /upload with PDF or image.

* Backend:

  * Calls get_ocr_output() for OCR.

  * Sends OCR text to Azure OpenAI LLM.

  * Parses structured data.

  * Stores structured result in MongoDB.

  * Uploads original & structured data to S3.

* API responds with JSON + Excel download link.
---
## 🔧 OCR Function Example

```python
async def get_ocr_output(self, input_file, session):
    text_recognition_url = self._vision_base_url + self._vision_endpoint
    headers = {
        "Ocp-Apim-Subscription-Key": self._vision_subscription_key,
        "Content-Type": "application/octet-stream",
    }

    response = await session.post(text_recognition_url, headers=headers, data=input_file, timeout=30)
    response.raise_for_status()

    operation_url = response.headers["Operation-Location"]
    poll, counter, max_retries = True, 0, 20
    while poll and counter < max_retries:
        await asyncio.sleep(1)
        response_final = await session.get(operation_url, headers=headers)
        analysis = json.loads(await response_final.content.read())
        if "analyzeResult" in analysis:
            poll = False
        elif analysis.get("status") == "Failed":
            raise Exception("OCR analysis failed")
        counter += 1

    if counter >= max_retries:
        raise TimeoutError("OCR operation timed out.")

    op_dict = {}
    for idx, page in enumerate(analysis["analyzeResult"]["readResults"], start=1):
        text = " ".join([line["text"] for line in page["lines"]])
        op_dict[f"Page_{idx}"] = text

    return op_dict
```
---

## 🧠 LLM Model Configuration
```python
from langchain.chat_models import AzureOpenAI
import os

# Load model name from environment or use default
llm_model_name = os.getenv("llm_model_name", "azure/gpt-35-turbo-16k")

# Initialize Azure OpenAI chat model
llm = AzureOpenAI(
    engine=llm_model_name,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

```
---

## 📤 Sample Output
```json
{
  "vendor": "Hotel Grand",
  "date": "2025-07-10",
  "total_amount": 1200,
  "currency": "INR",
  "line_items": [
    { "description": "Room Rent", "amount": 1000 },
    { "description": "GST", "amount": 200 }
  ],
  "location": "Bangalore",
  "invoice_number": "INV12345"
}
```
---

## 🗃 MongoDB Document Schema
```json 
{
  "_id": ObjectId,
  "user_id": "abc123",
  "source_file": "hotel_invoice_0710.pdf",
  "vendor": "Hotel Grand",
  "date": "2025-07-10",
  "total": 1200,
  "line_items": [...],
  "raw_text": {...},
  "created_at": "2025-07-10T12:00:00Z"
}
```
---

## 🛠 Installation
```bash 
# Clone the repo
git clone https://github.com/yourusername/smartreceipt-ai.git
cd smartreceipt-ai

# Install dependencies
pip install -r requirements.txt
```
--- 

## 🧪 Running the API
```bash 
uvicorn main:app --reload
```
---

## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 

