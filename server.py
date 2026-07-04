from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
import string

app = FastAPI(title="OSARE Hub")

# Static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Middleware to fix potential query param issues
@app.middleware("http")
async def fix_query_params(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
