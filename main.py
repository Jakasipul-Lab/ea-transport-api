import os
from fastapi import FastAPI
from fastapi.responses import FileResponse # <--- You were missing this import!

app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse('index.html') # Changed from message to your index file

@app.get("/osare")
def get_osare():
    return FileResponse('osare.html')

@app.get("/local")
def get_local():
    return FileResponse('local.html')

@app.get("/safari")
def get_safari():
    return FileResponse('safari.html')

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
