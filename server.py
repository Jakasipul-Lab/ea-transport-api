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
async def process_search(origin: str, destination: str):
    # This logs the search to your terminal/logs so you can see it
    print(f"Search: {origin} to {destination}")
    
    # This serves your actual HTML file instead of the JSON text
    file_path = os.path.join(BASE_DIR, "results.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    # Fallback to index if results.html is missing
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    # Fix the path to point to your file
    file_path = os.path.join(BASE_DIR, path)
    
    # Only return the file if it actually exists AND is a file
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # If the file doesn't exist, return your main page
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# 4. Only start if run directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
