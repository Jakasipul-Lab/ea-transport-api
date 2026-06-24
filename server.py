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

from fastapi import Query

@app.get("/local")
async def handle_search(q: str = Query(None)):
    # 'q' captures whatever comes after '?q=' in your URL
    if not q:
        return FileResponse(os.path.join(BASE_DIR, "index.html"))
    
    # Logic to return a specific file based on the search term
    if "safari" in q.lower():
        return FileResponse(os.path.join(BASE_DIR, "safari.html"))
    
    # Fallback if the search term doesn't match a specific file
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    return RedirectResponse("/")

from fastapi import Query

@app.get("/api/search")
async def search_tours(q: str = Query(..., description="The search term")):
    # For now, let's just return the search term to verify the connection works
    return {"message": f"You searched for: {q}", "results": []}

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
