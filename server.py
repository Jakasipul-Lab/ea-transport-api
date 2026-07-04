import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="OSARE Hub")

# Establish Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    # 1. Logic to select the file
    target = "safari.html"
    if "dashboard" in path:
        target = "dashboard.html"
    elif "admin" in path:
        target = "admin.html"
    
    # 2. Manual Render: Bypasses the dictionary hashing error entirely
    try:
        template = templates.env.get_template(target)
        content = template.render({"request": request})
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

if __name__ == "__main__":
    # Force port to the environment variable, default 8085
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
