import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

@app.get("/local.html")
def local_page_html():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/local")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

BASE_DIR = os.path.dirname(__file__)

# --------------------------------------
# ✅ DATA (fallback database)
# --------------------------------------

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu", "shuttle"], "title": "🚐 Local Shuttle & Matatu", "desc": "Daily routes across towns.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train Service", "desc": "Mombasa ↔ Nairobi tickets.", "price": "KES 1,500"},
    {"keywords": ["car", "taxi"], "title": "🚗 Car Hire Service", "desc": "Self-drive & chauffeur options.", "price": "KES 8,000/day"}
]

SAFARI_DATABASE = [
