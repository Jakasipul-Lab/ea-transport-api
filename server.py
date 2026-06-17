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

app = FastAPI(title="EA SafariRoutes Master Momentum Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- SECURE ENGINE ---
def generate_token(agency_id, total):
    secret_salt = os.getenv("SECRET_SALT", "kisumu_hq_secure_key_2026")
    payload = f"{agency_id}|{total}"
    return hmac.new(secret_salt.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

def get_db():
    db_url = os.getenv("NEON_DB_URL")
    if not db_url: return None
    return psycopg2.connect(db_url)

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/about", response_class=HTMLResponse)
def about_p(): return FileResponse("about.html")

@app.get("/help", response_class=HTMLResponse)
def help_p(): return FileResponse("help.html")

@app.get("/support", response_class=HTMLResponse)
def support_p(): return FileResponse("support.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_p(): return FileResponse("admin.html")

# --- TIER 1: LOGISTICS API ---
@app.get("/api/freight/lookup")
async def freight_lookup(bol: str):
    conn = get_db()
    if not conn: return {"error": "Logistics Server Offline"}
    cur = conn.cursor()
    cur.execute("SELECT consignment_id, current_corridor_node, clearance_status FROM transit_freight_codes WHERE container_bill_of_lading = %s", (bol,))
    res = cur.fetchone()
    cur.close(); conn.close()
    if not res: return {"error": "RECTS Code Not Found"}
    return {"consignment_id": res[0], "node": res[1], "status": res[2]}

# --- TIER 2: AVIATION MARKETPLACE ---
@app.post("/api/marketplace/book")
async def aviation_book(request: Request):
    data = await request.json()
    gross = data.get('rate', 0) * data.get('days', 1)
    commission = gross * 0.10 
    return {"gross_total_usd": gross, "agency_commission": commission, "operator_settlement": gross - commission}

# --- TICKETING ENGINE ---
class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int
    official_ref: str = "PENDING"

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    total = int(request.base_price * 1.05)
    token = generate_token(agency_id, total)
    return {"status": "success", "code": agency_id, "total_to_pay": total, "secure_token": token}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)