from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
import string

app = FastAPI(title="OSARE Hub")

# Mount static files (css, js, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Home Page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

# Other Pages
@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# API Endpoints
@app.get("/api/routes")
async def get_routes():
    return [
        {"route_id": "1", "origin": "Nairobi", "destination": "Mombasa", "operator": "SafariBus", "type": "Express"},
        {"route_id": "2", "origin": "Kampala", "destination": "Kigali", "operator": "AfricaLink", "type": "Luxury"}
    ]

@app.post("/api/book")
async def book_route(data: dict):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return {"status": "success", "booking_code": code, "message": "Booking received"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
