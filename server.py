import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="OSARE Hub")

# Establish the path dynamically for production safety
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Error handling for missing directory
if not os.path.exists(TEMPLATES_DIR):
    print(f"CRITICAL ERROR: Templates directory not found at {TEMPLATES_DIR}")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    # Logic to select the correct template
    target = "safari.html"
    if "dashboard" in path:
        target = "dashboard.html"
    elif "admin" in path:
        target = "admin.html"
    
    # Try-except block to pinpoint the exact source of an Internal Server Error
    try:
        return templates.TemplateResponse(target, {"request": request})
    except Exception as e:
        return HTMLResponse(content=f"<h1>Template Error:</h1><p>{str(e)}</p>", status_code=500)

if __name__ == "__main__":
    # Pull port from environment or default to 8085
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
