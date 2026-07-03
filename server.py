from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn

# Importing your modular components
from database import engine, get_db, Base
import models

# 1. Initialize Database Tables
Base.metadata.create_all(bind=engine)

# 2. Initialize App and Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 3. Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/inquire")
async def inquire(
    name: str = Form(...), 
    email: str = Form(...), 
    route: str = Form(...), 
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create a new record using the SQLAlchemy model
    new_booking = models.Booking(name=name, email=email, route=route, date=date)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return RedirectResponse("/", status_code=303)

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"status": "success", "message": "Connected to database successfully!"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
