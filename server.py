import os
from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base, sessionmaker, Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'transport.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    operator = Column(String)
    origin = Column(String)
    destination = Column(String)
    time = Column(String)
    price = Column(String)
    price_kes = Column(Integer)
    category = Column(String)  # "local" or "safari"
    info = Column(String)

Base.metadata.create_all(bind=engine)

# Auto-seed if DB is empty
db = SessionLocal()
if db.query(Route).count() == 0:
    sample_routes = [
        Route(operator="Mara Land Cruiser Safaris", origin="Nairobi CBD / JKIA", destination="Masai Mara (Talek / Sekenani Gate)", time="06:00 AM Daily", price="KES 15,000", price_kes=15000, category="safari", info="4x4 Tour Van / Land Cruiser"),
        Route(operator="Amboseli Express Shuttles", origin="Nairobi", destination="Amboseli National Park", time="07:30 AM Daily", price="KES 4,500", price_kes=4500, category="safari", info="Tourist Overland Shuttle"),
        Route(operator="Madaraka Express SGR", origin="Nairobi Terminus", destination="Mombasa Terminus", time="08:00 AM & 03:00 PM", price="KES 1,500", price_kes=1500, category="safari", info="High-speed rail"),
        Route(operator="Super Metro", origin="Nairobi CBD (Archives)", destination="Rongai / Kiserian", time="Every 5 mins", price="KES 100", price_kes=100, category="local", info="Express commuter"),
        Route(operator="Githurai Shuttle", origin="Nairobi CBD", destination="Githurai 45", time="Every 3 mins", price="KES 50", price_kes=50, category="local", info="Via Thika Rd"),
        Route(operator="Kangemi Matatus", origin="Nairobi CBD", destination="Kangemi", time="Every 5 mins", price="KES 60", price_kes=60, category="local", info="Via Westlands"),
    ]
    db.add_all(sample_routes)
    db.commit()
db.close()

app = FastAPI(title="OSARE Double Tier Transport API")

# PING TEST
@app.get("/ping")
def ping():
    return {"pong": True, "version": "v4-complete"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"status": "Server Running", "message": "OSARE API is live"}

# RETURN ARRAY DIRECTLY
@app.get("/api/search")
def get_routes(
    category: str = Query(None),
    q: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Route)
    
    if category:
        clean_cat = "safari" if category.lower() == "safari" else "local"
        query = query.filter(Route.category == clean_cat)
    if q:
        search_term = f"%{q}%"
        query = query.filter(or_(Route.origin.ilike(search_term), Route.destination.ilike(search_term), Route.operator.ilike(search_term)))
        
    results = query.all()
    if not results:
        results = db.query(Route).all()

    return [
        {
            "id": r.id, "operator": r.operator, "origin": r.origin, 
            "destination": r.destination, "time": r.time, "price": r.price,
            "price_kes": r.price_kes, "category": r.category, "info": r.info
        } for r in results
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
