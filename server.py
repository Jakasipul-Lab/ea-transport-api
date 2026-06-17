import os
import json
import hashlib
import hmac
import psycopg2
from psycopg2 import pool
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Master Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- DATABASE CONNECTION (EXTREME COMPATIBILITY) ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DB_URL") or os.getenv("DATA_URL") or os.getenv("RAILWAY_DB_URL")

try:
    if DATABASE_URL:
        # Ensure the URL starts with postgresql:// (Fixes common Neon/Render strings)
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
        print("DEBUG: Database connection pool active.")
    else:
        db_pool = None
except Exception as e:
    print(f"DEBUG: Pool failed: {e}")
    db_pool = None

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse) def home(): return FileResponse("index.html")
@app.get("/about", response_class=HTMLResponse) def about(): return FileResponse("about.html")
@app.get("/help", response_class=HTMLResponse) def help_p(): return FileResponse("help.html")
@app.get("/support", response_class=HTMLResponse) def support(): return FileResponse("support.html")
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("admin.html")
@app.get("/verify", response_class=HTMLResponse) def verify(): return FileResponse("verify.html")

@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"},
        {"route_id": "U-BUS", "origin": "Kampala", "destination": "Gulu", "operator": "Global Coaches", "base_price": 30000, "currency": "UGX"}
    ]

@app.get("/api/admin/stats")
def admin_stats():
    return {"total_bookings": 1482, "total_commission": 74100, "recent_bookings": []}

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    
    if db_pool:
        try:
            conn = db_pool.getconn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO bookings (route_id, passenger_name, price, operator) VALUES (%s, %s, %s, %s)",
                (request.route_id, request.passenger_name, request.base_price, "Official Agent")
            )
            conn.commit()
            cur.close()
            db_pool.putconn(conn)
        except Exception as e:
            print(f"DB Error: {e}")

    return {"status": "success", "code": agency_id, "total": int(request.base_price * 1.05)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)