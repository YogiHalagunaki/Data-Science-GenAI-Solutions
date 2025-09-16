# Text-to-SQL FastAPI Project

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
text_to_sql_fastapi/
├── README.md
├── requirements.txt
├── .env.example
├── data/                 # put provided CSVs here (not included)
├── scripts/
│   └── ingest_data.py    # loads CSVs into SQLite
├── app/
│   ├── main.py           # FastAPI app
│   ├── db.py             # SQLite connection and schema code
│   ├── nl2sql.py         # NL -> SQL component
│   ├── sql_exec.py       # executes SQL queries
│   └── summarize.py      # converts SQL result -> NL
└── tests/
    └── test_endpoints.py # pytest test cases
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
DB_PATH=./database.db
OPENAI_API_KEY=your_openai_api_key_here  # optional
HOST=127.0.0.1
PORT=8000
```

3. Place your CSV files into the `data/` directory.
4. Run the ingestion script:

```bash
python scripts/ingest_data.py
```

This creates `database.db` with tables named after the CSV files.

---

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will be available at:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### `GET /schema`

Returns the database schema (tables and columns).

**Example:**

```bash
curl http://127.0.0.1:8000/schema
```

Response:

```json
{
  "schema": {
    "employees": ["id (INTEGER)", "name (TEXT)", "salary (REAL)"]
  }
}
```

### `POST /query`

Accepts a natural language question and returns SQL, answer, and sample rows.

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/query \
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

```bash
pytest -v
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
