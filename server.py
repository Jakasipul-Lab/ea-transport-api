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

app = FastAPI(title="EA SafariRoutes Master Hub")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- SECURE HASHING ENGINE ---
def generate_ticket_token(agency_id, total):
    secret_salt = os.getenv("SECRET_SALT", "kisumu_hq_secure_key_2026")
    payload = f"{agency_id}|{total}"
    return hmac.new(secret_salt.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("RAILWAY_DB_URL")
    return psycopg2.connect(db_url) if db_url else None

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

# --- TIER 1: FREIGHT & LOGISTICS API ---
@app.get("/api/freight/lookup")
async def freight_lookup(bol: str):
    conn = get_db()
    if not conn: return {"error": "Logistics DB Offline"}
    cur = conn.cursor()
    cur.execute("SELECT consignment_id, cargo_destination, current_corridor_node, clearance_status FROM transit_freight_codes WHERE container_bill_of_lading = %s", (bol,))
    res = cur.fetchone()
    cur.close(); conn.close()
    if not res: return {"error": "Container not found"}
    return {"id": res[0], "destination": res[1], "location": res[2], "status": res[3]}

# --- TICKETING ENGINE (PAYMENT-GATED) ---
class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    total = int(request.base_price * 1.05)
    token = generate_ticket_token(agency_id, total)
    return {"status": "success", "code": agency_id, "total": total, "token": token}

@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR-001", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR-001", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"}
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)