from fastapi import FastAPI

# 1. Initialize the FastAPI app instance
# This MUST come before any of the @app.get decorators
app = FastAPI()

# 2. The Root Route
# This fixes the "404 Not Found" error you were seeing at the main URL
@app.get("/")
def read_root():
    return {"message": "EA Transport API is running"}

# 3. The Health Check Route
# This is what Railway uses to verify your app is alive
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 4. Your Other Endpoints
# You can add your transport-specific routes below this line
# Example:
# @app.get("/routes")
# def get_transport_routes():
#     return {"routes": ["Route A", "Route B"]}

# If you are running this locally for testing, 
# you can use: uvicorn Server:app --reload
