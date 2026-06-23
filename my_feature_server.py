import os
import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

import os
import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS config (FIXED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Homepage
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# ✅ Homepage
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")
``
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# 3. Your health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 4. A placeholder route showing how you will pull Neon data later
@app.get("/api/transport-data")
def get_transport_data():
    # This checks if Render is successfully seeing your Neon credentials
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return JSONResponse(
            status_code=500, 
            content={"error": "Database connection string is missing in Render settings!"}
        )
    
    # Your database query logic will go here
    return {"message": "Database configuration detected. Ready to build query logic."}
