from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()

@app.get("/search/local")
def search_local(q: str):
    query = q.lower()
    now = datetime.datetime.now().strftime("%H:%M")
    
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
