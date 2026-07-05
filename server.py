import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "Bus and Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "From KES 1,200"},
    {"keywords": ["train", "sgr", "tier 2"], "title": "SGR Train - 2nd Tier", "desc": "Nairobi to Mombasa economy class.", "price": "KES 1,500"}, # <- 2nd Tier is back
    {"keywords": ["train", "sgr", "tier 1"], "title": "SGR Train - 1st Tier", "desc": "Nairobi to Mombasa business class.", "price": "KES 3,000"}, # <- added 1st Tier too
    {"keywords": ["taxi", "car"], "title": "Taxi and Car Hire", "desc": "Comfortable and reliable rides.", "price": "From KES 8,000/day"}
]

@app.get("/", response_class=HTMLResponse)
async def home():
    cards = ""
    for item in LOCAL_DATABASE:
        cards += f"""
        <div style="border:1px solid #ddd; padding:15px; margin:10px; border-radius:8px;">
            <h3>{item['title']}</h3>
            <p>{item['desc']}</p>
            <p><b>Price: {item['price']}</b></p>
        </div>
        """
    return f"""
    <div style="background:#2563eb; color:#fff; padding:20px; border-radius:10px; text-align:center;">
        <h2>OSARE Local Travel</h2>
    </div>
    {cards}
    """

@app.get("/about", response_class=HTMLResponse)
async def about():
    return "<h1>About OSARE</h1>"
