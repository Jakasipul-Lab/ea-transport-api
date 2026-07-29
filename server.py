from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. THIS SERVES YOUR HOMEPAGE FIRST
# It will load index.html when someone goes to easaafariroutes.com
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# 2. THIS IS ONLY FOR DATA - your JS will call this
@app.get("/api/search")
def get_routes(category: str = Query(None), q: str = Query(None)):
    ROUTES = [
        {"id": 1, "operator": "Super Metro", "origin": "Nairobi CBD", "destination": "Rongai", "time": "Every 5 mins", "price": "KES 100", "price_kes": 100, "category": "local", "info": "Express Sacco"},
        {"id": 2, "operator": "Githurai Shuttle", "origin": "Nairobi CBD", "destination": "Githurai 45", "time": "Every 3 mins", "price": "KES 50", "price_kes": 50, "category": "local", "info": "Via Thika Rd"},
        {"id": 3, "operator": "Kangemi Matatus", "origin": "Nairobi CBD", "destination": "Kangemi", "time": "Every 5 mins", "price": "KES 60", "price_kes": 60, "category": "local", "info": "Via Westlands"},
        {"id": 4, "operator": "Mara Safaris", "origin": "Nairobi", "destination": "Masai Mara", "time": "06:00 AM", "price": "KES 15000", "price_kes": 15000, "category": "safari", "info": "Land Cruiser 4x4"},
        {"id": 5, "operator": "Amboseli Express", "origin": "Nairobi", "destination": "Amboseli", "time": "07:30 AM", "price": "KES 4500", "price_kes": 4500, "category": "safari", "info": "Tour Van"},
    ]
    results = ROUTES
    if category:
        results = [r for r in results if r["category"] == category]
    if q:
        q = q.lower()
        results = [r for r in results if q in r["origin"].lower() or q in r["destination"].lower() or q in r["operator"].lower()]
    return results
