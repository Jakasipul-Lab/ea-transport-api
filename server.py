import csv
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

# THE BRIDGE: Allows your website to connect to your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE BUSINESS ASSET: TRACKING LOG ---
def record_booking(provider, route):
    # This records every referral for your weekly commission collection
    with open("weekly_reconcile.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), provider, route, "PENDING"])

# --- ROUTES ---

# SERVES YOUR WEBSITE FRONTEND
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/book/sgr/{route_id}")
def book_sgr(route_id: str):
    # 1. Log the business referral
    record_booking("SGR", route_id)
    # 2. Redirect to the official portal with your referral code
    return RedirectResponse(url=f"https://metickets.krc.co.ke?ref=safariroutes&route={route_id}")

@app.get("/book/bus/{operator}/{route_id}")
def book_bus(operator: str, route_id: str):
    # 1. Log the business referral
    record_booking(operator, route_id)
    # 2. Redirect to the partner site
    return RedirectResponse(url=f"https://official-{operator}-site.com/book?ref=safariroutes")

@app.get("/corridor/nairobi-mombasa")
def get_nairobi_mombasa():
    return {
        "route": "Nairobi to Mombasa",
        "modes": [
            {
                "mode": "SGR Train",
                "station": "Syokimau Terminus",
                "booking_link": "/book/sgr/nairobi-mombasa"
            },
            {
                "mode": "Connection Bus",
                "provider": "SGR Link Bus / Basigo Electric",
                "booking_link": "/book/bus/sako/nairobi-mombasa"
            }
        ]
    }
