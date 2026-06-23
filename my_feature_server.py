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

# ✅ BASE DIR (needed for file paths)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def read_root():
    return FileResponse(...)

# ✅ Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ✅ Logging function
def log_lead(destination, service_type):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")

# ✅ API route
@app.get("/api/transport-data")
def get_transport_data():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        return JSONResponse(
            status_code=500,
            content={"error": "Database connection string is missing"}
        )

    return {"message": "Database configuration detected"}
