import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Your routes - defined only once
@app.get("/")
def read_root():
    return FileResponse('index.html')

from fastapi import Request
from fastapi.templating import Jinja2Templates

# Add this at the top of your file
templates = Jinja2Templates(directory=".")

@app.get("/search")
def search(q: str, request: Request):
    # This is where your search logic goes
    # For now, it just prints what they searched for to the server logs
    print(f"User searched for: {q}")
    
    # You can return a result page or simple text
    return {"message": f"You searched for: {q}"}

@app.get("/osare")
def get_osare():
    return FileResponse('osare.html')

@app.get("/search")
def search(q: str):
    # This is the logic that receives the 'q' from the search bar
    # For now, it will just show the search result
    return {"message": f"You searched for: {q}. Results page coming soon!"}

@app.get("/local")
def get_local():
    return FileResponse('local.html')

@app.get("/safari")
def get_safari():
    return FileResponse('safari.html')

@app.get("/about")
def get_about():
    return FileResponse('about.html')

@app.get("/support")
def get_support():
    return FileResponse('support.html')

# Server startup - defined only once
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
