import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

import sqlite3

# ✅ connect to database
conn = sqlite3.connect("travel.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    desc TEXT,
    keywords TEXT,
    region TEXT,
    price INTEGER,
    link TEXT
)
""")

conn.commit()

app = FastAPI()

# ✅ STEP 3 — DATA ENGINE (ADD HERE)
SEARCH_DATA = [
    {
        "name": "Masai Mara Safari",
        "desc": "3-Day Big Five Safari",
        "keywords": ["safari", "mara", "kenya", "wildlife"],
        "region": "africa",
        "price": 1200,
        "link": "https://wa.me/254700000000?text=Masai Mara Safari"
    },
    {
        "name": "Zanzibar Holiday",
        "desc": "Luxury Beach Escape",
        "keywords": ["zanzibar", "beach", "tanzania"],
        "region": "africa",
        "price": 900,
        "link": "https://wa.me/254700000000?text=Zanzibar Trip"
    },
    {
        "name": "Dubai City Tour",
        "desc": "Luxury Middle East Experience",
        "keywords": ["dubai", "uae", "tour"],
        "region": "asia",
        "price": 1500,
        "link": "https://wa.me/254700000000?text=Dubai Tour"
    }
]

# ✅ HOME PAGE
@app.get("/")
def read_root():
    return FileResponse('index.html')

# ✅ ✅ STEP 4 — REAL SEARCH ENGINE (ONLY ONE /search!)
@app.get("/search")
def search(q: str):
    query_words = q.lower().split()

    results = []

    for item in SEARCH_DATA:
        score = 0

        # 🔎 keyword scoring
        for word in query_words:
            if word in item["keywords"]:
                score += 3

        # 🌍 boost Africa (your business focus)
        if item["region"] == "africa":
            score += 2

        if score > 0:
            item_copy = item.copy()
            item_copy["score"] = score
            results.append(item_copy)

    # ✅ sort best results first
    results.sort(key=lambda x: x["score"], reverse=True)

    # ✅ build HTML dynamically
    cards = ""

    for r in results:
        cards += f"""
        <div class="card">
            <h3>{r['name']}</h3>
            <p>{r['desc']}</p>
            <p><b>From ${r['price']}</b></p>
            <a href="{r['link']}" class="btn">Book Now</a>
        </div>
        """

    if not cards:
        cards = "<p>No results found</p>"

    html = f"""
    <html>
    <head>
        <title>Search Results</title>
        <style>
            body {{ font-family: Arial; text-align:center; background:#f4f7f6; }}
            .card {{ background:white; padding:20px; margin:20px auto; max-width:400px; border-radius:10px; }}
            .btn {{ display:block; padding:10px; margin-top:10px; background:#16a34a; color:white; text-decoration:none; }}
        </style>
    </head>
    <body>
        <h1>Results for: {q}</h1>
        {cards}
        <br><a href="/">← Back</a>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

# ✅ STATIC ROUTES
@app.get("/osare")
def get_osare():
    return FileResponse('osare.html')

@app.get("/local")
def get_local():
    return FileResponse('local.html')

@app.get("/safari")
def get_safari():
    return FileResponse('safari.html')

@app.get("/about")
def get_about():
    return FileResponse('about.html')

@app.get("/support")
def get_support():
    return FileResponse('support.html')

# ✅ SERVER START (ONLY ONCE)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
