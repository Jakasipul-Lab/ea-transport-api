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

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("RAILWAY_DB_URL") or os.getenv("DATA_URL")
    if not db_url: return None
    try:
        return psycopg2.connect(db_url)
    except Exception as e:
        print(f"DEBUG: DB Connection attempt failed: {e}")
        return None

# --- ROBUST MIGRATION RUNNER ---
def run_migrations():
    conn = get_db()
    if not conn: 
        print("DEBUG: Database offline, skipping migrations.")
        return
    try:
        cur = conn.cursor()
        # Check if migration V1 was applied
        cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'schema_migrations')")
        if not cur.fetchone()[0]:
            print("DEBUG: Applying Initial Schema...")
            migration_path = os.path.join(os.path.dirname(__file__), "migrations", "V1__init_schema.sql")
            if os.path.exists(migration_path):
                with open(migration_path, "r") as f:
                    cur.execute(f.read())
                cur.execute("INSERT INTO schema_migrations (version) VALUES (1)")
                conn.commit()
                print("DEBUG: Schema V1 applied successfully.")
        cur.close(); conn.close()
    except Exception as e:
        print(f"DEBUG: Migration process skipped due to: {e}")

@app.on_event("startup")
def on_startup():
    # Fail-safe startup
    try:
        run_migrations()
    except: pass

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

class BookingRequest(BaseModel):
    route_id: str
    passenger_name: str
    base_price: int

@app.post("/api/book")
async def book_route(request: BookingRequest):
    agency_id = "SR-" + str(int(datetime.now().timestamp()))[-6:].upper()
    return {"status": "success", "code": agency_id, "total": int(request.base_price * 1.05)}

@app.get("/api/admin/stats")
async def get_stats():
    return {"total_bookings": 0, "total_commission": 0, "recent_bookings": []}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)