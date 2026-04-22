from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

import psycopg2
import dj_database_url

# 1. Load variables
load_dotenv()

# 2. Initialize App
app = FastAPI()

# 3. CORS (Allows your frontend to talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Root Route
@app.get("/")
def read_root():
    return {"message": "East African Transport API - Online"}

# 5. Health Check (What Railway looks for)
@app.get("/health")
def health():
    return {"status": "healthy"}

# 6. Start the Server (Crucial for Health Check)
if __name__ == "__main__":
    import uvicorn
    # This automatically picks up 8080 from Railway
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
