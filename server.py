import os
import json
import psycopg2
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="EA SafariRoutes Master Hub")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse) def home(): return FileResponse("index.html")
@app.get("/about", response_class=HTMLResponse) def about(): return FileResponse("about.html")
@app.get("/help", response_class=HTMLResponse) def help_p(): return FileResponse("help.html")
@app.get("/support", response_class=HTMLResponse) def support(): return FileResponse("support.html")
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("admin.html")
@app.get("/verify", response_class=HTMLResponse) def verify(): return FileResponse("verify.html")

# --- UNBREAKABLE ROUTES API ---
@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"},
        {"route_id": "U-BUS", "origin": "Kampala", "destination": "Gulu", "operator": "Global Coaches", "base_price": 30000, "currency": "UGX"}
    ]

@app.get("/api/admin/stats")
def admin_stats():
    return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    import time
    code = "SR-" + str(int(time.time()))[-6:].upper()
    return {"status": "success", "code": code}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)