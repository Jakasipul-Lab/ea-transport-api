import os
import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

# --- Existing Tracking Logic ---
DIRECTORY = "."

def log_lead(destination, service_type):
    file_path = os.path.join(DIRECTORY, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"[{timestamp}] Destination: {destination}, Service: {service_type}\n")

@app.get("/track")
def track(destination: str, service_type: str):
    log_lead(destination, service_type)
    partners = {
        "car_hire": "https://wa.me/254758378722",
        "flight": "https://wa.me/254758378722",
        "hotel": "https://wa.me/254758378722"
    }
    return RedirectResponse(partners.get(service_type, "https://wa.me/254758378722"))

# --- New Search Logic ---
@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    results = []
    
    if "bus" in query: results.append(f"🚌 Bus services available ({now})")
    if "matatu" in query: results.append(f"🚐 Matatu routes active ({now})")
    if "sgr" in query or "train" in query: results.append(f"🚆 SGR departures today ({now})")
    if "taxi" in query or "car" in query: results.append(f"🚗 Car hire available ({now})")
    
    if not results: results.append("❌ No transport found (try: bus, matatu, sgr, taxi)")
    
    return HTMLResponse(f"<h1>Local Results for: {q}</h1><ul><li>{'</li><li>'.join(results)}</li></ul><br><a href='/'>← Back</a>")

# --- Root Homepage ---
@app.get("/")
def home():
    return HTMLResponse("<h1>SafariRoutes is Online</h1><p>Search via <a href='/search/local?q=bus'>/search/local?q=...</a></p>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
