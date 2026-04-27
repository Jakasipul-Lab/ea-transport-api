from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This part is CRITICAL: It tells the browser "It's okay to show my data"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EA Transport API: SGR & Bus Corridor Service"}

@app.get("/corridor/nairobi-mombasa")
def get_nairobi_mombasa():
    # This is the data that will turn into your Blue Bars
    return {
        "route": "Nairobi - Mombasa",
        "status": "Active",
        "transport_type": "SGR & Bus",
        "last_updated": "Just now"
    }
