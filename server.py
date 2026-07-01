import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).parent

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/dashboard.html")
def get_dashboard():
    return FileResponse(BASE_DIR / "dashboard.html")

@app.get("/migration.html")
def get_migration():
    return FileResponse(BASE_DIR / "migration.html")

@app.get("/search.html")
def search():
    return FileResponse(BASE_DIR / "search.html")

@app.get("/admin.html")
def admin():
    return FileResponse(BASE_DIR / "admin.html")

@app.get("/migration.html")
def migration():
    return FileResponse(BASE_DIR / "migration.html")

@app.get("/support.html")
def support():
    return FileResponse(BASE_DIR / "support.html")

@app.get("/dashboard.html")
def dashboard():
    return FileResponse(BASE_DIR / "dashboard.html")

# This makes it run on Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
