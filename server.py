from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

import psycopg2
import dj_database_url

# 1. Load Environment Variables
load_dotenv()

app = FastAPI()

# 2. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Database Connection Logic
def get_db_connection():
    # Railway automatically provides the DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(db_url)

@app.get("/")
def root():
    return {"status": "Online", "message": "East African Transport API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# 4. The "Railway Port" Fix
if __name__ == "__main__":
    import uvicorn
    # This line is why Health Checks usually fail—it MUST use os.getenv("PORT")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
