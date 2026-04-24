from fastapi import FastAPI

app = FastAPI()

# Database of SGR Schedules
SGR_SCHEDULE = [
    {"train": "Inter-County", "departs": "08:00 AM", "arrives": "02:00 PM", "type": "Day"},
    {"train": "Express", "departs": "03:00 PM", "arrives": "08:10 PM", "type": "Afternoon"},
    {"train": "Night Express", "departs": "10:00 PM", "arrives": "03:35 AM", "type": "Night"}
]

@app.get("/")
def read_root():
    return {"message": "EA Transport API: SGR & Bus Corridor Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# New Endpoint: Nairobi to Mombasa Corridor
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
                "details": "Buses wait at Miritini Terminus to take passengers to Mombasa CBD."
            }
        ],
        "visa_status": "Not Required (Domestic)",
        "total_estimated_time": "6 hours"
    }
