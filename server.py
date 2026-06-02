from fastapi import FastAPI
# This import fixes the CORS crash!
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# THE BRIDGE: This allows your HTML file to talk to Railway safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites to access your API
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database of SGR Schedules
SGR_SCHEDULE = [
    {
        "train_id": "E1",
        "type": "Express",
        "from": "Nairobi",
        "to": "Mombasa",
        "departure": "15:00",
        "arrival": "20:00"
    },
    {
        "train_id": "InterCounty1",
        "type": "Inter-County",
        "from": "Mombasa",
        "to": "Nairobi",
        "departure": "08:00",
        "arrival": "14:15"
    }
]

# The API Endpoint your HTML frontend will call
@app.get("/schedules")
def get_schedules():
    return SGR_SCHEDULE

# A simple root endpoint to test if the server is online
@app.get("/")
def home():
    return {"status": "SGR Server is running perfectly!"}
