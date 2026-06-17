import os
import json
import hashlib
import hmac
import psycopg2
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Executive Hub")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- SECURE ENGINE ---
def generate_token(agency_id, total):
    secret_salt = os.getenv("SECRET_SALT", "kisumu_hq_secure_key_2026")
    payload = f"{agency_id}|{total}"
    return hmac.new(secret_salt.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("RAILWAY_DB_URL")
    if not db_url: return None
    return psycopg2.connect(db_url)

# Initialize database tables on startup
@app.on_event("startup")
def startup_db():
    conn = get_db()
    if not conn: return
    try:
        cur = conn.cursor()
        # Tier 1 & Core Bookings
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                booking_id VARCHAR(50) UNIQUE NOT NULL,
                passenger_name VARCHAR(100) NOT NULL,
                route_id VARCHAR(50) NOT NULL,
                operator VARCHAR(100) NOT NULL,
                safariroute_code VARCHAR(50) UNIQUE NOT NULL,
                status VARCHAR(20) DEFAULT 'ISSUED',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # TIER 2: MARKETPLACE ESCROW & QR
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customer_bookings_escrow_qr (
                booking_reference VARCHAR(50) PRIMARY KEY,
                listing_id VARCHAR(50),
                customer_identifier VARCHAR(100),
                gross_payment_usd NUMERIC(10, 2),
                commission_earned_usd NUMERIC(10, 2),
                vendor_payout_held_usd NUMERIC(10, 2),
                payment_escrow_status VARCHAR(50) DEFAULT 'HELD',
                qr_security_token VARCHAR(255) UNIQUE,
                qr_scan_status VARCHAR(50) DEFAULT 'UNSCANNED'
            )
        """)
        conn.commit()
        cur.close(); conn.close()
        print("DEBUG: Multi-tier tables initialized successfully.")
    except Exception as e:
        print(f"DB Setup Error: {e}")

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/about", response_class=HTMLResponse)
def about(): return FileResponse("about.html")

@app.get("/help", response_class=HTMLResponse)
def help_page(): return FileResponse("help.html")

@app.get("/support", response_class=HTMLResponse)
def support(): return FileResponse("support.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_hub(): return FileResponse("admin.html")

@app.get("/verify", response_class=HTMLResponse)
def verify(): return FileResponse("verify.html")

# --- TICKET ISSUANCE ---
class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    total = int(request.base_price * 1.05)
    token = generate_token(agency_id, total)

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

    return {"status": "success", "code": agency_id, "total": total, "token": token}

@app.get("/api/admin/stats")
async def get_admin_stats():
    conn = get_db()
    if not conn:
        return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM bookings")
        total = cur.fetchone()[0]
        cur.execute("SELECT passenger_name, route_id, 'Official', booking_id, status FROM bookings ORDER BY created_at DESC LIMIT 10")
        rows = cur.fetchall()
        recent = [{"passenger": r[0], "route": r[1], "operator": r[2], "code": r[3], "status": r[4]} for r in rows]
        cur.close(); conn.close()
        return {"total_bookings": total, "total_commission": total * 2000 * 0.05, "recent_bookings": recent}
    except: return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)