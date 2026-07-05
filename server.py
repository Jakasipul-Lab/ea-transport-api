import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html><body style='font-family:Arial; background:#f9fafb; padding:20px; max-width:800px; margin:auto;'>
    <div style='background:#2563eb; color:#fff; padding:25px; border-radius:12px; text-align:center; margin-bottom:20px;'>
        <h1>OSARE</h1><p>Free Local Logistics Information</p>
    </div>
    
    <div style='border:1px solid #e5e7eb; padding:20px; margin:15px 0; border-radius:12px; background:#fff;'>
        <h3 style='color:#2563eb; margin-top:0;'>Bus and Matatu Transport</h3>
        <p>Daily routes across towns and cities. Major terminals: Nairobi, Mombasa, Kisumu, Eldoret.</p>
    </div>

    <div style='border:1px solid #e5e7eb; padding:20px; margin:15px 0; border-radius:12px; background:#fff;'>
        <h3 style='color:#2563eb; margin-top:0;'>SGR Train - 2nd Tier</h3>
        <p>Nairobi to Mombasa economy class. Departs: 8:00 AM & 3:00 PM daily from Syokimau.</p>
    </div>

    <div style='border:1px solid #e5e7eb; padding:20px; margin:15px 0; border-radius:12px; background:#fff;'>
        <h3 style='color:#2563eb; margin-top:0;'>SGR Train - 1st Tier</h3>
        <p>Nairobi to Mombasa business class. More legroom and meals included.</p>
    </div>

    <div style='border:1px solid #e5e7eb; padding:20px; margin:15px 0; border-radius:12px; background:#fff;'>
        <h3 style='color:#2563eb; margin-top:0;'>Taxi and Car Hire</h3>
        <p>Available 24/7 for airport transfers, town trips, and upcountry travel.</p>
    </div>
    
    </body></html>
    """
    return html
