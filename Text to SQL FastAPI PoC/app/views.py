import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils import db_connect as db
from codes import nl_to_sql
from codes import sql_execute as sql_exec
from codes import sql_to_nl_summarize as summarize
from utils import custom_logger as clogs

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Text-to-SQL API", description="Ask questions in NL, get answers from DB")

clogs.get_logger(f"App :::::::::{app}")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    answer: str
    rows: list
    status: str

@app.get("/Text_to_SQL/schema")
def get_schema():
    try:
        schema = db.get_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/Text_to_SQL/query", response_model=QueryResponse)
def run_query(req: QueryRequest):
    
    question = req.question
    
    try:
        sql_query = nl_to_sql.convert_question_to_sql(question)
        if not sql_query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed")

        df = sql_exec.execute_sql(sql_query)
        answer = summarize.dataframe_to_text(df)

        return QueryResponse(
            sql=sql_query,
            answer=answer,
            rows=df.head(10).to_dict(orient="records"),
            status="ok"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")
