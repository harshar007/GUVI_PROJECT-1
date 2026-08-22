import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "cart2insights_db")

SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "ecommerce.db")

@st.cache_resource
def get_db_engine():
    """
    Attempts connection to MySQL database.
    If MySQL server is unavailable or fails, gracefully falls back to SQLite engine.
    """
    mysql_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    try:
        engine = create_engine(mysql_uri)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine, "MySQL"
    except Exception:
        # SQLite fallback engine
        sqlite_abs_path = os.path.abspath(SQLITE_DB_PATH)
        sqlite_uri = f"sqlite:///{sqlite_abs_path}"
        engine = create_engine(sqlite_uri)
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
