import os
import uvicorn
import datetime
from fastapi import FastAPI, RedirectResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow browser connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Logging Logic
def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

# 2. Tracking Route
@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    # Redirect to home after logging
    return RedirectResponse("/")

# 3. Serving Files (The clean "Catch-All")
@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    if not path or path == "/":
        path = "index.html"
    
    # Ensure it looks for the file in the same folder as main.py
    file_path = os.path.join(BASE_DIR, path)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    # Final fallback
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# 4. Server Startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
