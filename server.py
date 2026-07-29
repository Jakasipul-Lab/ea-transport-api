import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------
# ✅ PAGES
# --------------------------------------
@app.get("/")
def home(): 
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
@app.get("/local.html")
def local_page(): 
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse("Error: index.html not found.", status_code=404)
    return FileResponse(file_path)

@app.head("/")
def home_head():
    return Response(status_code=200)

# --- PASTE THE DYNAMIC PAGE ROUTE HERE ---
@app.get("/{page_name}")
@app.get("/{page_name}.html")
def serve_other_pages(page_name: str):
    file_path = os.path.join(BASE_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    file_path_alt = os.path.join(BASE_DIR, page_name)
    if os.path.exists(file_path_alt):
        return FileResponse(file_path_alt)
        
    return HTMLResponse("Error: Page not found.", status_code=404)
# ----------------------------------------

@app.get("/api/search")
def api_search(category: str = Query(...), q: str = ""):
    # ... rest of your search code ...

@app.get("/safari")
@app.get("/safari.html")
def safari_page(): 
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

# --- INSERT THIS BLOCK HERE TO HANDLE ALL OTHER HTML FILES AUTOMATICALLY ---
@app.get("/{page_name}")
@app.get("/{page_name}.html")
def serve_other_pages(page_name: str):
    file_path = os.path.join(BASE_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    file_path_alt = os.path.join(BASE_DIR, page_name)
    if os.path.exists(file_path_alt):
        return FileResponse(file_path_alt)
        
    return {"error": "Page not found"}
# --------------------------------------------------------------------------

@app.head("/")
def home_head(): 
    return Response(status_code=200)
