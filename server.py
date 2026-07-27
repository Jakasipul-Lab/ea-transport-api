import os
from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. Database setup (Modern SQLAlchemy 2.0 syntax)
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
    time = Column(String)          # Departure / schedule time
    price = Column(String)         # Formatted text e.g. "1,500 KES"
    price_kes = Column(Integer)    # Numeric price for sorting
    category = Column(String)      # "local" (Jakasipul) or "safari" (EAsafari)
    info = Column(String)          # Additional notes/amenities

# Ensure tables exist in transport.db
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

# 4. Search API Endpoints
@app.get("/api/search")
@app.get("/api/routes")
def get_routes(
    category: str = None, 
    search: str = Query(None, alias="q"), 
    q: str = None,
    db: Session = Depends(get_db)
):
    search_term = search or q
    query = db.query(Route)
    
    if category:
        query = query.filter(Route.category == category)
    if search_term:
        query = query.filter(
            or_(
                Route.origin.ilike(f"%{search_term}%"),
                Route.destination.ilike(f"%{search_term}%"),
                Route.operator.ilike(f"%{search_term}%")
            )
        )
    return query.all()

@app.get("/search/{category}")
def search_by_category(
    category: str, 
    q: str = Query(None), 
    db: Session = Depends(get_db)
):
    query = db.query(Route).filter(Route.category == category)
    if q:
        query = query.filter(
            or_(
                Route.origin.ilike(f"%{q}%"),
                Route.destination.ilike(f"%{q}%"),
                Route.operator.ilike(f"%{q}%")
            )
        )
    return query.all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=10000, reload=True)
