import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OSARE Transit Super Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

# Fallback routes to ensure no 404s during transition
@app.get("/admin", response_class=HTMLResponse) def admin(): return FileResponse("index.html")
@app.get("/support", response_class=HTMLResponse) def support(): return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)