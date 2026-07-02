from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uuid

Base = declarative_base()
engine = create_engine("sqlite:///./bookings.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, default=lambda: f"OSARE_TRK_{uuid.uuid4().hex[:6].upper()}")
    name = Column(String); email = Column(String); date = Column(String)

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db(): 
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html><head><title>EA Safari Routes</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:sans-serif;text-align:center;padding:60px;background:#f0fdf4}h1{color:#16a34a}.btn{display:inline-block;padding:16px 28px;background:#16a34a;color:white;text-decoration:none;border-radius:10px;font-size:18px;margin-top:20px}</style></head>
<body>
  <h1>EA Safari Routes ✅</h1>
  <p>Live Bookings Are Open</p>
  <a class="btn" href="/book">Live Book Now →</a>
  <br><br><a href="/leads" style="color:#2563eb">Admin Leads</a>
</body></html>"""

@app.get("/book", response_class=HTMLResponse) 
def book(): 
    return """<!DOCTYPE html><html><body style="max-width:420px;margin:40px auto;font-family:sans-serif">
  <h2>Book Your Safari - $150</h2>
  <form method=post><input name=name placeholder="Full Name" required style="width:100%;padding:10px;margin:8px 0;"><br>
  <input name=email type=email placeholder="Email" required style="width:100%;padding:10px;margin:8px 0;"><br>
  <input name=date type=date required style="width:100%;padding:10px;margin:8px 0;"><br>
  <button style="width:100%;padding:12px;background:#16a34a;color:white;border:0;border-radius:8px;">Confirm Booking</button></form></body></html>"""

@app.post("/book")
def submit(name=Form(...), email=Form(...), date=Form(...), db:Session=Depends(get_db)):
    b=Booking(name=name,email=email,date=date); db.add(b); db.commit(); db.refresh(b)
    return RedirectResponse(f"/thank-you?token={b.token}",303)

@app.get("/thank-you", response_class=HTMLResponse)
def ok(token:str): return f"""<body style="text-align:center;padding:60px;font-family:sans-serif"><h1>Booked ✅</h1><p>Token: <b>{token}</b></p><a href="/">Home</a></body>"""

@app.get("/leads", response_class=HTMLResponse)
def leads(db:Session=Depends(get_db)): 
    rows="".join([f"<tr><td>{b.token}</td><td>{b.name}</td><td>{b.email}</td><td>{b.date}</td></tr>" for b in db.query(Booking).order_by(Booking.id.desc()).all()]) or "<tr><td colspan=4>No leads yet</td></tr>"
    return f"""<body style="padding:20px;font-family:sans-serif"><h2>Admin Leads</h2><table border=1 cellpadding=8><tr><th>Token</th><th>Name</th><th>Email</th><th>Date</th></tr>{rows}</table><br><a href="/">Home</a></body>"""
