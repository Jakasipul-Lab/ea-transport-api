import os
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Get the directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Logging function
def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_path, "a") as f:
            f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Click lead tracking endpoint
@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    
    partners = {
        "car_hire": "https://wa.me/2547XXXXXXXX",
        "safari": "https://wa.me/2547XXXXXXXX"
    }
    
    url = partners.get(service_type, "/")
    return RedirectResponse(url)

# Transport API endpoint
@app.get("/api/transport")
async def get_transport_data():
    return [
        {"type": "bus", "price": 1200, "route": "Nairobi → Mombasa"},
        {"type": "train", "price": 1500, "route": "Nairobi → Kisumu"},
    ]

# Stats endpoint
@app.get("/api/stats")
async def stats():
    return {"status": "ok"}

# Catch-all route for serving HTML files
@app.get("/{path:path}")
async def serve_files(path: str = ""):
    if not path or path == "/":
        path = "index.html"
    
    if not path.endswith(".html") and "." not in path:
        path += ".html"
    
    file_path = os.path.join(BASE_DIR, path)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

