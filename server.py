import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# --- DATABASE SETUP ---
# Replace the URL below with your actual MongoDB connection string
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://your_user:your_password@cluster.mongodb.net/safariroutes?retryWrites=true&w=majority")
client = AsyncIOMotorClient(MONGO_URL)
db = client.safariroutes  # Database name
bookings_collection = db.bookings # Collection name

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- THE NEW PERSISTENT TRACKING LOG ---
async def record_booking(provider, route):
    # This records the referral into your permanent database
    booking_data = {
        "timestamp": datetime.now().isoformat(),
        "provider": provider,
        "route": route,
        "status": "PENDING"
    }
    await bookings_collection.insert_one(booking_data)

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/book/sgr/{route_id}")
async def book_sgr(route_id: str):
    await record_booking("SGR", route_id)
    return RedirectResponse(url=f"https://metickets.krc.co.ke?ref=safariroutes&route={route_id}")

@app.get("/book/bus/{operator}/{route_id}")
async def book_bus(operator: str, route_id: str):
    await record_booking(operator, route_id)
    return RedirectResponse(url=f"https://official-{operator}-site.com/book?ref=safariroutes")
