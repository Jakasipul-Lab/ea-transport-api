from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url)

@app.get("/")
def root():
    return {"message": "API is Live"}

@app.get("/stations")
def get_stations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM stations;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.get("/todos")
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM todos;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
