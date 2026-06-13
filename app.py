import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

try:
    from safariroute.src.generator import generate_safariroute_code
    from safariroute.src.database import save_booking, setup_database, get_connection
    MODULES_OK = True
except Exception: MODULES_OK = False

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_db():
    if os.getenv("RAILWAY_DB_URL") and MODULES_OK:
        try: setup_database()
        except: pass

@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/about", response_class=HTMLResponse)
def about(): return FileResponse("about.html")

@app.get("/verify", response_class=HTMLResponse)
def verify_page(): return FileResponse("verify.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(): return FileResponse("admin.html")

@app.get("/api/routes")
def get_routes():
    all_routes = []
    route_files = ["safariroute/data/routes/kenya_sgr.json","safariroute/data/routes/tanzania_sgr.json","safariroute/data/routes/east_africa_buses.json","safariroute/data/routes/uganda_buses.json"]
    for f in route_files:
        if os.path.exists(f):
            with open(f, "r") as file: all_routes.extend(json.load(file))
    return all_routes

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)