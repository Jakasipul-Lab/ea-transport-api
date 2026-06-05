import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# --- DATABASE SETUP ---
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://mongo:rjAnxIXFSEwQrJSzPDzsKXDWBATwPcsZ@shortline.proxy.rlwy.net:13892"
)

client = AsyncIOMotorClient(MONGO_URL)
db = client.safariroutes
bookings_collection = db.bookings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- TRACKING ---
async def record_booking(provider, route):
    booking_data = {
        "timestamp": datetime.now().isoformat(),
        "provider": provider,
        "route": route,
        "status": "PENDING"
    }
    await bookings_collection.insert_one(booking_data)

# --- ROUTES ---

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/about")
def about():
    return FileResponse("about.html")

import uuid

@app.get("/book/sgr/{route_id}")
async def book_sgr(route_id: str):
    code = f"SR-{uuid.uuid4().hex[:6]}"

    print("Tracking Code:", code)

    return RedirectResponse(
        url=f"https://metickets.krc.co.ke?ref=safariroutes&route={route_id}&code={code}"
``
    )
