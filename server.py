# LINE 1: put this on top
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "🚌 Bus & Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train", "desc": "Nairobi ↔ Mombasa transport.", "price": "KES 1,500"},
    {"keywords": ["taxi", "car"], "title": "🚗 Taxi / Car Hire", "desc": "Comfortable and reliable rides.", "price": "KES 8,000/day"}
]

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <div style="background:#2563eb; color:#fff; padding:20px; border-radius:10px; text-align:center;">
        <h2>🚆 OSARE Local Travel</h2>
    </div>
    """
@app.get("/health")
async def health():
    return {"status": "ok"}
# LINE 3: then this
app = FastAPI()

# LINE 4: then this
templates = Jinja2Templates(directory="templates")

import datetime
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <h1>OSARE</h1>
    <p>Deployed successfully at {datetime.datetime.now()}</p>
    """
app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OSARE BRAND COLORS
BLUE = "#2563eb"
GREEN = "#059669"
DARK = "#0f172a"

# --------------------------------------
# ✅ DATA WITH IMAGES
# --------------------------------------
LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "🚌 Bus & Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train", "desc": "Nairobi ↔ Mombasa transport.", "price": "KES 1,500"},
    {"keywords": ["taxi", "car"], "title": "🚗 Taxi / Car Hire", "desc": "Comfortable and reliable rides.", "price": "KES 8,000/day"}
]

SAFARI_DATABASE = [
    {
        "keywords": ["mara"], "operator_id": "mara001", 
        "title": "🦁 Masai Mara Safari", "desc": "3 Days Big Five experience. Witness the Great Migration.",
        "price": "$350", "dest": "mara",
        "img": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?q=80&w=1200"  # Lion
    },
    {
        "keywords": ["zanzibar"], "operator_id": "znz001",
        "title": "🏖️ Zanzibar Beach Holiday", "desc": "4 Days beach package. White sand & turquoise waters.",
        "price": "$490", "dest": "zanzibar",
        "img": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1200"  # Beach
    },
    {
        "keywords": ["serengeti"], "operator_id": "ser001",
        "title": "🐆 Serengeti Safari", "desc": "Migration wildlife experience in Tanzania.",
        "price": "$750", "dest": "serengeti",
        "img": "https://images.unsplash.com/photo-1516426122078-a0825049d721?q=80&w=1200"  # Safari
    }
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
 @app.get('/about')
def about():
    return send_file('about.html')
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# --------------------------------------
# ✅ LOCAL SEARCH - BLUE CARDS
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
    html = f"""<html><head><title>OSARE Local</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:Arial; background:#f1f5f9; padding:20px;">
    <div style="background:{BLUE}; color:#fff; padding:20px; border-radius:10px; text-align:center;"><h2>🚆 OSARE Local Travel</h2></div>
    <div style="max-width:700px; margin:20px auto;">{''.join(results) if results else '<p>No results. Try: bus, sgr, taxi</p>'}</div>
    <p style="text-align:center;"><a href="/local" style="color:{BLUE};">← Back</a></p></body></html>"""
    return HTMLResponse(html)

# --------------------------------------
# ✅ SAFARI SEARCH - GREEN CARDS + IMAGES
# --------------------------------------
@app.get("/search/safari")
def search_safari(q: str = ""):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []
    for item in SAFARI_DATABASE:
        if not query or any(k in query for k in item["keywords"]):
            results.append(f"""
            <div style="border:2px solid {GREEN}; border-radius:12px; background:#ecfdf5; overflow:hidden; margin:20px 0;">
                <img src="{item['img']}" style="width:100%; height:200px; object-fit:cover;">
                <div style="padding:15px;">
                    <h4 style="color:{GREEN}; margin:0;">{item['title']}</h4>
                    <p>{item['desc']}</p>
                    <strong style="color:{GREEN}; font-size:1.2em;">{item['price']}</strong>
                    <br><small>Updated: {now}</small>
                </div>
            </div>
            """)
    html = f"""<html><head><title>OSARE Safari</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:Arial; background:#ecfdf5; padding:20px;">
    <div style="background:{GREEN}; color:#fff; padding:20px; border-radius:10px; text-align:center;"><h2>🌍 OSARE Safari & Tours</h2></div>
    <div style="max-width:700px; margin:20px auto;">{''.join(results) if results else '<p>No results. Try: mara, zanzibar, serengeti</p>'}</div>
    <p style="text-align:center;"><a href="/safari" style="color:{GREEN};">← Back</a></p></body></html>"""
    return HTMLResponse(html)

from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/safari')
def safari():
    return send_file('safari.html')

@app.route('/local')
def local():
    return send_file('local.html')

@app.route('/about')
def about():
    return send_file('about.html')

@app.route('/dashboard')
def dashboard():
    return send_file('dashboard.html')

@app.route('/migration')
def migration():
    return send_file('migration.html')
from flask import Flask, render_template

app = Flask(__name__)  # don't change static_folder unless needed

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # change 8000 to 3000 or 8080
