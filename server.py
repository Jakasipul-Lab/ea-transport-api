from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="OSARE - East Africa Hub")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>OSARE - East Africa</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:system-ui;background:#0b1220;color:#fff;display:grid;place-items:center;height:100vh;margin:0}
    .box{text-align:center;padding:40px;border:1px solid #1f2a44;border-radius:16px;background:#0f172a;max-width:400px}
    a{display:inline-block;margin:12px;padding:16px 28px;border-radius:12px;background:#22c55e;color:#000;text-decoration:none;font-weight:700;font-size:1.1rem}
    a.alt{background:#38bdf8}
    </style>
    </head>
    <body>
      <div class="box">
        <h1>OSARE Hub</h1>
        <p>Choose your service tier</p>
        <a href="/local">🚆 Local Commute</a>
        <a class="alt" href="/safari">🌍 Safari Tours</a>
      </div>
    </body>
    </html>
    """

@app.get("/local", response_class=HTMLResponse)
def local():
    try:
        with open("local.html", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>local.html not found. Create it.</h1>"

@app.get("/safari", response_class=HTMLResponse)
def safari():
    try:
        with open("safari.html", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>safari.html not found. Create it.</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
