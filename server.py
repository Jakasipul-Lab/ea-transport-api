from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, os

app = FastAPI()

# 1. serve static folder for images/css/js
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. DB setup - will auto create transport.db if missing
DB_NAME = "transport.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY,
    operator TEXT,
    origin TEXT,
    destination TEXT,
    time TEXT,
    price TEXT,
    category TEXT
)
""")
conn.commit()

# 3. API for search - Local and Safari
@app.get("/api/search")
def search(q: str = "", category: str = "local"):
    cur = conn.cursor()
    q = f"%{q}%"
    if category == "local":
        cur.execute("""
            SELECT operator, origin, destination, time, price
            FROM routes
            WHERE category='local' AND (origin LIKE? OR destination LIKE?)
        """, (q, q))
    else: # safari
        cur.execute("""
            SELECT operator, origin, destination, time, price
            FROM routes
            WHERE category='safari' AND (origin LIKE? OR destination LIKE? OR operator LIKE?)
        """, (q, q, q))

    rows = cur.fetchall()
    return [{"op":r[0],"origin":r[1],"dest":r[2],"time":r[3],"price":r[4]} for r in rows]

# 4. Serve all your HTML pages
# / -> index.html
@app.get("/")
def home():
    return FileResponse("index.html")

# /about -> about.html, /vendor -> vendor.html, etc
@app.get("/{page}")
def serve_page(page: str):
    filename = f"{page}.html"
    if os.path.exists(filename):
        return FileResponse(filename)
    # fallback to home if page not found
    return FileResponse("index.html")
