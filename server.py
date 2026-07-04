from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="OSARE Hub")

# Static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Middleware to fix potential query param issues
@app.middleware("http")
async def fix_query_params(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard", methods=["GET", "HEAD"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin", methods=["GET", "HEAD"])
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

import os
# ...
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
