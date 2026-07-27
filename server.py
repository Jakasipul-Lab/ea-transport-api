import os
from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    time = Column(String)          # Departure / schedule time
    price = Column(String)         # Formatted text e.g. "1,500 KES"
    price_kes = Column(Integer)    # Numeric price for sorting
    category = Column(String)      # "local" (Jakasipul) or "safari" (EAsafari)
    info = Column(String)          # Additional notes/amenities

# Auto-create tables in transport.db if they don't exist yet
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

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Double Tier Routes (Serving restored HTML directly from root)

@app.get("/")
def home():
    """Serves the main Double Tier OSARE hub."""
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/local")
@app.get("/local.html")
def local_page():
    """Serves Tier 2: Jakasipul Local Commuter Hub."""
    return FileResponse(os.path.join(BASE_DIR, "local.html"))

@app.get("/safari")
@app.get("/safari.html")
def safari_page():
    """Serves Tier 1: EAsafari Long Distance Routes."""
    return FileResponse(os.path.join(BASE_DIR, "safari.html"))

@app.head("/")
def home_head():
    """Health check endpoint for hosting platforms like Render/Railway."""
    return Response(status_code=200)

# 4. Search API Endpoint for Frontend Queries

@app.get("/api/routes")
def get_routes(
    category: str = None, 
    search: str = None, 
    db: Session = Depends(get_db)
):
    """Fetches routes filtered by category (local/safari) or search terms."""
    query = db.query(Route)
    if category:
        query = query.filter(Route.category == category)
    if search:
        query = query.filter(
            or_(
                Route.origin.ilike(f"%{search}%"),
                Route.destination.ilike(f"%{search}%"),
                Route.operator.ilike(f"%{search}%")
            )
        )
    return query.all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=10000, reload=True)
