from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
import dj_database_url

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Helper
def get_db_connection():
    try:
        # Railway provides DATABASE_URL automatically
        db_config = dj_database_url.config(default=os.getenv("DATABASE_URL"))
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "East African Transport API - Live",
        "database": "Checking..."
    }

@app.get("/db-test")
def test_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "connected", "message": "Successfully reached Postgres!"}
    return {"status": "error", "message": "Could not reach database."}

if __name__ == "__main__":
    import uvicorn
    # Use the dynamic Railway port
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
