import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

@app.get("/{path:path}", response_class=HTMLResponse)
def catch_all(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse("index.html")
# --- ADD-ON: Transport Search Feature ---
from pydantic import BaseModel
import databases

db = databases.Database(os.environ.get("NEON_URL"))

class SearchRequest(BaseModel):
    destination: str

@app.post("/api/search")
async def search_transport(req: SearchRequest):
    await db.connect()
    query = "SELECT * FROM transport_options WHERE destination = :dest"
    results = await db.fetch_all(query=query, values={"dest": req.destination})
    await db.disconnect()
    return [dict(row) for row in results]
# --- END ADD-ON ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
