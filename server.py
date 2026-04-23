from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database Connection Tool
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url)

@app.get("/")
def read_root():
    return {"status": "API is Online", "docs": "/docs"}

@app.get("/health")
def check_health():
    return {"status": "healthy"}

@app.get("/stations")
def get_stations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM stations;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": "Database error", "details": str(e)}

@app.get("/todos")
def get_todos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM todos;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        return {"error": "Database error", "details": str(e)}
