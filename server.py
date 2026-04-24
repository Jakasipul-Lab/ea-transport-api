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

# KEEP THIS RUNNER (Works with Railway)
if __name__ == "__main__":
    import uvicorn
    # This part handles the Railway port error
    raw_port = os.getenv("PORT", "8000")
    if not raw_port.isdigit():
        port = 8000
    else:
        port = int(raw_port)
        
    uvicorn.run(app, host="0.0.0.0", port=port)
