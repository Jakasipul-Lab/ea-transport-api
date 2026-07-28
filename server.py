import os
from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. Database setup
DATABASE_URL = "sqlite:///./transport.db"
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

# 2. FastAPI Application
app = FastAPI(title="OSARE Double Tier Transport API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. HTML Route Handlers
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
@app.get("/local.html")
def local_page():
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
@app.get("/safari.html")
def safari_page():
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.head("/")
def home_head():
    return Response(status_code=200)

# Helper function to query routes safely
def query_routes(db: Session, category: str = None, from_: str = None, to: str = None, q: str = None):
    query = db.query(Route)
    
    if category:
        # Normalize category lookup just in case
        clean_cat = "safari" if category.lower() in ["safari", "easafari"] else "local"
        query = query.filter(Route.category == clean_cat)
        
    if from_:
        query = query.filter(Route.origin.ilike(f"%{from_}%"))
    if to:
        query = query.filter(Route.destination.ilike(f"%{to}%"))
        
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Route.origin.ilike(search_term),
                Route.destination.ilike(search_term),
                Route.operator.ilike(search_term),
                Route.info.ilike(search_term)
            )
        )
        
    return query.all()

# 4. Core Search API Endpoints
@app.get("/api/search")
@app.get("/api/routes")
def get_routes(
    category: str = Query(None),
    from_: str = Query(None, alias="from"),
    to: str = Query(None),
    q: str = Query(None),
    db: Session = Depends(get_db)
):
    results = query_routes(db, category=category, from_=from_, to=to, q=q)
    
    # Convert SQLAlchemy models to clean dictionaries for the frontend
    serialized_results = [
        {
            "id": r.id,
            "operator": r.operator,
            "origin": r.origin,
            "destination": r.destination,
            "time": r.time,
            "price": r.price,
            "price_kes": r.price_kes,
            "category": r.category,
            "info": r.info
        } for r in results
    ]
    
    return {
        "tier": category or "all",
        "commission": "5%",
        "count": len(serialized_results),
        "results": serialized_results
    }

# 5. Public Search Route for Frontend
@app.get("/public/search")
def public_search(
    from_: str = Query(None, alias="from"), 
    to: str = Query(None), 
    tier: str = Query("easafari"),
    db: Session = Depends(get_db)
):
    # Map incoming frontend tier names to database categories reliably
    category_mapping = {
        "easafari": "safari",
        "safari": "safari",
        "jakasipul": "local",
        "local": "local"
    }
    category = category_mapping.get(tier.lower(), "safari")
    
    return get_routes(category=category, from_=from_, to=to, db=db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=10000, reload=True)
