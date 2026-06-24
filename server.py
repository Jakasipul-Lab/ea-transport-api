import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Point this to your root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# If you have CSS or JS files, put them in a folder called 'static'
# If you don't have that folder, you can delete this line:
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/safari")
def get_safari():
    return FileResponse("safari.html")

@app.get("/local")
def get_local():
    return FileResponse("local.html")

@app.get("/about")
def get_about():
    return FileResponse("about.html")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/{page_name}.html")
async def serve_other_pages(page_name: str):
    # This specifically looks for your .html files
    return FileResponse(os.path.join(BASE_DIR, f"{page_name}.html"))

from fastapi.responses import HTMLResponse
import datetime

@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")

    results = []

    if "bus" in query:
        results.append(f"🚌 Bus available now ({now})")

    if "train" in query or "sgr" in query:
        results.append(f"🚆 SGR available ({now})")

    if "matatu" in query:
        results.append(f"🚐 Matatu running ({now})")

    if "car" in query or "taxi" in query:
        results.append(f"🚗 Car hire available ({now})")

    if not results:
        results.append("No local transport found")

    return HTMLResponse(f"""
    <h2>Local Results for: {q}</h2>
    {'<br>'.join(results)}
    <br><br>
    <a href="/local">← Back</a>
    """)
