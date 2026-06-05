import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel

# Safariroute internal modules
from safariroute.src.generator import generate_safariroute_code
from safariroute.src.database import save_booking, setup_database, get_connection

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_db():
    if os.getenv("RAILWAY_DB_URL"):
        setup_database()

# --- MODELS ---
class BookingRequest(BaseModel):
    route_id: str
    operator: str
    passenger_name: str

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

@app.get("/about", response_class=HTMLResponse)
def about():
    return FileResponse("about.html")

@app.get("/verify", response_class=HTMLResponse)
def verify_page():
    return FileResponse("verify.html")

@app.get("/api/routes")
def get_routes():
    all_routes = []
    route_files = [
        "safariroute/data/routes/kenya_sgr.json",
        "safariroute/data/routes/tanzania_sgr.json",
        "safariroute/data/routes/east_africa_buses.json",
        "safariroute/data/routes/uganda_buses.json"
    ]
    for f in route_files:
        if os.path.exists(f):
            with open(f, "r") as file:
                all_routes.extend(json.load(file))
    return all_routes

@app.post("/api/book")
async def book_route(request: BookingRequest):
    code = generate_safariroute_code(request.route_id)
    booking = {
        "booking_id": f"BK-{int(datetime.now().timestamp())}",
        "passenger_name": request.passenger_name,
        "route_id": request.route_id,
        "operator": request.operator,
        "safariroute_code": code,
        "status": "ISSUED"
    }
    if os.getenv("RAILWAY_DB_URL"):
        try:
            save_booking(booking)
        except Exception as e:
            print(f"Database Error: {e}")
    return {"status": "success", "code": code, "message": "Booking issued."}

@app.get("/api/verify/{code}")
async def verify_code(code: str):
    if not os.getenv("RAILWAY_DB_URL"):
        return {"status": "unknown", "message": "Database not connected"}
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT passenger_name, route_id, operator, status, created_at FROM bookings WHERE safariroute_code = %s", (code,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return {
                "status": "valid",
                "passenger": result[0],
                "route": result[1],
                "operator": result[2],
                "booking_status": result[3],
                "issued_at": result[4].isoformat()
            }
        else:
            return {"status": "invalid", "message": "Code not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}