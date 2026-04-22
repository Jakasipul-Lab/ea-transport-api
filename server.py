from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
# This is the change:
import psycopg2

# Load environment variables
load_dotenv()

app = FastAPI()

# Postgres connection variable from Railway
DATABASE_URL = os.getenv("DATABASE_URL")

@app.on_event("startup")
async def startup_db():
    print("Starting up... Connecting to Railway Postgres")

@app.on_event("shutdown")
async def shutdown_db():
    print("Shutting down...")

# CORS middleware to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "East African Transport API", "database": "PostgreSQL"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# THIS PART MUST BE AT THE FAR LEFT (NO SPACES)
if __name__ == "__main__":
    import uvicorn
    # Railway sets the PORT automatically; this line reads it correctly
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
