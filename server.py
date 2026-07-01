import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).parent

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"ok": "Livebooking Engine is Live"}

@app.get("/dashboard.html")
def get_dashboard():
    return FileResponse(BASE_DIR / "dashboard.html")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Livebooking Engine</title></head>
    <body style="text-align:center;padding:50px;font-family:sans-serif">
      <h1>Livebooking Engine is Live ✅</h1>
      <p>Your booking site is up on Render</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
