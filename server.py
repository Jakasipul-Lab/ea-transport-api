import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# Initialize App
app = FastAPI(title="OSARE Hub")

# Setup Templates
templates = Jinja2Templates(directory="templates")

# 1. Primary Routes
@app.get("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard", methods=["GET", "HEAD"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin", methods=["GET", "HEAD"])
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# 2. Catch-all to prevent 405/404 errors from health checks
@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str):
    return templates.TemplateResponse("safari.html", {"request": request})

# 3. Execution
if __name__ == "__main__":
    # Render assigns the port dynamically; default to 8080 for local dev
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
