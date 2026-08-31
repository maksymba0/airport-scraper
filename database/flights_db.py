import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        ) 
        return connection
    except psycopg2.OperationalError as e:
        print("\n--- NEW DECODED ERROR ---")
        try:
            raw_bytes = e.args
            if isinstance(raw_bytes, str):
                raw_bytes = raw_bytes.encode('utf-8', errors='surrogateescape')
            print(raw_bytes.decode('cp1250', errors='replace'))
        except Exception:
            print(f"Raw error: {e}")
            return None
 

conn = get_db_connection()
 
