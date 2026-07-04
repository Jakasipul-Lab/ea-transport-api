import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="OSARE Hub")

# Force the path to be the current directory + templates
# This removes ambiguity about where "BASE_DIR" starts
TEMPLATES_DIR = os.path.join(os.getcwd(), "templates")

# Debugging check: if this prints a list without your files, the files aren't on Render
print(f"DEBUG: Looking for templates in: {TEMPLATES_DIR}")
if os.path.exists(TEMPLATES_DIR):
    print(f"DEBUG: Files found in directory: {os.listdir(TEMPLATES_DIR)}")
else:
    print("CRITICAL: The 'templates' directory does not exist in the root!")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    target = "safari.html"
    if "dashboard" in path:
        target = "dashboard.html"
    elif "admin" in path:
        target = "admin.html"
    
    try:
        # Use the standard template response
        return templates.TemplateResponse(target, {"request": request})
    except Exception as e:
        return HTMLResponse(content=f"<h1>Debug Info:</h1><p>Searching in {TEMPLATES_DIR}</p><p>Error: {str(e)}</p>", status_code=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
