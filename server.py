import os
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, or_ # FIX 1: add or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./transport.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    operator = Column(String)
    origin = Column(String)
    destination = Column(String)
    price_kes = Column(Integer) # for sorting cheapest
    price_text = Column(String) # "1,200 KES"
    type = Column(String) # Matatu, Bus, Train
    info = Column(String) # "Bay 12"

Base.metadata.create_all(bind=engine)

# Seed data with requested terms
db = SessionLocal()
if db.query(Route).count() == 0:
    sample_routes = [
        # LOCAL
        Route(operator="Madaraka Express (SGR)", origin="Nairobi", destination="Mombasa", time="08:00 AM", price="1,500 KES", category="local"),
        Route(operator="Madaraka Express (SGR)", origin="Mombasa", destination="Nairobi", time="03:00 PM", price="1,500 KES", category="local"),
        Route(operator="Mash East Africa", origin="Nairobi", destination="Mombasa", time="09:00 PM", price="1,800 KES", category="local"),
        Route(operator="Easy Coach", origin="Nairobi", destination="Kisumu", time="08:00 AM", price="1,600 KES", category="local"),
        Route(operator="North Rift Sacco", origin="Nairobi", destination="Eldoret", time="Leaves hourly", price="1,200 KES", category="local"),
        Route(operator="2NK Sacco", origin="Nairobi", destination="Ngong", time="Every 10min", price="80-120 KES", category="local"),
        Route(operator="Metro Trans", origin="Nairobi", destination="Rongai", time="24/7", price="60-100 KES", category="local"),
        
        # SAFARI / TOURIST / HOTELS
        Route(operator="Safarilink Aviation", origin="Nairobi", destination="Masai Mara", time="Daily Flights", price="8,500 KES", category="safari"),
        Route(operator="Mara Gates Safaris", origin="Nairobi", destination="Masai Mara", time="3 Days Safari", price="45,000 KES", category="safari"),
        Route(operator="Mount Kilimanjaro Treks", origin="Nairobi", destination="Kilimanjaro", time="7 Days Trek", price="120,000 KES", category="safari"),
        Route(operator="Serena Hotel & Resort", origin="Mombasa", destination="Beach Stay", time="Per Night", price="15,000 KES", category="safari"),
        Route(operator="Safari Park Hotel", origin="Nairobi", destination="City Resort", time="Per Night", price="12,000 KES", category="safari"),
        Route(operator="African Spice Car Hire", origin="Nairobi", destination="Kilimanjaro Transfer", time="Immediate", price="25,000 KES", category="safari"),
        Route(operator="Mara Hotel & resort", origin="Masai Mara", destination="Luxury Stay", time="Per Night", price="20,000 KES", category="safari")
    ]
    db.add_all(sample_routes)
    db.commit()
db.close()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/search")
def search(q: str = Query(None), category: str = Query("local")):
    db = SessionLocal()
    query = db.query(Route).filter(Route.category == category)
    if q:
        # FIX 2: use or_() instead of | chain. Also search all words
        words = q.lower().replace("/", " ").replace(" to ", " ").split()
        for word in words:
            query = query.filter(
                or_(
                    Route.origin.ilike(f"%{word}%"), 
                    Route.destination.ilike(f"%{word}%"), 
                    Route.operator.ilike(f"%{word}%")
                )
            )
    results = query.all()
    db.close()
    return [{"op": r.operator, "origin": r.origin, "dest": r.destination, "time": r.time, "price": r.price} for r in results]

# 2. HOMEPAGE FIXED (GET + HEAD)
@app.get("/")
@app.head("/")
async def serve_root():
    return FileResponse("index.html")

# 3. DYNAMIC HTML ROUTER FOR ALL YOUR REAL PAGES
@app.get("/{page_name}")
@app.head("/{page_name}")
async def serve_any_page(page_name: str):
    clean_name = page_name.replace(".html", "")
    file_path = f"{clean_name}.html"

    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    return FileResponse("index.html")

# 4. Mount static directory LAST for assets - SAFE VERSION
static_dir = "static"
if os.path.exists(static_dir) and os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: '{static_dir}' directory not found. Skipping static files.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
