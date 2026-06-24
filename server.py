from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/search/local")
def test():
    return HTMLResponse("<h1>It is finally working!</h1>")
