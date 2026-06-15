import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Momentum Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
def home(): return FileResponse("index.html")

@app.get("/help", response_class=HTMLResponse)
def help_page(): return FileResponse("help.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(): return FileResponse("admin.html")

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
    # Calculate 5% Fee for revenue
    service_fee = int(request.base_price * 0.05)
    total_to_pay = request.base_price + service_fee
    
    # Generate SafariRoutes Code
    code = "SR-2026-" + str(int(datetime.now().timestamp()))[-6:].upper()
    
    return {
        "status": "success",
        "code": code,
        "base_price": request.base_price,
        "service_fee": service_fee,
        "total": total_to_pay
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)