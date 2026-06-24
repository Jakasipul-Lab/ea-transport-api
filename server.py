import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import datetime

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)

# ✅ Pages
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
def local():
    return FileResponse("local.html")

from fastapi import FastAPI
import datetime

app = FastAPI()  # <--- This must be here!

@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    return {"query": query, "time": now} # Don't forget to return something!

@app.get("/safari")
def safari():
    return FileResponse("safari.html")

@app.get("/about")
def about():
    return FileResponse("about.html")

# ✅ SIMPLE LOCAL SEARCH (SAFE)
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")

    results = []

    if "bus" in query:
        results.append(f"🚌 Bus available ({now})")

    if "matatu" in query:
        results.append(f"🚐 Matatu running ({now})")

    if "sgr" in query or "train" in query:
        results.append(f"🚆 SGR available ({now})")

    if "taxi" in query or "car" in query:
        results.append(f"🚗 Car hire available ({now})")

    if not results:
        results.append("No transport found")

    return HTMLResponse(f"""
    <h2>Local Results for: {q}</h2>
    {'<br>'.join(results)}
    <br><br>
    /local← Back</a>
    """)
