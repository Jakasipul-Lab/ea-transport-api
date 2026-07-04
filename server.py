import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# 1. Define Request Structure
class RouteQuery(BaseModel):
    mode: str
    origin: dict
    destination: dict
    preferences: dict = {}

app = FastAPI(title="OSARE Hub")

# 2. Setup Directories (Safety check for deployment)
if not os.path.exists("static"): os.makedirs("static")
if not os.path.exists("templates"): os.makedirs("templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 3. Logic Modules
def process_commuter_search(query: RouteQuery):
    # Logic for daily commuters (e.g., traffic/transit APIs)
    return {"status": "success", "mode": "commuter", "data": "Route calculation logic here"}

def process_tourist_search(query: RouteQuery):
    # Logic for safari routes (e.g., GIS/Safety data)
    return {"status": "success", "mode": "tourist", "data": "Safari route logic here"}

# 4. API Endpoints
@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/search")
async def search_route(query: RouteQuery):
    if query.mode == "commuter":
        return process_commuter_search(query)
    elif query.mode == "tourist":
        return process_tourist_search(query)
    return {"error": "Invalid mode"}

# 5. Production Execution (No 'reload', uses production port)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
