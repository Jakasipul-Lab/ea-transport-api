from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, os

app = FastAPI()

# serve css/js/images if you have a static folder
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

DB_NAME = "transport.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS routes (id INTEGER PRIMARY KEY, operator TEXT, origin TEXT, destination TEXT, time TEXT, price TEXT, category TEXT, phone TEXT, osare_code TEXT)")
conn.commit()

@app.get("/api/search")
def search(q: str = "", category: str = "local"):
    cur = conn.cursor()
    q = f"%{q}%"
    cur.execute("SELECT operator, origin, destination, time, price, phone, osare_code FROM routes WHERE category =? AND (origin LIKE? OR destination LIKE?)", (category, q, q))
    rows = cur.fetchall()
    return [{"op":r[0],"origin":r[1],"dest":r[2],"time":r[3],"price":r[4],"phone":r[5],"code":r[6]} for r in rows]

# THIS IS THE PART FOR YOUR main FOLDER
@app.get("/")
def home():
    return FileResponse("main/index.html")

@app.get("/{page}")
def serve_page(page: str):
    path = f"main/{page}.html"
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse("main/index.html")
