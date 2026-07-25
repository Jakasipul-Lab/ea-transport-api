from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Home Page - Server works"}

@app.get("/advertisement")
def advertisement():
    return {"message": "Advertisement Page - Server works"}

@app.get("/about")
def about():
    return {"message": "About Page - Server works"}
