import os
from fastapi import FastAPI

app = FastAPI()

def get_db_connection():
    # We move the import inside so the app doesn't crash on startup 
    # if the database is still waking up
    import psycopg2 
    try:
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
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "healthy", "database": "connected"}
    else:
        return {"status": "unhealthy", "database": "disconnected"}

@app.get("/stations")
def get_stations():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    cur = conn.cursor()
    # This query fetches your 5 specific columns
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
