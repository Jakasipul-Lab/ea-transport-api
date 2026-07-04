import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="OSARE Hub")

# --- EMBEDDED HTML CONTENT ---
# Replace the text inside these strings with the actual content of your files.
HTML_SAFARI = "<html><body><h1>Safari Hub</h1><p>Welcome to the main page.</p></body></html>"
HTML_DASHBOARD = "<html><body><h1>Dashboard</h1><p>Welcome to the user area.</p></body></html>"
HTML_ADMIN = "<html><body><h1>Admin Panel</h1><p>Restricted access only.</p></body></html>"

@app.api_route("/{path:path}", methods=["GET", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    # Logic to select the correct content based on the URL path
    if "dashboard" in path:
        content = HTML_DASHBOARD
    elif "admin" in path:
        content = HTML_ADMIN
    else:
        content = HTML_SAFARI
    
    return HTMLResponse(content=content)

if __name__ == "__main__":
    # Dynamically detects the PORT provided by Render or defaults to 8005 for local testing
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
