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

# Model definition
class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    operator = Column(String)
    origin = Column(String)
    destination = Column(String)
    time = Column(String)
    price = Column(String)
    price_kes = Column(Integer)
    category = Column(String)
    info = Column(String)

# CRITICAL FIX: Create database tables automatically if transport.db is missing/empty
Base.metadata.create_all(bind=engine)

# 2. FastAPI Setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Routes & Endpoints
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/local")
@app.get("/local.html")
def local_page():
    return FileResponse(os.path.join(STATIC_DIR, "local.html"))

@app.get("/safari")
@app.get("/safari.html")
def safari_page():
    return FileResponse(os.path.join(STATIC_DIR, "safari.html"))

@app.head("/")
def home_head():
    return Response(status_code=200)

# Sample API Endpoint for routes search
@app.get("/api/routes")
def get_routes(category: str = None, search: str = None, db: Session = Depends(get_db)):
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
