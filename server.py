from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# 1. THE CONNECTION TOOL (Must be at the top)
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    # This fix ensures Railway's postgres:// string works with Python
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url)

# 2. ROOT & HEALTH
@app.get("/")
def read_root():
    return {"status": "API is online", "docs": "/docs"}

@app.get("/health")
def check_health():
    return {"status": "healthy"}

# 3. STATIONS ENDPOINT
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
        return {"error": "Stations table issue", "details": str(e)}

# 4. TODOS ENDPOINT
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
        return {"error": "Todos table issue", "details": str(e)}
