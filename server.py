import os
import datetime
from fastapi import FastAPI, RedirectResponse
from fastapi.responses import FileResponse

app = FastAPI()

# EDIT THIS LINE: Put the full path to your folder here
# Example (Windows): "C:/Users/Name/Documents/osare_project"
# Example (Mac): "/Users/Name/Documents/osare_project"
DIRECTORY = "YOUR_FULL_PATH_HERE"

def log_lead(destination, service_type):
    file_path = os.path.join(DIRECTORY, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    partners = {
        "car_hire": "https://wa.me/2547XXXXXXXX",
        "safari": "https://wa.me/2547XXXXXXXX"
    }
    return RedirectResponse(partners.get(service_type, "/"))

@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    if path == "": path = "index.html"
    file_path = os.path.join(DIRECTORY, path)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(DIRECTORY, "index.html"))
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: You could add database connection code here later
    yield

app = FastAPI(lifespan=lifespan)

# 2. LOGGING ENGINE
def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

# 3. ROUTES
@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    
    # Update these numbers to your actual partner WhatsApp numbers
    partners = {
        "car_hire": "https://wa.me/2547XXXXXXXX",
        "safari": "https://wa.me/2547XXXXXXXX"
    }
    
    url = partners.get(service_type, "/")
    return RedirectResponse(url)

# 4. SERVE HTML (Catch-all)
@app.get("/{path:path}", response_class=FileResponse)
async def serve_files(path: str = ""):
    # If path is empty, serve index.html
    if not path:
        path = "index.html"
    
    # Ensure it ends with .html if not provided
    if not path.endswith(".html") and "." not in path:
        path += ".html"
        
    full_path = os.path.join(BASE_DIR, path)
    
    if os.path.exists(full_path):
        return FileResponse(full_path)
    
    return FileResponse(os.path.join(BASE_DIR, "index.html"))
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# ✅ APP
app = FastAPI(lifespan=lifespan)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
import datetime

import os

# Get the directory where server.py is actually saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_lead(destination, service_type):
    # This creates/opens leads.txt in the same folder as server.py
    file_path = os.path.join(BASE_DIR, "leads.txt")
    
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")
# ✅ REQUEST MODEL
class SearchRequest(BaseModel):
    destination: str
    category: str = "tourist"

# ✅ HOME
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

from fastapi import FastAPI, RedirectResponse
from fastapi.responses import FileResponse, HTMLResponse
import datetime
import os

app = FastAPI()

# 1. Logging Function
def log_lead(destination, service_type):
    with open("leads.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

# 2. Tracking Route (FastAPI style)
@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    
    partners = {
        "car_hire": "https://wa.me/2547XXXXXXXX",
        "safari": "https://wa.me/2547XXXXXXXX"
    }
    
    url = partners.get(service_type, "/")
    return RedirectResponse(url)

# 3. Serving HTML Files
@app.get("/{path:path}", response_class=FileResponse)
async def catch_all(path: str):
    # Default to index.html if path is empty
    if not path or path == "/":
        return FileResponse("index.html")
    
    # If the file exists, serve it
    if os.path.exists(path):
        return FileResponse(path)
    
    # Otherwise fallback
    return FileResponse("index.html")
    """

    results = await app.state.database.fetch_all(
        query=query,
        values={
            "dest": req.destination,
            "cat": req.category
        }
    )

    return [dict(row) for row in results]


# ✅ STATS API (for admin dashboard)
@app.get("/api/stats")
async def stats():
    query = "SELECT COUNT(*) as total FROM transport_options"
    result = await app.state.database.fetch_one(query)

    return {
        "total": result["total"] if result else 0
    }
    results = await app.state.database.fetch_all(
        query=query,
        values={
            "dest": req.destination,
            "cat": req.category
        }
    )

    return [dict(row) for row in results]

# ✅ START (for local run only)
if __name__ == "__main__":
    # ... all your routes and logic above ...

if __name__ == "__main__":
   # ... all your code ...

# Ensure 'app' is defined above this point!
app = FastAPI(lifespan=lifespan) 

#  Line 200 
def some_function():
This is a description of my function that I forgot to close!
    pass
    
# Line 207 (SyntaxError here) 
uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
