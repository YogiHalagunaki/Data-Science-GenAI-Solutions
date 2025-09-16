import pandas as pd
import sqlite3
from utils import custom_logger as clogs
from utils.db_connect import get_db_path

def execute_sql(query: str) -> pd.DataFrame:
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT statements are allowed")

    conn = sqlite3.connect(get_db_path())
    clogs.get_logger(f"sqlite3 conn ::::::{conn}")
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()
