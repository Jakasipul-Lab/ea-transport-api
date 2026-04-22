from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# SAFETY WRAPPER: This stops the 'libpq' crash from killing the app
try:
    import psycopg2
    HAS_DB = True
except ImportError:
    HAS_DB = False
    print("CRITICAL: libpq.so.5 not found. Database features will be disabled.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "database_library_loaded": HAS_DB,
        "message": "API is running" if HAS_DB else "API running in SAFE MODE (No DB)"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
