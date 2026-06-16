import os
import json
import hashlib
import hmac
import psycopg2
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Executive Hub")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Secure Anti-Tamper Token Generator
def generate_token(agency_id, total):
    secret_salt = os.getenv("SECRET_SALT", "kisumu_hq_secure_key_2026")
    payload = f"{agency_id}|{total}"
    return hmac.new(secret_salt.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("RAILWAY_DB_URL")
    if not db_url: return None
    return psycopg2.connect(db_url)

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/about", response_class=HTMLResponse)
def about(): return FileResponse("about.html")

@app.get("/help", response_class=HTMLResponse)
def help(): return FileResponse("help.html")

@app.get("/support", response_class=HTMLResponse)
def support(): return FileResponse("support.html")

@app.get("/admin", response_class=HTMLResponse)
def admin(): return FileResponse("admin.html")

@app.get("/verify", response_class=HTMLResponse)
def verify(): return FileResponse("verify.html")

@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR-001", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR-001", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"},
        {"route_id": "U-BUS-001", "origin": "Kampala", "destination": "Gulu", "operator": "Global Coaches", "base_price": 30000, "currency": "UGX"}
    ]

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    total = int(request.base_price * 1.05)
    token = generate_token(agency_id, total)

    # Save to Neon if connected
    conn = get_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO bookings (booking_id, passenger_name, route_id, operator, safariroute_code, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (agency_id, request.passenger_name, request.route_id, "Official", agency_id, "PAID")
            )
            conn.commit()
            cur.close(); conn.close()
        except Exception as e: print(f"DB Error: {e}")

    return {"status": "success", "code": agency_id, "total": total, "security_token": token}

@app.get("/api/admin/stats")
async def get_admin_stats():
    conn = get_db()
    if not conn:
        return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}
    
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT passenger_name, route_id, 'Official', booking_id, status FROM bookings ORDER BY created_at DESC LIMIT 10")
    rows = cur.fetchall()
    recent = [{"passenger": r[0], "route": r[1], "operator": r[2], "code": r[3], "status": r[4]} for r in rows]
    
    cur.close(); conn.close()
    return {"total_bookings": total, "total_commission": total * 2000 * 0.05, "recent_bookings": recent}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)