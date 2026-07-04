import datetime
import os
import urllib.parse
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OSARE BRAND COLORS
BLUE = "#2563eb"
GREEN = "#059669"
DARK = "#0f172a"
GOLD = "#fbbf24"

# --------------------------------------
# ✅ DATA
# --------------------------------------
LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "🚌 Bus & Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train", "desc": "Nairobi ↔ Mombasa transport.", "price": "KES 1,500"},
    {"keywords": ["taxi", "car"], "title": "🚗 Taxi / Car Hire", "desc": "Comfortable and reliable rides.", "price": "KES 8,000/day"}
]

SAFARI_DATABASE = [
    {"keywords": ["mara"], "operator_id": "mara001", "title": "🦁 Masai Mara Safari", "desc": "3 Days Big Five experience.", "price": "$350", "dest": "mara"},
    {"keywords": ["zanzibar"], "operator_id": "znz001", "title": "🏖️ Zanzibar Beach Holiday", "desc": "4 Days beach package.", "price": "$490", "dest": "zanzibar"},
    {"keywords": ["serengeti"], "operator_id": "ser001", "title": "🐆 Serengeti Safari", "desc": "Migration wildlife experience.", "price": "$750", "dest": "serengeti"}
]

# --------------------------------------
# ✅ PAGES
# --------------------------------------
@app.get("/")
def home(): return FileResponse(os.path.join(BASE_DIR, "index.html"))
@app.get("/local")
@app.get("/local.html")
def local_page(): return FileResponse(os.path.join(BASE_DIR, "local.html"))
@app.get("/safari")
@app.get("/safari.html")
def safari_page(): return FileResponse(os.path.join(BASE_DIR, "safari.html"))
@app.head("/")
def home_head(): return Response(status_code=200)

# --------------------------------------
# ✅ LOCAL SEARCH - OSARE BLUE THEME
# --------------------------------------
@app.get("/search/local")
def search_local(q: str = ""):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []
    for item in LOCAL_DATABASE:
        if not query or any(k in query for k in item["keywords"]):
            results.append(f"""
            <div style="border:2px solid {BLUE}; padding:15px; margin:15px 0; border-radius:12px; background:#eff6ff;">
                <h4 style="color:{BLUE}; margin:0;">{item['title']}</h4>
                <p>{item['desc']}</p>
                <strong style="color:{BLUE}; font-size:1.1em;">{item['price']}</strong>
                <br><small>Updated: {now}</small>
            </div>
            """)

    html = f"""
    <html><head><title>OSARE Local Results</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:Arial; background:#f1f5f9; padding:20px;">
    <div style="background:{BLUE}; color:#fff; padding:20px; border-radius:10px; text-align:center;">
        <h2>🚆 OSARE Local Travel</h2>
    </div>
    <div style="max-width:700px; margin:20px auto;">
        {''.join(results) if results else '<p style="text-align:center;">No results found. Try: bus, sgr, taxi</p>'}
    </div>
    <p style="text-align:center;"><a href="/local" style="color:{BLUE};">← Back to Search</a></p>
    </body></html>
    """
    return HTMLResponse(html)

# --------------------------------------
# ✅ SAFARI SEARCH - OSARE GREEN THEME  
# --------------------------------------
@app.get("/search/safari")
def search_safari(q: str = ""):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []
    for item in SAFARI_DATABASE:
        if not query or any(k in query for k in item["keywords"]):
            results.append(f"""
            <div style="border:2px solid {GREEN}; padding:15px; margin:15px 0; border-radius:12px; background:#ecfdf5;">
                <h4 style="color:{GREEN}; margin:0;">{item['title']}</h4>
                <p>{item['desc']}</p>
                <strong style="color:{GREEN}; font-size:1.1em;">{item['price']}</strong>
                <br><small>Updated: {now}</small>
            </div>
            """)

    html = f"""
    <html><head><title>OSARE Safari Results</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:Arial; background:#ecfdf5; padding:20px;">
    <div style="background:{GREEN}; color:#fff; padding:20px; border-radius:10px; text-align:center;">
        <h2>🌍 OSARE Safari & Tours</h2>
    </div>
    <div style="max-width:700px; margin:20px auto;">
        {''.join(results) if results else '<p style="text-align:center;">No results found. Try: mara, zanzibar, serengeti</p>'}
    </div>
    <p style="text-align:center;"><a href="/safari" style="color:{GREEN};">← Back to Search</a></p>
    </body></html>
    """
    return HTMLResponse(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
