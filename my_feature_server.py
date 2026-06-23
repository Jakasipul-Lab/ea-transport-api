import os
import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Homepage (SIMPLE + SAFE)
@app.get("/")
def read_root():
    return {"status": "ok"}

# ✅ Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ✅ API route
@app.get("/api/transport-data")
def get_transport_data():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        return JSONResponse(
            status_code=500,
            content={"error": "Database connection string is missing"}
        )

    return {"message": "API working correctly"}

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI()

# This tells the app to look in a folder named 'static' for your files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    # You need to return the file or use a template engine
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')
