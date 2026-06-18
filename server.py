import os
import json
import psycopg2
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="OSARE Aggregator Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("DATA_URL")
    if not db_url: return None
    try: return psycopg2.connect(db_url)
    except: return None

# --- MIGRATION RUNNER ---
def run_migrations():
    conn = get_db()
    if not conn: return
    try:
        cur = conn.cursor()
        # Apply V1 and V2 migrations
        for v in ["V1__init_schema.sql", "V2__osare_aggregator.sql"]:
            path = os.path.join("migrations", v)
            if os.path.exists(path):
                with open(path, "r") as f: cur.execute(f.read())
        conn.commit()
        cur.close(); conn.close()
    except Exception as e: print(f"Migration Failed: {e}")

@app.on_event("startup")
def on_startup(): run_migrations()

@app.get("/", response_class=HTMLResponse) def home(): return FileResponse("index.html")
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("admin.html")

# --- AGGREGATOR API ---
@app.get("/api/search")
async def search_transit(origin: str, destination: str, date: str):
    # This will later query the scraper_cache table
    return [
        {"id":"SGR-1", "type":"SGR", "time":"08:00 AM", "price":1000, "status":"12 seats left", "tag":"FASTEST"},
        {"id":"BUS-1", "type":"Bus", "time":"07:30 AM", "price":850, "status":"Available", "tag":"CHEAPEST"}
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)