import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="OSARE Hub")

# Create the directory if it doesn't exist to prevent the RuntimeError
if not os.path.exists("static"):
    os.makedirs("static")

# Now it is safe to mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- HTML CONTENT ---
HTML_SAFARI = "<html><body><h1>Safari Hub</h1></body></html>"
HTML_DASHBOARD = "<html><body><h1>Dashboard</h1></body></html>"
HTML_ADMIN = "<html><body><h1>Admin Panel</h1></body></html>"

@app.get("/")
async def get_safari():
    return HTMLResponse(content=HTML_SAFARI)

@app.get("/dashboard")
async def get_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)

@app.get("/admin")
async def get_admin():
    return HTMLResponse(content=HTML_ADMIN)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
