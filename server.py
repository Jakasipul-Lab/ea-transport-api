import datetime
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data
LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "🚌 Bus & Matatu", "desc": "Daily routes.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train", "desc": "Nairobi ↔ Mombasa.", "price": "KES 1,500"}
]

# Pages
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local.html")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari.html")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

# Search
@app.get("/search/local")
def search_local(q: str = ""):
    query = q.lower()
    results = [
        f"<div><h4>{item['title']}</h4><p>{item['desc']}</p><strong>{item['price']}</strong></div>"
        for item in LOCAL_DATABASE if not query or any(k in query for k in item["keywords"])
    ]
    return HTMLResponse(content="".join(results) if results else "<p>No results.</p>")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8005, reload=False)
