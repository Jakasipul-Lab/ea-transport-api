import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Your routes - defined only once
@app.get("/")
def read_root():
    return FileResponse('index.html')

@app.get("/osare")
def get_osare():
    return FileResponse('osare.html')

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
