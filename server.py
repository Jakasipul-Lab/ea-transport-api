from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, os

app = FastAPI()

# serve static folder for images/css
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# DB
conn = sqlite3.connect("transport.db", check_same_thread=False)
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

@app.get("/api/search")
def search(q: str = "", category: str = "local"):
    cur = conn.cursor()
    if category == "local":
        cur.execute("""
            SELECT operator, origin, destination, time, price
            FROM routes
            WHERE category='local' AND (origin LIKE? OR destination LIKE?)
        """, (f"%{q}%", f"%{q}%"))
    else: # safari
        cur.execute("""
            SELECT operator, origin, destination, time, price
            FROM routes
            WHERE category='safari' AND (origin LIKE? OR destination LIKE? OR operator LIKE?)
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    rows = cur.fetchall()
    return [{"op":r[0],"origin":r[1],"dest":r[2],"time":r[3],"price":r[4]} for r in rows]

# serve your pages
@app.get("/{page}")
def serve(page: str):
    if os.path.exists(f"{page}.html"):
        return FileResponse(f"{page}.html")
    if os.path.exists(page):
        return FileResponse(page)
    return FileResponse("index.html")
