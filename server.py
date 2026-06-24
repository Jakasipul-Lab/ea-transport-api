from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/search/local")
def test():
    return HTMLResponse("<h1>It is finally working!</h1>")

@app.get("/")
def home():
    return HTMLResponse("<h1>Welcome to SafariRoutes</h1><a href='/search/local?q=bus'>Search for Transport</a>")

@app.get("/search/local")
def search_local(q: str):
    # ... your existing code ...
