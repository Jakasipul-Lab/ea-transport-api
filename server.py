import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
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

# Seed data with more "real" routes
db = SessionLocal()
if db.query(Route).count() == 0:
    sample_routes = [
        # LOCAL
        Route(operator="Madaraka Express (SGR)", origin="Nairobi", destination="Mombasa", time="08:00 AM", price="1,500 KES", category="local"),
        Route(operator="Madaraka Express (SGR)", origin="Mombasa", destination="Nairobi", time="03:00 PM", price="1,500 KES", category="local"),
        Route(operator="Mash East Africa", origin="Nairobi", destination="Mombasa", time="09:00 PM", price="1,800 KES", category="local"),
        Route(operator="Easy Coach", origin="Nairobi", destination="Kisumu", time="08:00 AM", price="1,600 KES", category="local"),
        Route(operator="Easy Coach", origin="Kisumu", destination="Nairobi", time="09:30 PM", price="1,600 KES", category="local"),
        Route(operator="North Rift Sacco", origin="Nairobi", destination="Eldoret", time="Leaves hourly", price="1,200 KES", category="local"),
        Route(operator="Guardian Angel", origin="Nairobi", destination="Busia", time="07:00 AM", price="1,500 KES", category="local"),
        Route(operator="Modern Coast", origin="Mombasa", destination="Kampala", time="05:00 PM", price="4,500 KES", category="local"),
        
        # SAFARI / TOURIST
        Route(operator="Safarilink Aviation", origin="Nairobi", destination="Maasai Mara", time="Daily", price="8,500 KES", category="safari"),
        Route(operator="AirKenya", origin="Nairobi", destination="Amboseli", time="10:00 AM", price="9,200 KES", category="safari"),
        Route(operator="African Spice Car Hire", origin="Nairobi", destination="Anywhere", time="Immediate", price="5,000 KES/day", category="safari"),
        Route(operator="Mara Gates Safaris", origin="Nairobi", destination="Maasai Mara", time="3 Days / 2 Nights", price="45,000 KES", category="safari"),
        Route(operator="Discover Kenya Tours", origin="Mombasa", destination="Tsavo East", time="Full Day", price="12,000 KES", category="safari")
    ]
    db.add_all(sample_routes)
    db.commit()
db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

@app.get("/api/search")
def search(q: str = Query(None), category: str = Query("local")):
    db = SessionLocal()
    query = db.query(Route).filter(Route.category == category)
    if q:
        # Flexible search: split query and search for keywords
        words = [w for w in q.replace(" to ", " ").replace("-", " ").replace(">", " ").split() if w.lower() not in ["to", "from", "via"]]
        for word in words:
            query = query.filter(
                (Route.origin.ilike(f"%{word}%")) | 
                (Route.destination.ilike(f"%{word}%")) | 
                (Route.operator.ilike(f"%{word}%"))
            )
    results = query.all()
    db.close()
    return [{"op": r.operator, "time": r.time, "price": r.price} for r in results]

@app.get("/{path:path}")
def catch_all(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    if os.path.exists(path):
        return FileResponse(path)
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
