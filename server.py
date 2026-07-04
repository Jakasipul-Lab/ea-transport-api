import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="EA SafariRoutes")
templates = Jinja2Templates(directory="templates")

# --- 1. API ROUTES ---
@app.get("/api/routes")
async def get_routes():
    return [
        {"id": 1, "operator": "SafariBus", "origin": "Nairobi", "destination": "Mombasa"},
        {"id": 2, "operator": "CityLink", "origin": "Nairobi", "destination": "Kisumu"}
    ]

# --- 2. EXPLICIT PAGE ROUTES (No more 'Not Found' errors) ---
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/migration")
async def migration(request: Request):
    return templates.TemplateResponse("migration.html", {"request": request})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
