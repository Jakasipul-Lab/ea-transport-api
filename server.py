import os
from fastapi import FastAPI

app = FastAPI()

def get_db_connection():
    import psycopg2 
    try:
        # This looks for the DATABASE_URL variable you set in Railway
        db_url = os.environ.get("DATABASE_URL")
        return psycopg2.connect(db_url)
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Station API", "status": "Online"}

@app.get("/health")
def health_check():
    # We removed the database connection here so the site 
    # stays "Healthy" even if the DB is sleeping.
    return {"status": "healthy"}

@app.get("/stations")
def get_stations():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    cur = conn.cursor()
    # This query matches your 'stations' table structure
    cur.execute("SELECT id, station_name, location_city, terminal_capacity, is_active FROM stations;")
    rows = cur.fetchall()
    
    stations = []
    for row in rows:
        stations.append({
            "id": row[0],
            "name": row[1],
            "city": row[2],
            "capacity": row[3],
            "active": row[4]
        })
    
    cur.close()
    conn.close()
    return stations

# --- THE STARTUP BLOCK ---
if __name__ == "__main__":
    import uvicorn
    # Change the default to 8000 to match your Railway settings
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
