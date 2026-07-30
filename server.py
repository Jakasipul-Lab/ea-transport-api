import datetime
import os
import uvicorn
from fastapi import FastAPI, Response, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

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
# ✅ PAGE ROUTES (Fixes code showing as text)
# --------------------------------------
@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse("Error: index.html not found in project directory.", status_code=404)
    return FileResponse(file_path)

@app.head("/")
def home_head():
    return Response(status_code=200)

@app.get("/local.html")
def local_page():
    file_path = os.path.join(BASE_DIR, "local.html")
    if not os.path.exists(file_path):
        return HTMLResponse("Error: local.html not found in project directory.", status_code=404)
    return FileResponse(file_path)

@app.get("/safari.html")
def safari_page():
    file_path = os.path.join(BASE_DIR, "safari.html")
    if not os.path.exists(file_path):
        return HTMLResponse("Error: safari.html not found in project directory.", status_code=404)
    return FileResponse(file_path)

# --------------------------------------
# ✅ UNIFIED API SEARCH ROUTE
# --------------------------------------
@app.get("/api/search")
def api_search(category: str = Query(...), q: str = ""):
    query = q.lower()
    source_db = SAFARI_DATABASE if category == "safari" else LOCAL_DATABASE
    results = []
    
    for item in source_db:
        if (not query.strip() or 
            any(k in query for k in item["keywords"]) or 
            any(k in query for k in [item["origin"].lower(), item["destination"].lower()])):
            results.append(item)
            
    return JSONResponse(results)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
