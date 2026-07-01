from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Livebooking Engine</title></head>
    <body style="text-align:center;padding:50px;font-family:sans-serif">
      <h1>Livebooking Engine is Live ✅</h1>
      <p>Your booking site is up on Render</p>
      <a href="/book" style="padding:12px 20px;background:#2563eb;color:white;text-decoration:none;border-radius:8px">
        Book Now
      </a>
    </body>
    </html>
    """

@app.get("/book", response_class=HTMLResponse)
def book_form():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Book Your Trip</title></head>
    <body style="max-width:500px;margin:50px auto;font-family:sans-serif">
      <h2>Book Your Trip</h2>
      <form method="post" action="/book">
        <label>Name:</label><br>
        <input name="name" required style="width:100%;padding:8px;margin:8px 0;"><br>
        
        <label>Email:</label><br>
        <input type="email" name="email" required style="width:100%;padding:8px;margin:8px 0;"><br>
        
        <label>Date:</label><br>
        <input type="date" name="date" required style="width:100%;padding:8px;margin:8px 0;"><br>
        
        <button type="submit" style="padding:12px 20px;background:#16a34a;color:white;border:0;border-radius:8px;cursor:pointer">
          Confirm Booking
        </button>
      </form>
      <br>
      <a href="/">← Back Home</a>
    </body>
    </html>
    """

@app.post("/book")
def submit_booking(name: str = Form(...), email: str = Form(...), date: str = Form(...)):
    print(f"New Booking: {name}, {email}, {date}") # You'll see this in Render Logs
    return RedirectResponse(url="/thank-you", status_code=303)

@app.get("/thank-you", response_class=HTMLResponse)
def thank_you():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Booked</title></head>
    <body style="text-align:center;padding:50px;font-family:sans-serif">
      <h1>Booking Received ✅</h1>
      <p>We got your details. Check Render Logs to see them.</p>
      <a href="/">← Back Home</a>
    </body>
    </html>
    """
