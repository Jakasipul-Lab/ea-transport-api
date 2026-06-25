import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

# --------------------------------------
# ✅ SMART DATA (expanded keywords)
# --------------------------------------

LOCAL_DATABASE = [
    {
        "keywords": ["bus", "matatu", "transport", "travel", "ride", "shuttle"],
        "title": "🚐 Local Shuttle & Matatu Transport",
        "desc": "Daily transport across cities and towns.",
        "price": "KES 1,200"
    },
    {
        "keywords": ["train", "sgr", "rail", "mombasa", "nairobi"],
        "title": "🚆 SGR Train Transport",
        "desc": "Nairobi ↔ Mombasa railway booking.",
        "price": "KES 1,500"
    },
    {
        "keywords": ["taxi", "car", "hire", "vehicle", "uber"],
        "title": "🚗 Taxi & Car Hire",
        "desc": "Affordable ride and car hire services.",
        "price": "KES 8,000/day"
    }
]

SAFARI_DATABASE = [
    {
        "keywords": ["mara", "safari", "kenya", "wildlife", "tour", "trip", "holiday"],
        "operator_id": "mara001",
        "title": "🦁 Masai Mara Safari",
        "desc": "3 Days Big Five safari experience.",
        "price": "$350",
        "dest": "mara"
    },
    {
        "keywords": ["zanzibar", "beach", "tanzania", "holiday", "island", "vacation"],
        "operator_id": "znz001",
