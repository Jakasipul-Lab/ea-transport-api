from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
import random
import string

from database import engine, get_db, Base
import models

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# API Endpoint to list routes
@app.get("/api/routes")
def get_routes():
    # In a real app, you would fetch these from the database
    return [
        {"route_id": "1", "origin": "Nairobi", "destination": "Mombasa", "operator": "SafariBus", "type": "Express"},
        {"route_id": "2", "origin": "Kampala", "destination": "Kigali", "operator": "AfricaLink", "type": "Luxury"}
    ]

# API Endpoint to handle booking
@app.post("/api/book")
def book_route(data: dict):
    # Logic to save to DB (using your model)
    # Generate a random booking code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return {"status": "success", "code": code}

# Web Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
