import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# 1. Initialization
app = FastAPI(title="OSARE Hub")

# 2. Path Handling: Prevents file not found errors on any server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 3. Universal Routing: Handles both GET and HEAD requests
# This covers all valid paths for users and health checkers
@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    # A simple mapping to serve your files based on the requested path
    target = "safari.html"
    if "dashboard" in path:
        target = "dashboard.html"
    elif "admin" in path:
        target = "admin.html"
        
    return templates.TemplateResponse(target, {"request": request})

# 4. Production Execution
if __name__ == "__main__":
    # Dynamically picks up Render's assigned port, defaults to 8085 for your case
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
