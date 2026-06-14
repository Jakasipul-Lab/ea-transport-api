import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

# SafariRoutes internal modules
try:
    from safariroute.src.generator import generate_safariroute_code
    from safariroute.src.database import save_booking, setup_database, get_connection
    MODULES_OK = True
except Exception:
    MODULES_OK = False

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_db():
    db_url = os.getenv("RAILWAY_DB_URL") or os.getenv("NEON_DB_URL")
    if db_url and MODULES_OK:
        try: setup_database()
        except: pass

@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/help", response_class=HTMLResponse)
def help_page(): return FileResponse("help.html")

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

@app.post("/api/book")
async def book_route(request: BookingRequest):
    code = generate_safariroute_code(request.route_id) if MODULES_OK else "SR-OFFLINE"
    booking = {"booking_id": f"BK-{int(datetime.now().timestamp())}", "passenger_name": request.passenger_name, "route_id": request.route_id, "operator": request.operator, "safariroute_code": code, "status": "ISSUED"}
    db_url = os.getenv("RAILWAY_DB_URL") or os.getenv("NEON_DB_URL")
    if db_url and MODULES_OK:
        try: save_booking(booking)
        except: pass
    return {"status": "success", "code": code}

class BookingRequest(BaseModel):
    route_id: str
    operator: str
    passenger_name: str

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)