from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
app = FastAPI()
templates = Jinja2Templates(directory="templates") # Sagt: "Schau in den Ordner templates"

conn = sqlite3.connect("bookings.db") # Erstellt Datei wenn nicht da
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, name TEXT, email TEXT, route TEXT, date TEXT)")
conn.commit()
conn.close()
@app.get("/") 
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) # Zeigt Home

@app.get("/search") 
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request}) # Zeigt Form

@app.post("/inquire")
async def inquire(name: str = Form(...), email: str = Form(...), route: str = Form(...), date: str = Form(...)):
    # Speichert was im Form steht in die DB
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, email, route, date) VALUES (?,?,?,?)", (name, email, route, date))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303) # Zurück auf Home
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)