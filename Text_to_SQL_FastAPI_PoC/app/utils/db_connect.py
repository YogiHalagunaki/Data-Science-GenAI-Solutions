import os
import sqlite3
from dotenv import load_dotenv
from utils import custom_logger as clogs
from utils import config

load_dotenv()

DB_PATH = config.DB_PATH

clogs.get_logger(f"DB_PATH:::::::::::{DB_PATH}")

def get_db_path():
    return DB_PATH

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def get_schema():
    conn = create_connection()
    cursor = conn.cursor()
    clogs.get_logger(f"cursor:::::::::::::{cursor}")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = [col[1] + " (" + col[2] + ")" for col in columns]

    conn.close()
    return schema
