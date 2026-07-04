import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="OSARE Hub")

# Set up the absolute path for templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    # Logic to select the file
    target = "safari.html"
    if "dashboard" in path:
        target = "dashboard.html"
    elif "admin" in path:
        target = "admin.html"
    
    # UNIVERSAL FIX: Pass 'request' as an argument, not inside a nested dict
    # This avoids the 'tuple' and 'unhashable' errors entirely
    return templates.TemplateResponse(target, {"request": request})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
