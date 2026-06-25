import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

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
