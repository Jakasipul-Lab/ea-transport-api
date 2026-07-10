import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Added for safe static routing
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
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
    category = Column(String) # 'local' or 'safari'

Base.metadata.create_all(bind=engine)

# Seed data
db = SessionLocal()
if db.query(Route).count() == 0:
    sample_routes = [
        Route(operator="Madaraka Express (SGR)", origin="Nairobi", destination="Mombasa", time="08:00 AM", price="1,500 KES", category="local"),
        Route(operator="Madaraka Express (SGR)", origin="Mombasa", destination="Nairobi", time="03:00 PM", price="1,500 KES", category="local"),
        Route(operator="Mash East Africa", origin="Nairobi", destination="Mombasa", time="09:00 PM", price="1,800 KES", category="local"),
        Route(operator="Easy Coach", origin="Nairobi", destination="Kisumu", time="08:00 AM", price="1,600 KES", category="local"),
        Route(operator="North Rift Sacco", origin="Nairobi", destination="Eldoret", time="Leaves hourly", price="1,200 KES", category="local"),
        Route(operator="Safarilink Aviation", origin="Nairobi", destination="Maasai Mara", time="Daily", price="8,500 KES", category="safari"),
        Route(operator="African Spice Car Hire", origin="Nairobi", destination="Anywhere", time="Immediate", price="5,000 KES/day", category="safari"),
        Route(operator="Discover Kenya Tours", origin="Mombasa", destination="Tsavo East", time="Full Day", price="12,000 KES", category="safari")
    ]
    db.add_all(sample_routes)
    db.commit()
db.close()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 1. Your API search endpoint stays exactly here
@app.get("/api/search")
def search(q: str = Query(None), category: str = Query("local")):
    db = SessionLocal()
    query = db.query(Route).filter(Route.category == category)
    if q:
        words = q.lower().replace(" to ", " ").split()
        for word in words:
            query = query.filter(
                (Route.origin.ilike(f"%{word}%")) | 
                (Route.destination.ilike(f"%{word}%")) | 
                (Route.operator.ilike(f"%{word}%"))
            )
    results = query.all()
    db.close()
    return [{"op": r.operator, "time": r.time, "price": r.price} for r in results]

# 2. REMOVED the old home() and catch_all() routes.
# Instead, we mount the current directory. FastAPI handles index.html as root automatically,
# resolves HEAD requests properly, and routes all your files like advertisment.html smoothly.
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    # Using string "server:app" allows Uvicorn to safely track reload states
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
