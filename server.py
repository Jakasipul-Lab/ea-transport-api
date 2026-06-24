import os
import uvicorn
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# 1. Initialize app FIRST
app = FastAPI()

# 2. Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 3. Define routes
@app.get("/search")
async def handle_search(origin: str, destination: str):
    return {"status": "success", "from": origin, "to": destination}

@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    file_path = os.path.join(BASE_DIR, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# 4. Only start if run directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
