from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uuid
from datetime import datetime

DATABASE_URL = "sqlite:///./bookings.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, default=lambda: f"OSARE_TRK_{uuid.uuid4().hex[:6].upper()}")
    name = Column(String)
    email = Column(String)
    date = Column(String)
    service = Column(String, default="Savannah Group Tour")
    value_usd = Column(String, default="150")
    notes = Column(String, default="Lead transmitted successfully.")

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html><html><head><title>Livebooking Engine</title></head>
    <body style="text-align:center;padding:50px;font-family:sans-serif">
      <h1>Livebooking Engine is Live ✅</h1>
      <a href="/book" style="padding:12px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:8px">Book Now</a>
      <br><br><a href="/leads">View Leads</a>
    </body></html>"""

@app.get("/book", response_class=HTMLResponse)
def book_form():
    return """<!DOCTYPE html><html><head><title>Book Your Trip</title></head>
    <body style="max-width:500px;margin:50px auto;font-family:sans-serif">
      <h2>Book Your Trip</h2>
      <form method="post" action="/book">
        <label>Name:</label><br><input name="name" required style="width:100%;padding:8px;margin:8px 0;"><br>
        <label>Email:</label><br><input type="email" name="email" required style="width:100%;padding:8px;margin:8px 0;"><br>
        <label>Date:</label><br><input type="date" name="date" required style="width:100%;padding:8px;margin:8px 0;"><br>
        <button type="submit" style="padding:12px 20px;background:#16a34a;color:white;border:0;border-radius:8px;cursor:pointer">Confirm Booking</button>
      </form></body></html>"""

@app.post("/book")
def submit_booking(name: str = Form(...), email: str = Form(...), date: str = Form(...), db: Session = Depends(get_db)):
    notes = "Client requested customized 4x4 cruiser vehicle availability check. Lead transmitted successfully."
    booking = Booking(name=name, email=email, date=date, notes=notes)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    print(f"New Booking Saved: {booking.token}")
    # TODO: Phase 2 = WhatsApp API call here with booking.token
    return RedirectResponse(url=f"/thank-you?token={booking.token}", status_code=303)

@app.get("/thank-you", response_class=HTMLResponse)
def thank_you(token: str):
    return f"""<!DOCTYPE html><html><head><title>Booked</title></head>
    <body style="text-align:center;padding:50px;font-family:sans-serif">
      <h1>Booking Received ✅</h1>
      <p>Your Tracking Token: <b>{token}</b></p>
      <a href="/">← Back Home</a>
    </body></html>"""

@app.get("/leads", response_class=HTMLResponse) # Phase 3 = Admin page
def view_leads(db: Session = Depends(get_db)):
    bookings = db.query(Booking).order_by(Booking.id.desc()).all()
    rows = "".join([f"<tr><td>{b.token}</td><td>{b.name}</td><td>{b.email}</td><td>{b.date}</td><td>${b.value_usd}</td></tr>" for b in bookings])
    return f"""<!DOCTYPE html><html><head><title>Leads</title></head>
    <body style="padding:20px;font-family:sans-serif">
      <h2>🔒 Secure Record Details</h2>
      <table border="1" cellpadding="8" style="border-collapse:collapse;width:100%">
        <tr><th>Token</th><th>Name</th><th>Email</th><th>Date</th><th>Value</th></tr>
        {rows if rows else '<tr><td colspan=5>No leads yet</td></tr>'}
      </table>
      <br><a href="/">← Back Home</a>
    </body></html>"""
