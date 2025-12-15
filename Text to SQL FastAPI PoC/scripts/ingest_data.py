
import os
import sqlite3
import pandas as pd
from pathlib import Path

from app.utils import config
from app.utils import custom_logger as clogs

from dotenv import load_dotenv
load_dotenv()

DB_PATH = config.DB_PATH

DATA_DIR = Path("data")

def ingest_csvs_to_sqlite():
    
    if not DATA_DIR.exists():
        clogs.logging.info("")
        raise FileNotFoundError("data/ folder not found. Please add CSV files.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    clogs.get_logger(f"sqlite3 conn ::::::{conn}")
    clogs.get_logger(f"cursor::::::::::::{cursor}")

    for csv_file in DATA_DIR.glob("*.csv"):
        table_name = csv_file.stem.lower()
        print(f"[INFO] Processing {csv_file} -> table '{table_name}'")

        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"[INFO] Loaded {row_count} rows into {table_name}")

    conn.commit()
    conn.close()
    print(f"[INFO] Database created at {DB_PATH}")

if __name__ == "__main__":
    ingest_csvs_to_sqlite()
