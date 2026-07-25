from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Home</title></head>
    <body>
        <h1>Welcome</h1>
        <a href="/advertisement">Advertisement Page</a> | 
        <a href="/about">About</a>
    </body>
    </html>
    """)

@app.get("/advertisement")
def advertisement():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Advertisement</title></head>
    <body>
        <h1>Advertisement Page</h1>
        <p>This is where your ads and WhatsApp button will go</p>
        <a href="/">Back Home</a>
    </body>
    </html>
    """)

@app.get("/about")
def about():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>About</title></head>
    <body>
        <h1>About</h1>
        <p>About your project</p>
        <a href="/">Back Home</a>
    </body>
    </html>
    """)
