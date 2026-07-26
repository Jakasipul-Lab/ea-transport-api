from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Serve your html files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/safari", response_class=HTMLResponse)
async def safari_page():
    with open("safari.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/local", response_class=HTMLResponse)
async def local_page():
    with open("local.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/search/safari", response_class=HTMLResponse)
async def search_safari(q: str = ""):
    html = f"""
    <body style='font-family:Arial; padding:20px; background:#fff7ed;'>
    <h2>🌍 Safari Results for: {q}</h2>
    <p>No data connected yet. You searched for: <b>{q}</b></p>
    <p><a href='/safari'>← Back to Safari Search</a></p>
    </body>
    """
    return HTMLResponse(html)

@app.get("/search/local", response_class=HTMLResponse)
async def search_local(q: str = ""):
    html = f"""
    <body style='font-family:Arial; padding:20px; background:#eff6ff;'>
    <h2>🚆 Local Results for: {q}</h2>
    <p>No data connected yet. You searched for: <b>{q}</b></p>
    <p><a href='/local'>← Back to Local Search</a></p>
    </body>
    """
    return HTMLResponse(html)
