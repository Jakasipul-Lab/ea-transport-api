import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import databases

# Database connection URL
DATABASE_URL = os.environ.get("NEON_URL")

# Define the lifespan to handle database connection safely
# Place 'import os' at the very top of your server.py file

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB
    # Ensure this print is indented with 4 spaces to match the lines below
    print(f"DEBUG: DATABASE_URL is {os.environ.get('DATABASE_URL')}")
    
    database = databases.Database(DATABASE_URL)
    await database.connect()
    app.state.database = database
    yield
    # Shutdown: Disconnect from DB
    await database.disconnect()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    destination: str
    category: str = "tourist"  # This allows the search to handle different types

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

@app.get("/{path:path}", response_class=HTMLResponse)
def catch_all(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse("index.html")

@app.post("/api/search")
async def search_transport(req: SearchRequest):
    # This queries your existing table, filtering by both destination and category
    query = "SELECT * FROM transport_options WHERE destination = :dest AND category = :cat"
    results = await app.state.database.fetch_all(
        query=query, 
        values={"dest": req.destination, "cat": req.category}
    )
    return [dict(row) for row in results]
@app.get("/api/search")
def search(origin: str, destination: str, date: str):
    return [
        {
            "id": 1,
            "provider": "SGR",
            "price": 1000
        },
        {
            "id": 2,
            "provider": "EasyCoach",
            "price": 800
        }
    ]
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
