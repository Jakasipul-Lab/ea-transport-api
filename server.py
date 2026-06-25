import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Synology!"}

# --------------------------------------
# ✅ DATA (simple + reliable)
# --------------------------------------

LOCAL_DATABASE = [
    {
        "keywords": ["bus", "matatu"],
        "title": "🚌 Bus & Matatu Transport",
        "desc": "Daily routes across towns and cities.",
        "price": "KES 1,200"
    },
    {
        "keywords": ["train", "sgr"],
        "title": "🚆 SGR Train",
        "desc": "Nairobi ↔ Mombasa transport.",
        "price": "KES 1,500"
    },
    {
        "keywords": ["taxi", "car"],
        "title": "🚗 Taxi / Car Hire",
        "desc": "Comfortable and reliable rides.",
        "price": "KES 8,000/day"
    }
]

SAFARI_DATABASE = [
    {
        "keywords": ["mara"],
        "operator_id": "mara001",
        "title": "🦁 Masai Mara Safari",
        "desc": "3 Days Big Five experience.",
        "price": "$350",
        "dest": "mara"
    },
    {
        "keywords": ["zanzibar"],
        "operator_id": "znz001",
        "title": "🏖️ Zanzibar Beach Holiday",
        "desc": "4 Days beach package.",
        "price": "$490",
        "dest": "zanzibar"
    },
    {
        "keywords": ["serengeti"],
        "operator_id": "ser001",
        "title": "🐆 Serengeti Safari",
        "desc": "Migration wildlife experience.",
        "price": "$750",
        "dest": "serengeti"
    }
]

# --------------------------------------
# ✅ PAGES
# --------------------------------------

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
@app.get("/local.html")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
@app.get("/safari.html")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.get("/about")
def about_page():
    return FileResponse(os.path.join(BASE_DIR, "about.html"))

# --------------------------------------
# ✅ LOCAL SEARCH (simple + guided)
# --------------------------------------

@app.get("/search/local")
def search_local(q: str = ""):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []

    for item in LOCAL_DATABASE:
        # ✅ match OR show all if no query
        if not query or any(k in query for k in item["keywords"]):
            results.append(f"""
            <div style="border:1px solid #ddd; padding:10px; margin:10px;">
                <h4>{item['title']}</h4>
                <p>{item['desc']}</p>
                <strong>{item['price']}</strong>
                <br><small>{now}</small>
            </div>
            """)

    return HTMLResponse(f"""
