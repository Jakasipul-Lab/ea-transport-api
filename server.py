import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import databases

# ✅ DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")

# ✅ LIFESPAN (connect / disconnect DB safely)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DEBUG: DATABASE_URL =", DATABASE_URL)

    database = databases.Database(DATABASE_URL)
    await database.connect()
    app.state.database = database

    yield

    await database.disconnect()

# ✅ APP
app = FastAPI(lifespan=lifespan)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ REQUEST MODEL
class SearchRequest(BaseModel):
    destination: str
    category: str = "tourist"

# ✅ HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

# ✅ CATCH ALL (serves your pages like /admin, /verify)
@app.get("/{path:path}", response_class=HTMLResponse)
def catch_all(path: str):
    file_path = path + ".html"

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return FileResponse("index.html")
# ✅ SEARCH API
@app.post("/api/search")
async def search_transport(req: SearchRequest):
    query = """
        SELECT * FROM transport_options
        WHERE destination = :dest AND category = :cat
    """

    results = await app.state.database.fetch_all(
        query=query,
        values={
            "dest": req.destination,
            "cat": req.category
        }
    )

    return [dict(row) for row in results]


# ✅ STATS API (for admin dashboard)
@app.get("/api/stats")
async def stats():
    query = "SELECT COUNT(*) as total FROM transport_options"
    result = await app.state.database.fetch_one(query)

    return {
        "total": result["total"] if result else 0
    }
    results = await app.state.database.fetch_all(
        query=query,
        values={
            "dest": req.destination,
            "cat": req.category
        }
    )

    return [dict(row) for row in results]

# ✅ START (for local run only)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
