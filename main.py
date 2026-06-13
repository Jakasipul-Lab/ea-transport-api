import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

try:
    from safariroute.src.generator import generate_safariroute_code
    from safariroute.src.database import save_booking, setup_database, get_connection
    MODULES_OK = True
except Exception:
    MODULES_OK = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/about")
def about():
    return FileResponse("about.html")

@app.get("/verify")
def verify_page():
    return FileResponse("verify.html")

@app.get("/admin")
def admin_dashboard():
    return FileResponse("admin.html")

@app.get("/api/routes")
def get_routes():
    all_routes = []
    route_files = ["safariroute/data/routes/kenya_sgr.json","safariroute/data/routes/tanzania_sgr.json","safariroute/data/routes/east_africa_buses.json","safariroute/data/routes/uganda_buses.json"]
    for f in route_files:
        if os.path.exists(f):
            with open(f, "r") as file: all_routes.extend(json.load(file))
    return all_routes

if __name__ == "__main__":
    # RAILWAY CRITICAL: Must use 0.0.0.0 and dynamic PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")