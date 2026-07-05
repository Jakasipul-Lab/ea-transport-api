import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "Bus and Matatu Transport", "desc": "Daily routes across towns and cities.", "price": "From KES 1,200", "route": "All major towns"},
    {"keywords": ["train", "sgr", "tier 2"], "title": "SGR Train - 2nd Tier", "desc": "Nairobi to Mombasa economy class. Air conditioned.", "price": "KES 1,500", "route": "Nairobi ↔ Mombasa"},
    {"keywords": ["train", "sgr", "tier 1"], "title": "SGR Train - 1st Tier", "desc": "Nairobi to Mombasa business class.", "price": "KES 3,000", "route": "Nairobi ↔ Mombasa"},
    {"keywords": ["taxi", "car"], "title": "Taxi and Car Hire", "desc": "Comfortable and reliable rides with driver.", "price": "From KES 8,000/day", "route": "Door to door"}
]

def render_page(services):
    cards = ""
    for item in services:
        cards += f"""
        <div style="border:1px solid #e5e7eb; padding:20px; margin:15px 0; border-radius:12px; box-shadow:0 2px 5px rgba(0,0,0,0.05); background:#fff;">
            <h3 style="margin:0; color:#2563eb;">{item['title']}</h3>
            <p style="color:#555; margin:8px 0;">{item['desc']}</p>
            <p style="margin:4px 0;"><b>Route:</b> {item['route']}</p>
            <p style="margin:4px 0; font-size:18px; color:#16a34a;"><b>Price: {item['price']}</b></p>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <title>OSARE Local Travel</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; background:#f9fafb; margin:0; padding:20px; }}
            .header {{ background:#2563eb; color:#fff; padding:25px; border-radius:12px; text-align:center; margin-bottom:20px; }}
            .search {{ width:100%; padding:12px; border:1px solid #ddd; border-radius:8px; margin-bottom:20px; font-size:16px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>OSARE Local Travel</h1>
            <p>Find buses, trains, and taxis near you</p>
        </div>
        
        <form method="get">
            <input class="search" type="text" name="q" placeholder="Search: bus, sgr, taxi..." value="{Request.query_params.get('q','') if 'Request' in globals() else ''}">
        </form>

        <div>{cards}</div>
        <p style="text-align:center; color:#888; margin-top:30px;">Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    query = request.query_params.get("q", "").lower()
    if query:
        filtered = [s for s in LOCAL_DATABASE if query in " ".join(s["keywords"]).lower() or query in s["title"].lower()]
    else:
        filtered = LOCAL_DATABASE
    return render_page(filtered)

@app.get("/about", response_class=HTMLResponse)
async def about():
    return "<h1>About OSARE</h1><p>Connecting Kenya to affordable local transport.</p>"
