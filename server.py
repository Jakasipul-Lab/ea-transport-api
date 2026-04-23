from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database Connection Tool
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    # This fix is CRITICAL for Railway/Postgres compatibility
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url)

@app.get("/")
def read_root():
    return {"status": "API is Online", "docs": "/docs", "message": "System Revived"}

@app.get("/health")
def check_health():
    return {"status": "healthy"}

@app.get("/stations")
def get_stations():
    conn = None
    try:
        conn = get_db_connection()
        # Using 'with' ensures the cursor closes even if there is an error
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM stations;")
            return cursor.fetchall()
    except Exception as e:
        return {"error": "Database error", "details": str(e)}
    finally:
        if conn:
            conn.close()

@app.get("/todos")
def get_todos():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM todos;")
            return cursor.fetchall()
    except Exception as e:
        return {"error": "Database error", "details": str(e)}
    finally:
        if conn:
            conn.close()
