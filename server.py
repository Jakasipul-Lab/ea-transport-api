from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from werkzeug.datastructures import ImmutableMultiDict
import uvicorn
import random
import string

app = FastAPI(title="OSARE Hub")

# app.mount("/static", StaticFiles(directory="static"), name="static")
# Templates
templates = Jinja2Templates(directory="templates")

# Fix for Jinja2 cache bug
@app.before_request
def fix_request_args():
    if hasattr(request, 'args') and not isinstance(request.args, ImmutableMultiDict):
        request.args = ImmutableMultiDict(request.args)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/api/routes")
async def get_routes():
    return [
        {"route_id": "1", "origin": "Nairobi", "destination": "Mombasa", "operator": "SafariBus"},
        {"route_id": "2", "origin": "Kampala", "destination": "Kigali", "operator": "AfricaLink"}
    ]

@app.post("/api/book")
async def book_route(data: dict):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return {"status": "success", "booking_code": code}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
