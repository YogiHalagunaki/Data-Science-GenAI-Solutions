# Text-to-SQL FastAPI PoC

This project implements a **Text-to-SQL API** using **FastAPI**. It allows you to ask questions in **natural language** and get answers from a SQLite database populated with CSV data.

---

## Features

* **Data ingestion**: Load CSV files into a SQLite database.
* **Schema inspection**: View database schema via API.
* **NL → SQL**: Convert natural language questions into SQL.
* **SQL execution**: Run queries safely (only `SELECT` allowed).
* **Summarization**: Convert SQL results into human-readable text.
* **API endpoints**: FastAPI-based REST API.
* **Testing**: Pytest-based test cases for endpoints.

---

## Project Structure

```
Text_to_SQL_FastAPI_PoC/
├── README.md                       # API blue print
├── start-server.sh                 # Fast API server starts on this script
├── requirements.txt                # API requirments as per requirment
├── Dockerfile                      # TO create docker container to run API on EKS/AKS
├── .env                            # required env var to run the Fast API locally
├── data/                           # put provided CSVs here (not included)
├── scripts/
│   └── ingest_data.py              # loads CSVs into SQLite
├── app/
|   ├── run.py                      # run the server of FastAPI app
│   ├── views.py                    # FastAPI app: API entry point
├── app/codes/
│   ├── nl_to_sql.py                # NL -> SQL component
│   ├── sql_execute.py              # executes SQL queries
│   └── sql_to_nl_summarize.py      # converts SQL result -> NL
├── app/utils/
│   ├── db_connect.py               # SQLite connection and schema code
|   ├── config.py                   # API config var 
|   ├── custom_logger.py            # user defined logging module
|   ├── fileconstant.py             # const. store or usefull abrivation
└── test/
    └── test_api_endpoints.py       # pytest test cases, to test the Fast API.
```

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:

* fastapi
* uvicorn
* pandas
* python-dotenv
* sqlite-utils
* sqlparse
* openai (optional)
* requests
* pytest
* httpx

---

## Setup

1. Clone the repository and navigate into it.
2. Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_PATH=./database.db # add absulate path of your database
OPENAI_API_KEY=your_openai_api_key_here  # optional
HOST=127.0.0.1
PORT=8000
```

3. Place your CSV files into the `data/` directory.
4. Run the ingestion script:

```bash
(venv) python3 scripts/ingest_data.py
```

This creates `database.db` with tables named after the CSV files.

---

## Running the API

Start the FastAPI server:

```bash
(venv) uvicorn app.run:app --reload
or 

(venv) python3 app/run.py   
```

The server will be available at:

* Swagger UI: [http://127.0.0.1:8000/Text_to_SQL/schema](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/Text_to_SQL/query](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### `GET /Text_to_SQL/schema`

Returns the database schema (tables and columns).

**Example:**

```bash
curl http://127.0.0.1:8000/Text_to_SQL/schema
```

Response:

```json
{
  "schema": {
    "employees": ["id (INTEGER)", "name (TEXT)", "salary (REAL)"]
  }
}
```

### `POST /Text_to_SQL/query`

Accepts a natural language question and returns SQL, answer, and sample rows.

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/Text_to_SQL/query \
     -H "Content-Type: application/json" \
     -d '{"question": "How many employees are there?"}'
```

**Response:**

```json
{
  "sql": "SELECT COUNT(*) FROM employees;",
  "answer": "The COUNT(*) is 42.",
  "rows": [{"COUNT(*)": 42}],
  "status": "ok"
}
```

---

## Testing

Run tests with:

#### 1. Create a virtual environment
```bash 
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```
#### 2. run test file
```bash 
(venv) python3 /Text_to_SQL_FastAPI_PoC/test/test_api_endpoints.py 

```
---

## Notes

* If `OPENAI_API_KEY` is set, the system will use OpenAI for SQL generation.
* Without an API key, the system uses a **rule-based fallback**.
* Only `SELECT` queries are allowed for safety.

---

## Next Steps

* Expand NL → SQL patterns for more complex queries.
* Add CI/CD pipeline with GitHub Actions.
* Support more databases (Postgres, MySQL).

---
## 🙋 Author

**Yogi Halagunaki**  
GitHub: [@YogiHalagunaki](https://github.com/YogiHalagunaki)  
Email: halagunakiyogi@gmil.com  
Location: Pune, India 
