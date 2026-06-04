from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Added commission_link to your schedule for direct booking hand-offs
SGR_SCHEDULE = [
    {
        "train": "Inter-County", 
        "departs": "08:00 AM", 
        "arrives": "02:00 PM", 
        "type": "Day",
        "booking_url": "https://metickets.krc.co.ke?ref=safariroutes" 
    },
    {
        "train": "Express", 
        "departs": "03:00 PM", 
        "arrives": "08:10 PM", 
        "type": "Afternoon",
        "booking_url": "https://metickets.krc.co.ke?ref=safariroutes"
    }
]

@app.get("/")
def read_root():
    return {"message": "EA SafariRoutes: Official Travel & Logistics Concierge"}

# New Business Route: This acts as your "Agent" portal
@app.get("/book/sgr/{train_name}")
def book_sgr(train_name: str):
    # This acts as the automated hand-off to the partner
    return RedirectResponse(url=f"https://metickets.krc.co.ke?ref=safariroutes&train={train_name}")

@app.get("/corridor/nairobi-mombasa")
def get_nairobi_mombasa():
    return {
        "route": "Nairobi to Mombasa",
        "modes": [
            {
                "mode": "SGR Train",
                "options": SGR_SCHEDULE,
                "station": "Syokimau Terminus"
            },
            {
                "mode": "Connection Bus",
                "provider": "SGR Link Bus / Basigo Electric",
                "booking_url": "https://sako-bus-booking.com?ref=safariroutes" # Added tracking
            }
        ]
    }
