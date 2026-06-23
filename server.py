# REPLACE your current line with this block:
import os
from fastapi.staticfiles import StaticFiles

static_dir = os.path.join(os.getcwd(), "static")

if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"CRITICAL ERROR: Folder 'static' not found in: {os.getcwd()}")

# --- REPLACE YOUR CURRENT app.mount BLOCK WITH THIS ---
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Instead of crashing, we check if it exists first
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HEALTH CHECK (IMPORTANT)
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return FileResponse("frontend/index.html")
``
# ✅ CLICK LEAD (TRACK + REDIRECT)
@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    # placeholder logging
    print(f"Lead: {destination} - {service_type}")

    return RedirectResponse("/")

from fastapi.responses import FileResponse
import os

@app.get("/api/transport")
async def get_transport_data():
    return [
        {"type": "bus", "price": 1200, "route": "Nairobi → Mombasa"},
        {"type": "train", "price": 1500, "route": "Nairobi → Kisumu"},
    ]

@app.get("/{path:path}")
def catch_all(path: str):
    return FileResponse(os.path.join(BASE_DIR, "osare.html"))
    file_path = os.path.join(BASE_DIR, path + ".html")

import os
from fastapi.staticfiles import StaticFiles

# --- REPLACE YOUR MOUNT LINE WITH THIS ---
# Force the app to look for 'static' in the current working directory
static_dir = os.path.join(os.getcwd(), "static")

if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    # This prevents the crash. You will see this in the logs if it's missing.
    print(f"DEBUG: Static folder not found at {static_dir}. Server starting anyway.")

app = FastAPI()

# --- THE CRASH-PROOF MOUNT ---
# This ensures that if the folder is missing, your server starts anyway
# rather than throwing a RuntimeError.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.get("/{path:path}")
def catch_all(path: str):
    return FileResponse(os.path.join(BASE_DIR, "osare.html"))
``
# --- REPLACE LINE 57 WITH THIS BLOCK ---
# This looks for a 'static' folder in the same place as your server script
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print(f"CRITICAL WARNING: The folder '{static_path}' does not exist. Skipping.")

    # ✅ fallback to your main UI
    return FileResponse(os.path.join(BASE_DIR, "osare.html"))

# Change line 57 to this:
import os
from fastapi.staticfiles import StaticFiles

# ... your other code ...

# REPLACE LINE 57 WITH THIS:
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"WARNING: Static directory not found at {static_dir}. Skipping.")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

import os
import datetime

def log_lead(destination, service_type):
    try:
        # Use a safe temporary path if DIRECTORY is not defined
        target_dir = os.environ.get("LOG_DIR", ".") 
        file_path = os.path.join(target_dir, "leads.txt")
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(file_path, "a") as f:
            f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")
    except Exception as e:
        # Instead of crashing, we print the error to the logs
        print(f"CRITICAL: Failed to write to log file: {e}")
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
    return FileResponse(os.path.join(DIRECTORY, "index.html")

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
    
@app.get("/{path:path}", response_class=FileResponse)
async def catch_all(path: str):

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if not path or path == "/":
        return FileResponse(os.path.join(base_dir, "index.html"))

    file_path = os.path.join(base_dir, path)

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return FileResponse(os.path.join(base_dir, "index.html"))
    # Otherwise fallback to index.html
    return FileResponse("index.html")
    
    # 1. First, perform your database operation
    results = await app.state.database.fetch_all(
        query=query,
        values={
            "dest": req.destination,
            "cat": req.category
        }
    )

    # 2. Check if you got results, if so, return them
    if results:
        return [dict(row) for row in results]

    # 3. If no results found, perform the fallback
    return FileResponse("index.html")

    return [dict(row) for row in results]

# @app.get starts at 0 spaces
@app.get("/api/stats")
# async def starts at 0 spaces
async def stats():
    # Everything inside MUST start at 4 spaces
    query = "SELECT COUNT(*) as total FROM transport_options"
    result = await app.state.database.fetch_one(query)
    
    # Don't forget to return something! 
    return {"total_transport_options": result["total"]}
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

# ✅ STATS API (for admin dashboard)
@app.get("/stats")
@app.get("/api/stats")
async def stats():
    # Everything here must be indented by exactly 4 spaces
    query = "SELECT COUNT(*) as total FROM transport_options"
    result = await app.state.database.fetch_one(query)
    
    # Return the data so the frontend can read it
    return {"total_transport_options": result["total"]}   
    return {"total_transport_options": result["total"]}
    
    def get_data_from_db():
        # Everything here is indented 8 spaces (4 for the parent + 4 for the child)
        pass 
    
    # Logic for stats() follows here, also at 4 spaces
    return {"status": "ok"}
# This line must be flush to the left (0 spaces)
print("Done") # If this line has 1 space in front of it, you get the error

def catch_all(path: str):
    print("Done")
def catch_all(path: str):
    print("Done")

    if os.path.exists(file_path):
        return FileResponse(file_path)

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return FileResponse(os.path.join(base_dir, "index.html"))
    results = db.execute("SELECT * FROM table")
    # This return must be indented relative to the 'def' line
    return [dict(row) for row in results]

from fastapi.responses import RedirectResponse

@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)

    return RedirectResponse("/")
``

Python
import os
import uvicorn

# ... rest of your code ...

if __name__ == "__main__":
    # Render provides a PORT environment variable. Default to 8000 if not set.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("my_feature_server:app", host="0.0.0.0", port=port)
