# 📄 Finance Document Processing using LLM and RAG Agent Pipline 

This project extracts structured **bond trade data** from financial documents (PDF term sheets, etc.) using a combination of **OCR + RAG (Retrieval-Augmented Generation)**.  
It validates extracted results against ground truth and generates a color-coded **Excel validation report**.  

---

## 🚀 Features

- 🔎 Extracts text from PDFs using **Azure Computer Vision OCR**.  
- 🤖 Uses **LLM (Anthropic Claude / OpenAI / Gemini)** with strict JSON schema to convert text into structured trades.  
- 📦 Stores OCR chunks and embeddings in **LanceDB** for retrieval.  
- ✅ Defines trade schema with **Pydantic models** for validation.  
- 📊 Compares extracted vs. actual JSON and generates **Excel reports** with green/red highlights.  
- ⚡ Modular design → easily extendable to other financial or insurance documents.  

---

## 📂 Project Structure

```
.
├── finance_doc_processing_rag_agent.py   # Main RAG pipeline orchestrator
├── models.py                             # Pydantic models for trades
├── ocr_computer_vision.py                # Azure OCR extraction
├── prompts.py                            # LLM extraction prompts
├── validate_results.py                   # JSON validation + Excel export
├── Genel Energy.pdf                      # Sample financial document (bond term sheet)
├── Genel_Energy_Trades.json              # Ground truth JSON for validation
└── trade_validation.xlsx                 # Example validation output
```

---

## 🛠️ Setup

### 1️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables
Create a `.env` file in the root directory:

```env
AZURE_SUBSCRIPTION_KEY=your_azure_key
AZURE_VISION_BASE_URL=https://<your-region>.api.cognitive.microsoft.com/
DB_URL=./tmp/lancedb
LLM_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0
EMBEDDING_MODEL=text-embedding-ada-002
```

---

## 📖 Usage

### 🔹 1. OCR a PDF
Extract raw text using Azure OCR:

```python
from ocr_computer_vision import ocr_output

text_data = ocr_output("Genel Energy.pdf")
print(text_data)
```

---

### 🔹 2. Run RAG Agent for Trade Extraction
Run the pipeline that embeds, retrieves, and extracts JSON:

```bash
python finance_doc_processing_rag_agent.py
```

This will:
- OCR the document  
- Store embeddings in LanceDB  
- Generate JSON output following the `Trade` Pydantic schema  

---

### 🔹 3. Validate Extracted Results
Compare model output with ground-truth JSON:

```python
from validate_results import validate_result
import json

# Example result (LLM output)
result_data = {
  "trades": [
    {
      "TradeID": 1,
      "ISIN": "NO0010894330",
      "Issuer": "Genel Energy Finance 4 Limited",
      "Maturity": "2025-10-14",
      "Notional": 3000000,
      "Coupon": 9.25,
      "Currency": "USD",
      "SettlementDate": "2020-10-14",
      "DayCountFraction": "30/360",
      "InterestPaymentDate": "2021-04-14",
      "IssueDate": "2020-10-14",
      "IssueAmount": 300000000,
      "IssuePrice": 97,
      "NominalAmountPerBond": 2000,
      "InterestPaymentFrequency": "Semi-annual",
      "BusinessDayConvention": "Unadjusted",
      "BusinessDayLocation": ["Oslo", "New York"],
      "AmortizationType": "Bullet",
      "MinimumSubscription": 200000,
      "Parent": "Genel Energy plc"
    }
  ]
}

validate_result(result_data)
```

This generates:

📊 `trade_validation.xlsx` → with **conditional formatting**:
- ✅ Green = Match  
- ❌ Red = Mismatch  

---

## 📑 Example Output

**Extracted JSON (from Genel Energy.pdf):**
```json
{
  "trades": [
    {
      "TradeID": 1,
      "ISIN": "NO0010894330",
      "Issuer": "Genel Energy Finance 4 Limited",
      "Maturity": "2025-10-14",
      "Notional": 3000000,
      "Coupon": 9.25,
      "Currency": "USD",
      "SettlementDate": "2020-10-14",
      "DayCountFraction": "30/360",
      "InterestPaymentDate": "2021-04-14",
      "IssueDate": "2020-10-14",
      "IssueAmount": 300000000,
      "IssuePrice": 97,
      "NominalAmountPerBond": 2000,
      "InterestPaymentFrequency": "Semi-annual",
      "BusinessDayConvention": "Unadjusted",
      "BusinessDayLocation": ["Oslo", "New York"],
      "AmortizationType": "Bullet",
      "MinimumSubscription": 200000,
      "Parent": "Genel Energy plc"
    }
  ]
}
```
![Validation Excel Screenshot](/media/yogi/WORK_SPACE/Git Codes /Data-Science-GenAI-Solutions/Insurance-Finance-Doc-Processing (LLM - RAG Pipline)-BNP/Pasted image.png)

---

## ✅ Next Steps

- Support **multi-trade documents** (batch extraction).  
- Extend schema for **insurance & other financial contracts**.  
- Integrate storage with **MongoDB & S3**.  
- Add API layer with **FastAPI**.  

---

## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: India 
