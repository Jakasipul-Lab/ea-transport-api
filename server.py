from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# THE BRIDGE: This allows your HTML file to talk to Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites to access your API
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        ]
    }
