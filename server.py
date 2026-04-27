from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This part stops the "Network Error"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/corridor/nairobi-mombasa")
def get_data():
    return {
        "route": "Nairobi - Mombasa",
        "status": "Active",
        "transport_type": "SGR & Bus"
    }
