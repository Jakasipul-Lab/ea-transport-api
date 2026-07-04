import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

class RouteQuery(BaseModel):
    mode: str
    origin: dict
    destination: dict
    preferences: dict = {}

app = FastAPI(title="OSARE Hub")

if not os.path.exists("static"): os.makedirs("static")
if not os.path.exists("templates"): os.makedirs("templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- THE FIX: Added a catalog for your UI to display ---
@app.get("/api/routes")
async def get_all_routes():
    # This is the actual data your frontend will now find
    return [
        {"id": "1", "operator": "SafariBus", "origin": "Nairobi", "destination": "Mombasa"},
        {"id": "2", "operator": "CityLink", "origin": "Nairobi", "destination": "Kisumu"}
    ]

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/search")
async def search_route(query: RouteQuery):
    # This handles your specific logic when a user hits "Search"
    return {"status": "success", "message": "Search processed"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
