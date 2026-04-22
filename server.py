from pydantic import BaseModel
from typing import List

# 1. Station/Route Models (What the agent asked for)
class Station(BaseModel):
    name: str
    location: str

class Schedule(BaseModel):
    station_name: str
    arrival_time: str
    route_id: str

# 2. Schedule Endpoints
@app.get("/schedules", response_model=List[Schedule])
async def get_all_schedules():
    schedules = await db.schedules.find().to_list(100)
    return schedules

# 3. Booking Endpoints
@app.post("/book")
async def create_booking(booking: dict):
    result = await db.bookings.insert_one(booking)
    return {"id": str(result.inserted_id), "status": "success"}
