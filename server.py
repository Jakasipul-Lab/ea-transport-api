import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Point this to your root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# If you have CSS or JS files, put them in a folder called 'static'
# If you don't have that folder, you can delete this line:
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/safari")
def get_safari():
    return FileResponse("safari.html")

@app.get("/local")
def get_local():
    return FileResponse("local.html")

@app.get("/about")
def get_about():
    return FileResponse("about.html")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/{page_name}.html")
async def serve_other_pages(page_name: str):
    # This specifically looks for your .html files
    return FileResponse(os.path.join(BASE_DIR, f"{page_name}.html"))
