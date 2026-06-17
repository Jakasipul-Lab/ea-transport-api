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

app = FastAPI(title="EA SafariRoutes Master Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("RAILWAY_DB_URL") or os.getenv("DATA_URL")
    if not db_url: return None
    return psycopg2.connect(db_url)

# --- MIGRATION RUNNER ---
def run_migrations():
    conn = get_db()
    if not conn: return
    try:
        cur = conn.cursor()
        # Check if migration V1 was applied
        cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'schema_migrations')")
        if not cur.fetchone()[0]:
            print("DEBUG: Running V1 Migration...")
            with open("migrations/V1__init_schema.sql", "r") as f:
                cur.execute(f.read())
            cur.execute("INSERT INTO schema_migrations (version) VALUES (1)")
            conn.commit()
        cur.close(); conn.close()
    except Exception as e: print(f"Migration Error: {e}")

@app.on_event("startup")
def on_startup():
    run_migrations()

@app.get("/", response_class=HTMLResponse) def home(): return FileResponse("index.html")
@app.get("/about", response_class=HTMLResponse) def about(): return FileResponse("about.html")
@app.get("/help", response_class=HTMLResponse) def help_p(): return FileResponse("help.html")
@app.get("/support", response_class=HTMLResponse) def support(): return FileResponse("support.html")
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("admin.html")

@app.get("/api/routes")
def get_routes():
    return [
        {"route_id": "K-SGR", "origin": "Nairobi", "destination": "Mombasa", "operator": "Madaraka Express", "base_price": 1000, "currency": "KES"},
        {"route_id": "T-SGR", "origin": "Dar es Salaam", "destination": "Dodoma", "operator": "TRC", "base_price": 15000, "currency": "TZS"}
    ]

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    total = int(request.base_price * 1.05)
    return {"status": "success", "code": agency_id, "total": total}

@app.get("/api/admin/stats")
async def get_stats():
    return {"total_bookings": 1482, "total_commission": 74100, "recent_bookings": []}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)