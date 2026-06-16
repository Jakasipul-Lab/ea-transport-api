import os
import json
import hashlib
import hmac
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Momentum Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Secure Anti-Tamper Logic
def generate_validation_hash(agency_id, official_ref, amount):
    secret_salt = os.getenv("SECRET_SALT", "kisumu_hq_secure_key_2026")
    payload = f"{agency_id}|{official_ref}|{amount}"
    return hmac.new(secret_salt.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

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

@app.get("/verify", response_class=HTMLResponse)
def verify_p(): return FileResponse("verify.html")

@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR-001", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR-001", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"}
    ]

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int
    official_ref: str = "PENDING"

@app.post("/api/book")
async def book_route(request: BookingRequest):
    commission_rate = 0.05
    fee = int(request.base_price * commission_rate)
    total = request.base_price + fee
    agency_tx_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    
    # Generate anti-tamper token
    security_token = generate_validation_hash(agency_tx_id, request.official_ref, total)

    return {
        "status": "success",
        "code": agency_tx_id,
        "base_price": request.base_price,
        "service_fee": fee,
        "total": total,
        "security_token": security_token
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)