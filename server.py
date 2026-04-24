from fastapi import FastAPI
import os
import uvicorn
# ADD YOUR ORIGINAL IMPORTS HERE
# from your_module import your_functions

app = FastAPI()

# YOUR ORIGINAL ENDPOINTS/ROUTES GO HERE
@app.get("/")
def read_root():
    return {"message": "EA Transport API is running"}

# ADD YOUR ORIGINAL ROUTES HERE
# @app.get("/routes")
# def get_routes():
#     return {...}

# KEEP THE NEW HEALTH CHECK
@app.get("/health")
def health_check():
    return {"status": "healthy"}

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "healthy"}
