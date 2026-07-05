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
        "title": "Masai Mara 3-Day Safari",
        "vendor": "Mara Safari Lodges Ltd",
        "type": "Safari Package",
        "location": "Masai Mara National Reserve, Narok County",
        "desc": "Experience the Big Five. Includes game drives, park fees, transport from Nairobi, and 2 nights at a tented camp with meals.",
        "includes": ["Park fees", "Transport", "2 Nights Tented Camp", "All Meals", "Professional Guide"],
        "price": "$350",
        "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?q=80&w=800", # Mara photo
        "map_link": "https://maps.google.com/?q=Masai+Mara+National+Reserve",
        "dest": "mara"
    },
    {
        "keywords": ["zanzibar", "beach", "tanzania", "holiday", "island", "vacation", "resort"],
        "operator_id": "znz001",
        "title": "Zanzibar Beach Resort - 4 Days",
        "vendor": "Blue Ocean Resort",
        "type": "Hotel + Beach Package",
        "location": "Nungwi Beach, Zanzibar, Tanzania",
        "desc": "Relax on white sand beaches. 3 nights in beachfront resort, breakfast, airport transfers, and sunset dhow cruise.",
        "includes": ["3 Nights Beachfront Room", "Breakfast", "Airport Transfers", "Dhow Cruise"],
        "price": "$490",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=800", # Zanzibar photo
        "map_link": "https://maps.google.com/?q=Nungwi+Beach+Zanzibar",
        "dest": "zanzibar"
    },
    {
        "keywords": ["serengeti", "migration", "wildlife", "tanzania", "tour"],
        "operator_id": "ser001",
        "title": "Serengeti Migration Safari",
        "vendor": "Wild Trails Tanzania",
        "type": "Safari Package",
        "location": "Serengeti National Park, Tanzania",
        "desc": "Witness the Great Migration. 4 days, 3 nights lodge stay, unlimited game drives.",
        "includes": ["Park fees", "3 Nights Lodge", "All Meals", "Game Drives"],
        "price": "$750",
        "image": "https://images.unsplash.com/photo-1516426122078-a82eecbf4c90?q=80&w=800", # Serengeti photo
        "map_link": "https://maps.google.com/?q=Serengeti+National+Park",
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
@app.get("/search/safari")
def search_safari(q: str):
    query = q.lower()
    results = []
    for item in SAFARI_DATABASE:
        if smart_match(query, item["keywords"]):
            link = f"/click-lead?op={item['operator_id']}&dest={urllib.parse.quote(item['dest'])}&price={item['price']}"
            includes_list = "".join([f"<li>{i}</li>" for i in item['includes']])
            results.append(f"""
            <div style="border:1px solid #ddd; padding:20px; margin:15px 0; border-radius:12px; background:white; box-shadow:0 4px 12px rgba(0,0,0,0.06);">
                <img src="{item['image']}" style="width:100%; height:220px; object-fit:cover; border-radius:8px; margin-bottom:12px;">
                <h3 style="color:#1e3a8a; margin:0;">{item['title']}</h3>
                <p style="color:#f97316; font-weight:bold; margin:4px 0;">{item['type']} | By: {item['vendor']}</p>
                <p style="color:#64748b; font-size:14px;">📍 <a href="{item['map_link']}" target="_blank">{item['location']}</a></p>
                <p>{item['desc']}</p>
                <h4>What's Included:</h4>
                <ul style="margin-left:18px;">{includes_list}</ul>
                <h2 style="color:#10b981;">{item['price']}</h2>
                <a href="{link}" style="background:#25d366;color:white;padding:12px 20px;border-radius:8px; text-decoration:none; font-weight:bold; display:inline-block;">
                    Book via WhatsApp
                </a>
            </div>
            """)
    if not results:
        results.append("""
        <p>No matches found. Try: safari, mara, zanzibar, beach, hotel, serengeti</p>
        """)
    return HTMLResponse(f"""
    <div style="max-width:900px; margin:20px auto; padding:15px; font-family:Segoe UI;">
    <h2>Results for: "{q}"</h2>
    {''.join(results)}
    <br>
    <a href="/" style="color:#1e3a8a;">← Back to Search</a>
    </div>
    """)
# --------------------------------------
# WHATSAPP TRACKING
# --------------------------------------
@app.get("/click-lead")
def click_lead(op: str, dest: str, price: str):
    YOUR_PHONE = "254758378729"
    message = f"Hello, I want to book {dest} ({price}) [ID:{op}]"
    encoded = urllib.parse.quote(message)
    url = f"https://wa.me/{YOUR_PHONE}?text={encoded}"
    return Response(status_code=303, headers={"Location": url})
