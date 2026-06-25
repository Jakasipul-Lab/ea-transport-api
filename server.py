from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")

import os
import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

DIRECTORY = "."

def log_lead(destination, service_type):
    file_path = os.path.join(DIRECTORY, "leads.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as f:
        f.write(f"[{timestamp}] Destination: {destination}, Service: {service_type}\n")

@app.get("/")
def home():
    return {"message": "SafariRoutes is active. Use /track to get routed."}

@app.get("/track")
def track(destination: str, service_type: str):
    log_lead(destination, service_type)

    # Real partner routing numbers
    partners = {
        "car_hire": "https://wa.me/254758378722",
        "flight": "https://wa.me/254758378722",
        "hotel": "https://wa.me/254758378722"
    }

    # Redirect to the matched number, or fallback to the main number
    return RedirectResponse(partners.get(service_type, "https://wa.me/254758378722"))

if __name__ == "__main__":
    print("Starting production tracking server on port 10000...")
    uvicorn.run(app, host="0.0.0.0", port=10000)

@app.get("/")
def read_root():
    return {"message": "Welcome to SafariRoutes! Use /track to get routed to our partners."}
    
    results = []
    if "bus" in query: results.append(f"🚌 Bus services available ({now})")
    if "matatu" in query: results.append(f"🚐 Matatu routes active ({now})")
    if "sgr" in query or "train" in query: results.append(f"🚆 SGR departures today ({now})")
    if "taxi" in query or "car" in query: results.append(f"🚗 Car hire available ({now})")
    
    if not results:
        results.append("❌ No transport found (try: bus, matatu, sgr, taxi)")
        
    # Using triple quotes for clean multiline HTML
    html_content = f"""
    <html>
        <body>
            <h1>Local Results for: {q}</h1>
            <p>{'<br>'.join(results)}</p>
            <br>
            <a href="/">← Back</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/search/local")
def test():
    return HTMLResponse("<h1>It is finally working!</h1>")

@app.get("/")
def home():
    return HTMLResponse("<h1>Welcome to SafariRoutes</h1><a href='/search/local?q=bus'>Search for Transport</a>")

@app.get("/search/local")
def search_local(q: str):
    # ... your existing code ...

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. Add this home route
@app.get("/")
def home():
    return HTMLResponse("<h1>Welcome!</h1><a href='/search/local?q=bus'>Go to Search</a>")

# 2. Keep your existing search route
@app.get("/search/local")
def search_local(q: str):
    # Your search logic here...
    return HTMLResponse(f"Searching for: {q}")
