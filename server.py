import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/{path:path}")
async def catch_all(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse("index.html")
