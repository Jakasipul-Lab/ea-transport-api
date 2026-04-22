from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# 1. Database Connection Logic
def get_db_connection():
    try:
        # This uses your Railway Variable
        db_url = os.environ.get("DATABASE_URL")
        return psycopg2.connect(db_url)
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# 2. THE CLEAN SLATE (Table Restructuring)
@app.on_event("startup")
def setup_db():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # This 'Drops' the old table so we can build the 5 columns fresh
            cur.execute("DROP TABLE IF EXISTS stations;")
            
            # Rebuilding with your 5 Columns
            cur.execute('''
                CREATE TABLE stations (
                    id SERIAL PRIMARY KEY,
                    station_name TEXT NOT NULL,
                    location_city TEXT,
                    terminal_capacity INTEGER,
                    is_active BOOLEAN DEFAULT TRUE
                );
            ''')
            conn.commit()
            cur.close()
            print("CLEAN SLATE: Stations table recreated with 5 columns.")
        except Exception as e:
            print(f"Error during Clean Slate: {e}")
        finally:
            conn.close()

# 3. Routes
@app.get("/")
def root():
    return {"status": "Online", "database": "Clean Slate Applied"}

# 4. The Railway Port Fix (DO NOT CHANGE)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
