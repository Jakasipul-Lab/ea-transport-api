import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
BASE_DIR = Path(__file__).parent

LOCAL_DATABASE = [
    {"keywords": ["bus", "matatu"], "title": "🚌 Bus & Matatu", "desc": "Daily routes.", "price": "KES 1,200"},
    {"keywords": ["train", "sgr"], "title": "🚆 SGR Train", "desc": "Nairobi ↔ Mombasa.", "price": "KES 1,500"}
]

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/migration.html")
def migration():
    return FileResponse(BASE_DIR / "migration.html")

@app.get("/admin.html")
def admin():
    return FileResponse(BASE_DIR / "admin.html")

@app.get("/support.html")
def support():
    return FileResponse(BASE_DIR / "support.html")

@app.get("/dashboard.html")
def dashboard():
    return FileResponse(BASE_DIR / "dashboard.html")

@app.get("/search/local")
def search_local(q: str = ""):
    query = q.lower()
    results = [f"<div><h4>{item['title']}</h4><p>{item['desc']}</p><strong>{item['price']}</strong></div>" for item in LOCAL_DATABASE if not query or any(k in query for k in item["keywords"])]
    return HTMLResponse(content="".join(results) if results else "<p>No results.</p>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
'@
