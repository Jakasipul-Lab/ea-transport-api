import os
import json
import hashlib
import hmac
import psycopg2
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

app = FastAPI(title="OSARE Transit API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- DATABASE CONNECTION ---
def get_db():
    db_url = os.getenv("NEON_DB_URL") or os.getenv("DATA_URL")
    if not db_url: return None
    try: return psycopg2.connect(db_url)
    except: return None

# --- PAGE ROUTES ---
@app.get("/", response_class=HTMLResponse) def home(): return FileResponse("index.html")
@app.get("/about", response_class=HTMLResponse) def about(): return FileResponse("about.html")
@app.get("/help", response_class=HTMLResponse) def help_p(): return FileResponse("help.html")
@app.get("/support", response_class=HTMLResponse) def support(): return FileResponse("support.html")
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("admin.html")

# --- TIER 1: FREIGHT API ---
@app.get("/api/freight/lookup")
async def freight_lookup(bol: str):
    return {"consignment_id": "EA-FR-1001", "status": "IN_TRANSIT", "node": "MALABA_OSBP"}

# --- TIER 2: AVIATION API ---
@app.post("/api/marketplace/book")
async def aviation_book(request: Request):
    data = await request.json()
    gross = data.get('rate', 1500) * data.get('days', 1)
    commission = gross * 0.10
    return {"total_usd": gross, "agency_cut": commission, "operator_payout": gross - commission}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)