import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="OSARE Hub")

# Mount the static directory to serve CSS/JS/Images
# Ensure you have a folder named 'static' in the same directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- HTML CONTENT ---
# For now, keeping these as strings. In a real project, move these to a /templates folder.
HTML_SAFARI = "<html><head><link rel='stylesheet' href='/static/style.css'></head><body><h1>Safari Hub</h1></body></html>"
HTML_DASHBOARD = "<html><body><h1>Dashboard</h1></body></html>"
HTML_ADMIN = "<html><body><h1>Admin Panel</h1></body></html>"

@app.get("/")
async def get_safari():
    return HTMLResponse(content=HTML_SAFARI)

@app.get("/dashboard")
async def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)

@app.get("/admin")
async def get_admin():
    return HTMLResponse(content=HTML_ADMIN)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    # Removed reload=True for standard execution
    uvicorn.run(app, host="0.0.0.0", port=port)
