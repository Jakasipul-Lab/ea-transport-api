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
def read_root():
    return FileResponse("index.html")

@app.get("/about")
def about_page():
    return FileResponse("AboutMe.html")

@app.get("/book/sgr/{route_id}")
async def book_sgr(route_id: str):
    await record_booking("SGR", route_id)
    return RedirectResponse(
        url=f"https://metickets.krc.co.ke?ref=safariroutes&route={route_id}"
    )

@app.get("/book/bus/{operator}/{route_id}")
async def book_bus(operator: str, route_id: str):
    await record_booking(operator, route_id)
    return RedirectResponse(
        url=f"https://official-{operator}-site.com/book?ref=safariroutes"
    )
