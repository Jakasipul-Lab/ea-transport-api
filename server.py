import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

def log_lead(destination, service_type):
    with open("leads.txt", "a") as f:
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
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
