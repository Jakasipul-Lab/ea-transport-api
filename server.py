import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="OSARE Hub")
templates = Jinja2Templates(directory="templates")

@app.get("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard", methods=["GET", "HEAD"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin", methods=["GET", "HEAD"])
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

if __name__ == "__main__":
    # Render provides the port in the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
