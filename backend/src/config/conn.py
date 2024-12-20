from sqlalchemy import create_engine
from psycopg import Connection
from src.constants import Constant
from langgraph.checkpoint.postgres import PostgresSaver
from urllib.parse import quote
POSTGRES_CONFIG = Constant.POSTGRES_CONFIG
DB_URI = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"
print(DB_URI)

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

def create_connection():
    conn = Connection.connect(DB_URI, **connection_kwargs)
    return conn



def postgres_checkpointer():
    conn = create_connection()
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()
    return checkpointer
