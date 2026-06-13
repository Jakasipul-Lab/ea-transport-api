import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel

# SafariRoutes internal modules
try:
    from safariroute.src.generator import generate_safariroute_code
    from safariroute.src.database import save_booking, setup_database, get_connection
    DB_AVAILABLE = True
except Exception as e:
    print(f"Warning: Internal modules not found correctly: {e}")
    DB_AVAILABLE = False

app = FastAPI(title="EA SafariRoutes API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fail-safe database initialization
@app.on_event("startup")
def startup_db():
    db_url = os.getenv("RAILWAY_DB_URL")
    print(f"DEBUG: Starting up with DB_URL: {'Found' if db_url else 'MISSING'}")
    if db_url and DB_AVAILABLE:
        try:
            setup_database()
            print("DEBUG: Database tables verified.")
        except Exception as e:
            print(f"DEBUG: Database setup failed but keeping app alive: {e}")

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

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    return FileResponse("admin.html")

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
    code = "ERROR" if not DB_AVAILABLE else generate_safariroute_code(request.route_id)
    booking = {
        "booking_id": f"BK-{int(datetime.now().timestamp())}",
        "passenger_name": request.passenger_name,
        "route_id": request.route_id,
        "operator": request.operator,
        "safariroute_code": code,
        "status": "ISSUED"
    }
    if os.getenv("RAILWAY_DB_URL") and DB_AVAILABLE:
        try:
            save_booking(booking)
        except Exception as e:
            print(f"Database Error: {e}")
    return {"status": "success", "code": code, "message": "Booking issued."}

@app.get("/api/admin/stats")
async def get_admin_stats():
    if not os.getenv("RAILWAY_DB_URL") or not DB_AVAILABLE:
        return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM bookings")
        total = cur.fetchone()[0]
        commission = total * 2000 * 0.05
        cur.execute("SELECT passenger_name, route_id, operator, safariroute_code, status FROM bookings ORDER BY created_at DESC LIMIT 10")
        rows = cur.fetchall()
        recent = [{"passenger": r[0], "route": r[1], "operator": r[2], "code": r[3], "status": r[4]} for r in rows]
        cur.close()
        conn.close()
        return {"total_bookings": total, "total_commission": commission, "recent_bookings": recent}
    except Exception as e:
        return {"error": str(e), "total_bookings": 0, "total_commission": 0, "recent_bookings": []}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"DEBUG: Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)