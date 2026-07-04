import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# 1. Initialize App
app = FastAPI(title="OSARE Hub")

# 2. Path Setup: Ensures Render finds your files regardless of the environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# 3. Setup Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 4. Routes: Every route explicitly accepts HEAD for health checks
@app.get("/", methods=["GET", "HEAD"])
async def home(request: Request):
    return templates.TemplateResponse("safari.html", {"request": request})

@app.get("/dashboard", methods=["GET", "HEAD"])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin", methods=["GET", "HEAD"])
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# 5. Catch-All: Prevents 405/404 errors if a health checker hits an undefined path
@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str):
    return templates.TemplateResponse("safari.html", {"request": request})

# 6. Execution: Dynamically binds to the port assigned by the environment
if __name__ == "__main__":
    # Render sets the PORT variable; if not found, it defaults to 8085 as per your finding
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
