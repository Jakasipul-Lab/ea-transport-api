import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

# --------------------------------------
# SMART DATA
# --------------------------------------
LOCAL_DATABASE = [
    {
        "keywords": ["bus", "matatu", "transport", "travel", "ride", "shuttle"],
        "title": "Local Shuttle & Matatu Transport",
        "desc": "Daily transport across cities and towns.",
        "price": "KES 1,200"
    },
    {
        "keywords": ["train", "sgr", "rail", "mombasa", "nairobi"],
        "title": "SGR Train Transport",
        "desc": "Nairobi ↔ Mombasa railway booking.",
        "price": "KES 1,500"
    },
    {
        "keywords": ["taxi", "car", "hire", "vehicle", "uber"],
        "title": "Taxi & Car Hire",
        "desc": "Affordable ride and car hire services.",
        "price": "KES 8,000/day"
    }
]

SAFARI_DATABASE = [
    {
        "keywords": ["mara", "safari", "kenya", "wildlife", "tour", "trip", "holiday"],
        "operator_id": "mara001",
        "title": "Masai Mara Safari",
        "desc": "3 Days Big Five safari experience.",
        "price": "$350",
        "dest": "mara"
    },
    {
        "keywords": ["zanzibar", "beach", "tanzania", "holiday", "island", "vacation"],
        "operator_id": "znz001",
        "title": "Zanzibar Beach Holiday",
        "desc": "4 Days beach package with hotel.",
        "price": "$490",
        "dest": "zanzibar"
    },
    {
        "keywords": ["serengeti", "migration", "wildlife", "tanzania", "tour"],
        "operator_id": "ser001",
        "title": "Serengeti Safari Tour",
        "desc": "Wildlife migration safari package.",
        "price": "$750",
        "dest": "serengeti"
    }
]

# --------------------------------------
# PAGES
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
# SMART SEARCH FUNCTION
# --------------------------------------
def smart_match(query, keywords):
    words = query.lower().split()
    return any(k in query for k in keywords) or any(w in keywords for w in words)

# --------------------------------------
# LOCAL SEARCH
# --------------------------------------
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []
    for item in LOCAL_DATABASE:
        if smart_match(query, item["keywords"]):
            results.append(f"""
            <div style="border:1px solid #ddd; padding:10px; margin:10px;">
                <h4>{item['title']}</h4>
                <p>{item['desc']}</p>
                <strong>{item['price']}</strong> <small>{now}</small>
            </div>
            """)
    if not results:
        results.append("""
        <p>No exact match found. Try general terms like:
        transport, bus, taxi, travel.</p>
        """)
    return HTMLResponse(f"""
    <h2>Local Results for: {q}</h2>
    {''.join(results)}
    <br>
    <a href="/local">← Back</a>
    """)

# --------------------------------------
# SAFARI SEARCH
# --------------------------------------
@app.get("/search/safari")
def search_safari(q: str):
    query = q.lower()
    results = []
    for item in SAFARI_DATABASE:
        if smart_match(query, item["keywords"]):
            link = f"/click-lead?op={item['operator_id']}&dest={urllib.parse.quote(item['dest'])}&price={item['price']}"
            results.append(f"""
            <div style="border:1px solid green; padding:15px; margin:10px;">
                <h3>{item['title']} - {item['price']}</h3>
                <p>{item['desc']}</p>
                <a href="{link}" style="background:green;color:white;padding:8px;border-radius:5px;">
                    Book via WhatsApp
                </a>
            </div>
            """)
    if not results:
        results.append("""
        <p>No safari matches found. Try:
        safari, mara, kenya, beach, zanzibar.</p>
        """)
    return HTMLResponse(f"""
    <h2>Safari Results for: {q}</h2>
    {''.join(results)}
    <br>
    <a href="/safari">← Back</a>
    """)

# --------------------------------------
# WHATSAPP TRACKING
# --------------------------------------
@app.get("/click-lead")
def click_lead(op: str, dest: str, price: str):
    YOUR_PHONE = "254700000"
    message = f"Hello, I want to book {dest} ({price}) [ID:{op}]"
    encoded = urllib.parse.quote(message)
    url = f"https://wa.me/{YOUR_PHONE}?text={encoded}"
    return Response(status_code=303, headers={"Location": url})
