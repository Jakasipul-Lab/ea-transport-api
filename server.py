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
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB
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
    # Use the database instance from app.state
    query = "SELECT * FROM transport_options WHERE destination = :dest"
    results = await app.state.database.fetch_all(query=query, values={"dest": req.destination})
    return [dict(row) for row in results]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
