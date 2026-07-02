from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uuid
Base=declarative_base()
engine=create_engine("sqlite:///./bookings.db",connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(bind=engine)
class Booking(Base):
 __tablename__="bookings"
 id=Column(Integer,primary_key=True)
 token=Column(String,unique=True,default=lambda:f"OSARE_TRK_{uuid.uuid4().hex[:6].upper()}")
 tier=Column(String);name=Column(String);email=Column(String);date=Column(String)
Base.metadata.create_all(bind=engine)
app=FastAPI()
def get_db():db=SessionLocal();try:yield db;finally:db.close()
@app.get("/",response_class=HTMLResponse)
def home():return'<!DOCTYPE html><html><head><title>EA Safari Routes</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{font-family:sans-serif;text-align:center;padding:40px;background:#f0fdf4}h1{color:#16a34a}.card{display:inline-block;width:260px;margin:12px;padding:20px;background:white;border-radius:12px;box-shadow:0 2px 8px #0001}.btn{display:block;margin-top:12px;padding:12px;background:#16a34a;color:white;text-decoration:none;border-radius:8px;font-weight:600}</style></head><body><h1>EA Safari Routes ✅</h1><p>Choose Your Corridor</p><div class="card"><h3>1. Local Tier</h3><a class="btn" href="/local">Open Local →</a></div><div class="card"><h3>2. Safari Tier</h3><a class="btn" href="/safari">Open Safari →</a></div><br><br><a href="/leads" style="color:#2563eb">Admin Leads</a></body></html>'
@app.get("/local")
def local():return FileResponse("local.html")
@app.get("/safari")
def safari():return FileResponse("safari.html")
@app.post("/book")
def submit(tier=Form(...),name=Form(...),email=Form(...),date=Form(...),db:Session=Depends(get_db)):b=Booking(tier=tier,name=name,email=email,date=date);db.add(b);db.commit();db.refresh(b);return RedirectResponse(f"/thank-you?token={b.token}",303)
@app.get("/thank-you",response_class=HTMLResponse)
def ok(token:str):return f'<body style="text-align:center;padding:60px;font-family:sans-serif"><h1>Booked ✅</h1><p>Token: <b>{token}</b></p><a href="/">Home</a></body>'
@app.get("/leads",response_class=HTMLResponse)
def leads(db:Session=Depends(get_db)):rows="".join([f"<tr><td>{b.token}</td><td>{b.tier}</td><td>{b.name}</td><td>{b.email}</td></tr>" for b in db.query(Booking).order_by(Booking.id.desc()).all()])or"<tr><td colspan=4>No leads yet</td></tr>";return f'<body style="padding:20px;font-family:sans-serif"><h2>Admin Leads</h2><table border=1 cellpadding=8><tr><th>Token</th><th>Tier</th><th>Name</th><th>Email</th></tr>{rows}</table><br><a href="/">Home</a></body>'