import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# This automatically finds where your server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/search")
async def handle_search(passengerName: str, origin: str, destination: str):
    # Log the search so you can see it in Render Logs
    print(f"Search received: {passengerName} from {origin} to {destination}")
    
    # After processing, send the user to the results page
    # Make sure 'results.html' exists in your root folder
    return FileResponse(os.path.join(BASE_DIR, "results.html"))

@app.get("/{path:path}")
async def serve_files(path: str = "index.html"):
    # This construction ensures we look in the right place
    file_path = os.path.join(BASE_DIR, path)
    
    # If the user goes to the root (/)
    if path == "":
        file_path = os.path.join(BASE_DIR, "index.html")

    # Serve the file if it exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Default to index.html for everything else (including search)
    return FileResponse(os.path.join(BASE_DIR, "index.html"))
