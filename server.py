from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>EA Safari Routes</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:system-ui;background:#0b1220;color:#fff;display:grid;place-items:center;height:100vh;margin:0}
    .box{text-align:center;padding:32px;border:1px solid #1f2a44;border-radius:16px;background:#0f172a}
    a{display:inline-block;margin:12px;padding:14px 22px;border-radius:12px;background:#22c55e;color:#000;text-decoration:none;font-weight:700}
    a.alt{background:#38bdf8}
    </style></head>
    <body>
      <div class="box">
        <h1>EA Safari Routes ✅</h1>
        <p>Choose your tier</p>
        <a href="/local">Local Tier</a>
        <a class="alt" href="/safari">Safari Tier</a>
      </div>
    </body></html>
    """

@app.get("/local", response_class=HTMLResponse)
def local():
    return open("local.html", encoding="utf-8").read()

@app.get("/safari", response_class=HTMLResponse)
def safari():
    return open("safari.html", encoding="utf-8").read()
