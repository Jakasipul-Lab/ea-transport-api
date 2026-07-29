from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "OSARE Backend Running"}

@app.get("/api/search")
def search_routes(q: str = Query(None), category: str = Query("local")):
    dummy_data = [
        {"id": 1, "name": "Jakasipul Route", "category": "local", "price": 200},
        {"id": 2, "name": "Easafari Route", "category": "local", "price": 350},
        {"id": 3, "name": "Advertisement Banner", "category": "local", "price": 100},
    ]
    
    results = dummy_data
    
    if category:
        results = [r for r in results if r["category"] == category]
    
    if q:
        results = [r for r in results if q.lower() in r["name"].lower()]
        
    return results
