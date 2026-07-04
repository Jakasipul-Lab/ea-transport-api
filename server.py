import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Initialize the app with your brand name
app = FastAPI(title="EA SafariRoutes")

# Only templates are used for the UI
templates = Jinja2Templates(directory="templates")

class RouteQuery(BaseModel):
    mode: str
    origin: dict
    destination: dict
    preferences: dict = {}

# --- PAGE ROUTES ---
@app.get("/{page}")
async def get_page(request: Request, page: str = "index"):
    try:
        return templates.TemplateResponse(f"{page}.html", {"request": request})
    except Exception:
        # Fallback if the file is missing
        return {"error": "Page not found"}

# --- API ROUTES ---
@app.get("/api/routes")
async def get_routes():
    return [
        {"id": 1, "operator": "SafariBus", "origin": "Nairobi", "destination": "Mombasa"},
        {"id": 2, "operator": "CityLink", "origin": "Nairobi", "destination": "Kisumu"}
    ]

# Production runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
