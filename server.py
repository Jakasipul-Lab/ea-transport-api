@app.get("/search")
async def process_search(origin: str, destination: str):
    # This logs the search so you can see it in leads.txt or console
    print(f"Search request: From {origin} to {destination}")
    
    # Logic to return a specific result page
    # For example, if destination is Mombasa, serve a specific file:
    if "mombasa" in destination.lower():
        return FileResponse(os.path.join(BASE_DIR, "mombasa.html"))
        
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

import os
import uvicorn
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

# Place this BEFORE the serve_files route
@app.get("/{page_name}")
async def serve_specific_page(page_name: str):
    file_path = os.path.join(BASE_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    # Fallback to index if not found
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    return RedirectResponse("/")

@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    if not path or path == "/":
        path = "index.html"
    file_path = os.path.join(BASE_DIR, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
