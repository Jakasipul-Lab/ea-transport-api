import os
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)

# ✅ HOME
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# ✅ LOCAL PAGE
@app.get("/local")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

# ✅ SAFARI PAGE
@app.get("/safari")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

# ✅ ABOUT PAGE
@app.get("/about")
def about_page():
    return FileResponse(os.path.join(BASE_DIR, "about.html"))

# ✅ ✅ LOCAL SEARCH (OPERATIONS)
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")

    results = []

    if "bus" in query:
        results.append(f"🚌 Bus available now ({now})")

    if "train" in query or "sgr" in query:
        results.append(f"🚆 SGR departure around {now}")

    if "matatu" in query:
        results.append(f"🚐 Matatu running now ({now})")

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

# ✅ ✅ SAFARI SEARCH (MONETIZATION)
@app.get("/search/safari")
def search_safari(q: str):
    query = q.lower()

    results = []

    if "safari" in query or "mara" in query:
        results.append("""
        <h3>Masai Mara Safari - $1200</h3>
        <a href="/click-lead/safari?operator_id=mara_cruisers&transport=4x4&dest=masai+mara">
        Book via WhatsApp</a>
        """)

    if "zanzibar" in query or "beach" in query:
        results.append("""
        <h3>Zanzibar Beach Holiday - $900</h3>
        <a href="/click-lead/safari?operator_id=mara_cruisers&transport=flight&dest=zanzibar">
        Book via WhatsApp</a>
        """)

    if not results:
        results.append("No safari results found")

    return HTMLResponse(f"""
    <h2>Safari Results for: {q}</h2>
    {'<br><br>'.join(results)}
    <br><br>
    <a href="/safari">← Back</a>
    """)
