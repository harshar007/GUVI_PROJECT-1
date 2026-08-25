import os
import socket
import logging
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st

# Suppress Streamlit runtime caching warnings when script is executed outside of Streamlit runtime
logging.getLogger("streamlit.runtime.caching.cache_data_api").setLevel(logging.ERROR)
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "cart2insights_db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "cleaned", "ecommerce.db"))

def _is_mysql_available(host, port, timeout=0.5):
    """Probes MySQL host:port to check if connection is available before trying SQLAlchemy connection."""
    try:
        target_host = "127.0.0.1" if host == "localhost" else host
        s = socket.create_connection((target_host, int(port)), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False

def get_db_engine():
    """
    Attempts connection to MySQL database if server port is open.
    If MySQL server is unavailable or fails, gracefully falls back to SQLite engine instantly.
    """
    if _is_mysql_available(MYSQL_HOST, MYSQL_PORT):
        mysql_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        try:
            engine = create_engine(mysql_uri, connect_args={"connect_timeout": 2})
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine, "MySQL"
        except Exception:
            pass

    # SQLite fallback engine with 30s timeout for concurrent process safety
    engine = create_engine(
        "sqlite://",
        creator=lambda: sqlite3.connect(SQLITE_DB_PATH, timeout=30.0, check_same_thread=False)
    )
    return engine, "SQLite"

@st.cache_data(ttl=3600)
def run_query(query_str, params=None):
    """
    Executes a SQL query string using cached SQLAlchemy engine.
    Returns result as a Pandas DataFrame.
    """
    engine, _ = get_db_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text(query_str), conn, params=params)
    return df

def get_db_tables():
    """
    Returns list of table names in the active database.
    """
    engine, db_type = get_db_engine()
    if db_type == "SQLite":
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    else:
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema='{MYSQL_DB}' ORDER BY table_name;"
    df = run_query(query)
    if not df.empty:
        col = df.columns[0]
        return df[col].tolist()
    return []

if __name__ == "__main__":
    print("==================================================")
    print("        Cart2Insights Database Utility Test        ")
    print("==================================================")
    engine, db_type = get_db_engine()
    print(f"[*] Engine Status: Connected to {db_type} Database")
    
    tables = get_db_tables()
    print(f"[*] Total Tables Found: {len(tables)}")
    for t in tables:
        print(f"    - {t}")
    
    print("\n[*] Executing Test Query ('SELECT 1'):")
    test_df = run_query("SELECT 1 AS status_check")
    print(test_df)
    print("==================================================")
