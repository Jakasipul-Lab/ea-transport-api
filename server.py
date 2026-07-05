import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "Bus and Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "SGR Train", "desc": "Nairobi to Mombasa transport.", "price": "KES 1,500"},
    {"keywords": ["taxi", "car"], "title": "Taxi and Car Hire", "desc": "Comfortable and reliable rides.", "price": "KES 8,000/day"}
]

@app.get("/", response_class=HTMLResponse)
async def home():
    services = ""
    for item in LOCAL_DATABASE:
        services += f"<li>{item['title']} - {item['price']}</li>"
    
    return f"""
    <div style="background:#2563eb; color:#fff; padding:20px; border-radius:10px; text-align:center;">
        <h2>OSARE Local Travel</h2>
    </div>
    <ul>{services}</ul>
    """

@app.get("/about", response_class=HTMLResponse)
async def about():
    return "<h1>About OSARE</h1><p>We connect you to local transport.</p>"
