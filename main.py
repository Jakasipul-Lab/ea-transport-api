import datetime
import os
import urllib.parse
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)

# ---------------------------------------------------------
# 🛠️ EMBEDDED REAL DATA FALLBACK (Replaces corrupted server)
# ---------------------------------------------------------
LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu", "shuttle"], "title": "🚐 Reliable Local Shuttle & Matatu Routes", "desc": "Daily departures across major towns.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "列車 SGR Express Economy Tier", "desc": "Mombasa to Nairobi ticketing assistance.", "price": "KES 1,500"},
    {"keywords": ["car", "taxi", "hire", "cruiser"], "title": "🚗 Budget Safari Van & Car Hire", "desc": "Self-drive or chauffeured options for local groups.", "price": "KES 8,000/day"}
]

SAFARI_DATABASE = [
    {"keywords": ["mara", "safari", "big five", "kenya"], "operator_id": "mara_cruisers", "title": "🦁 Budget Masai Mara Group Joining Safari", "desc": "3 Days, 2 Nights. See the Big Five. Ideal for tourists & local groups.", "price": "$350", "dest": "masai mara"},
    {"keywords": ["zanzibar", "beach", "tanzania"], "operator_id": "znz_tours", "title": "🏖️ Zanzibar Beach Getaway & Stone Town", "desc": "4 Days all-inclusive package with airport transfers.", "price": "$490", "dest": "zanzibar"},
    {"keywords": ["serengeti", "migration"], "operator_id": "serengeti_wild", "title": "🐆 Serengeti & Ngorongoro Crater Circuit", "desc": "Budget camping safari for international groups.", "price": "$750", "dest": "serengeti"}
]

# --- PAGES ---

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.get("/about")
def about_page():
    return FileResponse(os.path.join(BASE_DIR, "about.html"))


# --- API OPERATIONS & MONETIZATION ---

# ✅ FIX: DYNAMIC LOCAL SEARCH
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []

    # Loop through the database instead of hardcoded words
    for item in LOCAL_DATABASE:
        if any(keyword in query for keyword in item["keywords"]):
            results.append(f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <h4>{item['title']}</h4>
                <p>{item['desc']}</p>
                <strong>Price: {item['price']}</strong> <small>(Updated at {now})</small>
            </div>
            """)

    if not results:
        results.append("<p>No local transport options match your search. Try keywords like: Bus, SGR, Matatu, or Car.</p>")

    return HTMLResponse(f"""
    <h2>Local Results for: {q}</h2>
    {''.join(results)}
    <br>
    <a href="/local">← Back to Search</a>
    """)


# ✅ FIX: DYNAMIC SAFARI SEARCH WITH TRACKING
@app.get("/search/safari")
def search_safari(q: str):
    query = q.lower()
    results = []

    for item in SAFARI_DATABASE:
        if any(keyword in query for keyword in item["keywords"]):
            # URL Encoded variables safely passed to the click-lead pipeline
            link = f"/click-lead/safari?operator_id={item['operator_id']}&dest={urllib.parse.quote_plus(item['dest'])}&price={item['price']}"
            results.append(f"""
            <div style="border: 1px solid #2ecc71; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
                <h3>{item['title']} — <span style="color:#2ecc71;">{item['price']}</span></h3>
                <p>{item['desc']}</p>
                <a href="{link}" style="background-color:#2ecc71; color:white; padding: 8px 12px; text-decoration:none; border-radius:3px; display:inline-block;">
                    Book Route via Agent WhatsApp
                </a>
            </div>
            """)

    if not results:
        results.append("<p>No safari packages found matching that location. Try searching 'Mara', 'Zanzibar', or 'Serengeti'.</p>")

    return HTMLResponse(f"""
    <h2>Safari Tour Results for: {q}</h2>
    {''.join(results)}
    <br><br>
    <a href="/safari">← Back to Search</a>
    """)


# ✅ FIX: TRACKED REDIRECT FOR YOUR 5% COMMISSION
@app.get("/click-lead/safari")
def safari_lead(operator_id: str, dest: str, price: str):
    # YOUR phone number where you receive the lead first
    YOUR_PHONE = "254700000000" 
    
    # The message includes the vendor identity (operator_id) so you know exactly who owes you 5%
    message = f"Hello SafariRoutes! I want to book the package to {dest} ({price}). [TRACKING_ID: {operator_id}]"
    encoded_message = urllib.parse.quote_plus(message)

    whatsapp_url = f"https://wa.me/{YOUR_PHONE}?text={encoded_message}"

    # Redirects the client straight into WhatsApp conversation with the secure tracking ID intact
    return Response(status_code=303, headers={"Location": whatsapp_url})
