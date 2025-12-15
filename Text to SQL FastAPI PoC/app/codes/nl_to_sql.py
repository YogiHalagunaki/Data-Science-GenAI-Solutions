import os
import re
import openai
from utils import db_connect as db
from utils import config
from utils import custom_logger as clogs

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = config.OPENAI_API_KEY

clogs.get_logger(f"OPENAI_API_KEY:::::::::::{OPENAI_API_KEY}")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def simple_rule_based(question: str) -> str:
    q = question.lower()
    schema = db.get_schema()
    table_names = list(schema.keys())

    # Try to detect table name
    table = None
    for t in table_names:
        if t in q:
            table = t
            break
    if not table and table_names:
        table = table_names[0]

    if "count" in q or "how many" in q:
        return f"SELECT COUNT(*) FROM {table};"
    if "all" in q or "list" in q:
        return f"SELECT * FROM {table} LIMIT 20;"
    if "average" in q or "mean" in q:
        for col in schema.get(table, []):
            if "int" in col or "real" in col or "num" in col:
                colname = col.split(" ")[0]
                return f"SELECT AVG({colname}) FROM {table};"

    # default fallback
    return f"SELECT * FROM {table} LIMIT 10;"

def openai_generate(question: str) -> str:
    schema = db.get_schema()
    schema_text = "\n".join([f"{t}: {cols}" for t, cols in schema.items()])

    prompt = f"""
    You are a Text-to-SQL assistant. Convert the natural language question into a valid SQLite SELECT query.

    Schema:
    {schema_text}

    Question: {question}
    SQL:
    """
    clogs.get_logger(f"schema_text {schema_text}:::::::::prompt ::::::{prompt}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=5
    )
    sql_query = response.choices[0].text.strip()
    return sql_query

def convert_question_to_sql(question: str) -> str:
    clogs.logging.info("")
    
    if OPENAI_API_KEY:
        try:
            return openai_generate(question)
        except Exception:
            return simple_rule_based(question)
    else:
        return simple_rule_based(question)
