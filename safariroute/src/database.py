import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("RAILWAY_DB_URL") or os.getenv("NEON_DB_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def setup_database():
    commands = (
        """CREATE TABLE IF NOT EXISTS routes (id SERIAL PRIMARY KEY, route_id VARCHAR(50) UNIQUE NOT NULL, origin VARCHAR(100) NOT NULL, destination VARCHAR(100) NOT NULL, transport_type VARCHAR(20) NOT NULL, operator VARCHAR(100) NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS bookings (id SERIAL PRIMARY KEY, booking_id VARCHAR(50) UNIQUE NOT NULL, passenger_name VARCHAR(100) NOT NULL, route_id VARCHAR(50) NOT NULL, operator VARCHAR(100) NOT NULL, safariroute_code VARCHAR(50) UNIQUE NOT NULL, status VARCHAR(20) DEFAULT 'ISSUED', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (route_id) REFERENCES routes (route_id))"""
    )
    if not DATABASE_URL: return
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        for command in commands: cur.execute(command)
        cur.close(); conn.commit()
    except Exception as e: print(e)
    finally: 
        if conn is not None: conn.close()

def save_booking(booking_data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (booking_id, passenger_name, route_id, operator, safariroute_code) VALUES (%s, %s, %s, %s, %s)", (booking_data['booking_id'], booking_data['passenger_name'], booking_data['route_id'], booking_data['operator'], booking_data['safariroute_code']))
    conn.commit(); cur.close(); conn.close()