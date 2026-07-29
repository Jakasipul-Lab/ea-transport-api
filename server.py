import os
import uvicorn
from fastapi import FastAPI, Response, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def safari_home(q: str = ""):
    results_html = f"<p>Showing Safari results for: <b>{q}</b></p>" if q else ""
    return f"""
    <html>
        <head><title>Safari Search</title></head>
        <body style="font-family: Arial; padding: 40px;">
            <h1>Safari Search Engine</h1>
            <form action="/" method="get">
                <input type="text" name="q" value="{q}" placeholder="Search Safari..." style="padding: 8px; width: 300px;">
                <button type="submit" style="padding: 8px 16px;">Search</button>
            </form>
            {results_html}
        </body>
    </html>
    """

@app.get("/local", response_class=HTMLResponse)
def local_page(q: str = ""):
    results_html = f"<p>Showing Local results for: <b>{q}</b></p>" if q else ""
    return f"""
    <html>
        <head><title>Local Search</title></head>
        <body style="font-family: Arial; padding: 40px;">
            <h1>Local Search Engine</h1>
            <form action="/local" method="get">
                <input type="text" name="q" value="{q}" placeholder="Search Local..." style="padding: 8px; width: 300px;">
                <button type="submit" style="padding: 8px 16px;">Search</button>
            </form>
            {results_html}
        </body>
    </html>
    """

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------
# ✅ DATA PLATFORM
# --------------------------------------
SAFARI_DATABASE = [
    {"operator": "SGR Express", "origin": "Nairobi", "destination": "Mombasa", "time": "08:00 AM", "price": "KES 1,500", "info": "Standard class SGR train", "category": "safari", "keywords": ["nairobi", "mombasa"]},
    {"operator": "EAsafari Luxury Bus", "origin": "Nairobi", "destination": "Kisumu", "time": "09:30 AM", "price": "KES 1,800", "info": "Direct VIP coach", "category": "safari", "keywords": ["nairobi", "kisumu"]}
]

LOCAL_DATABASE = [
    {"operator": "Jakasipul Commuter", "origin": "Nairobi CBD", "destination": "Rongai", "time": "Every 10 mins", "price": "KES 100", "info": "Regular Matatu stage", "category": "local", "keywords": ["nairobi", "cbd", "rongai"]},
    {"operator": "Jakasipul Express", "origin": "Nairobi CBD", "destination": "Githurai", "time": "Every 5 mins", "price": "KES 80", "info": "Frequent town service", "category": "local", "keywords": ["nairobi", "cbd", "githurai"]}
]

# --------------------------------------
# ✅ PAGES & FILE ROUTING
# --------------------------------------
@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse("Error: index.html not found.", status_code=404)
    return FileResponse(file_path)

@app.head("/")
def home_head():
    return Response(status_code=200)

@app.get("/local")
@app.get("/local.html")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
@app.get("/safari.html")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.get("/{page_name}")
@app.get("/{page_name}.html")
def serve_other_pages(page_name: str):
    file_path = os.path.join(BASE_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    file_path_alt = os.path.join(BASE_DIR, page_name)
    if os.path.exists(file_path_alt):
        return FileResponse(file_path_alt)
        
    return HTMLResponse("Error: Page not found.", status_code=404)

# --------------------------------------
# ✅ UNIFIED API SEARCH ROUTE
# --------------------------------------
@app.get("/api/search")
def api_search(category: str = Query(...), q: str = ""):
    query = q.lower()
    source_db = SAFARI_DATABASE if category == "safari" else LOCAL_DATABASE
    results = []
    for item in source_db:
        if not query.strip() or any(k in query for k in item["keywords"]) or any(k in query for k in [item["origin"].lower(), item["destination"].lower()]):
            results.append(item)
    return JSONResponse(content=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
