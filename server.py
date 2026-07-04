import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# --- THE FIX: Added your brand name here ---
app = FastAPI(title="EA SafariRoutes")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class RouteQuery(BaseModel):
    mode: str
    origin: dict
    destination: dict
    preferences: dict = {}

# --- ALL PAGE ROUTES ---
@app.get("/{page}")
async def get_page(request: Request, page: str = "index"):
    try:
        return templates.TemplateResponse(f"{page}.html", {"request": request})
    except Exception as e:
        return {"error": f"Template {page}.html not found"}

# --- API ROUTES ---
@app.get("/api/routes")
async def get_routes():
    return [
        {"id": 1, "operator": "SafariBus", "origin": "Nairobi", "destination": "Mombasa"},
        {"id": 2, "operator": "CityLink", "origin": "Nairobi", "destination": "Kisumu"}
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
