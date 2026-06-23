import os
import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def log_lead(destination: str, service_type: str):
    file_path = os.path.join(BASE_DIR, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_path, "a") as f:
            f.write(f"{timestamp} | Destination: {destination} | Service: {service_type}\n")
    except Exception as e:
        print(f"WARNING: Could not write to leads.txt: {e}")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/click-lead/{destination}/{service_type}")
async def track_and_redirect(destination: str, service_type: str):
    log_lead(destination, service_type)
    partners = {
        "car_hire": "https://wa.me/2547XXXXXXXX",
        "safari": "https://wa.me/2547XXXXXXXX",
    }
    url = partners.get(service_type, "/")
    return RedirectResponse(url)


@app.get("/api/transport")
def get_transport_data():
    return [
        {"type": "bus", "price": 1200, "route": "Nairobi → Mombasa"},
        {"type": "train", "price": 1500, "route": "Nairobi → Kisumu"},
    ]


@app.get("/{path:path}")
def catch_all(path: str):
    osare = os.path.join(BASE_DIR, "osare.html")
    if os.path.exists(osare):
        return FileResponse(osare)
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
