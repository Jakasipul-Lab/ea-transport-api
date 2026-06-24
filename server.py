import os
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Static Pages ---
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/search/local", response_class=HTMLResponse)
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = ["...your logic here..."]
    
    # WRAP IN HTML TAGS
    return f"""
    <html>
        <body>
            <h2>Local Results for: {q}</h2>
            <p>{'<br>'.join(results)}</p>
            <br><br>
            <a href="/local">← Back</a>
        </body>
    </html>
    """

@app.get("/local")
@app.get("/local.html")
def local():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
def safari():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.get("/about")
def about():
    return FileResponse(os.path.join(BASE_DIR, "about.html"))

# --- Search Functionality ---
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []

    if "bus" in query: results.append(f"🚌 Bus available ({now})")
    if "matatu" in query: results.append(f"🚐 Matatu running ({now})")
    if "sgr" in query or "train" in query: results.append(f"🚆 SGR available ({now})")
    if "taxi" in query or "car" in query: results.append(f"🚗 Car hire available ({now})")

    if not results:
        results.append("No transport found")

    return HTMLResponse(f"""
    <html>
        <body>
            <h2>Local Results for: {q}</h2>
            {'<br>'.join(results)}
            <br><br>
            <a href="/local">← Back</a>
        </body>
    </html>
    """)
