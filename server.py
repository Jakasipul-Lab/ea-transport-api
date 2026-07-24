from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, os

app = FastAPI()

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

DB_NAME = "transport.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS routes (id INTEGER PRIMARY KEY, operator TEXT, origin TEXT, destination TEXT, time TEXT, price TEXT, category TEXT)")
conn.commit()

# add test data only if table is empty
c.execute("SELECT COUNT(*) FROM routes")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO routes VALUES (?,?,?,?,?,?,?)", [
        (1,'Metro Shuttle','Nairobi','Thika','6:00 AM','KES 200','local'),
        (2,'Safari Adventures','Nairobi','Maasai Mara','7:00 AM','KES 4500','safari'),
        (3,'Coast Express','Nairobi','Mombasa','8:00 AM','KES 1200','safari')
    ])
    conn.commit()

@app.get("/api/search")
def search(q: str = "", category: str = "local"):
    cur = conn.cursor()
    q = f"%{q}%"
    cur.execute("SELECT operator, origin, destination, time, price FROM routes WHERE category =? AND (origin LIKE? OR destination LIKE?)", (category, q, q))
    rows = cur.fetchall()
    return [{"op":r[0],"origin":r[1],"dest":r[2],"time":r[3],"price":r[4]} for r in rows]

@app.get("/")
def home(): return FileResponse("index.html")
@app.get("/{page}")
def serve_page(page: str):
    return FileResponse(f"{page}.html") if os.path.exists(f"{page}.html") else FileResponse("index.html")
