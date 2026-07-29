import datetime
import os
import uvicorn
from fastapi import FastAPI, Response, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so browser fetches never get blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# ✅ PAGES
# --------------------------------------
@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "index.html file missing in server directory"})
    return FileResponse(file_path)

@app.head("/")
def home_head(): 
    return Response(status_code=200)

# --------------------------------------
# ✅ SEARCH API ENDPOINT
# --------------------------------------
@app.get("/api/search")
def api_search(category: str = Query("safari"), q: str = ""):
    query = q.lower().strip()
    source_db = SAFARI_DATABASE if category == "safari" else LOCAL_DATABASE
    
    results = []
    for item in source_db:
        if not query or any(k in query for k in item["keywords"]) or query in item["origin"].lower() or query in item["destination"].lower():
            results.append(item)
            
    return JSONResponse(content=results)

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
  return "Hello, World!"


if __name__ == "__main__":
  app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
