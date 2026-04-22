from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# 1. Load variables (Essential for Railway)
load_dotenv()

app = FastAPI(title="Transport API")

# 2. CORS (Essential for your Frontend to talk to this code)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Database Connection
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client.test
# 4. Data Models (Schemas)
class Station(BaseModel):
    name: str
    location: str

# 5. Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Transport API",
        "status": "Online",
        "available_endpoints": ["/stations", "/health"]
    }
@app.get("/")
async def root():
    return {"message": "Transport Backend is Live"}

@app.get("/health")
async def health():
    try:
        await client.admin.command('ping')
        return {"status": "online", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/stations")
async def get_stations():
    stations = await db.stations.find().to_list(100)
    return stations

# This part runs the server
if __name__ == "__main__":
    import uvicorn
    if __name__ == "__main__":
    import uvicorn
    import os
    # Railway tells the app which port to use via an 'environment variable'
    port = int(os.getenv("PORT", 8080))
    # '0.0.0.0' allows the app to accept outside traffic
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
