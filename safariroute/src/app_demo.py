import json
import os
from generator import generate_safariroute_code
from datetime import datetime
try:
    from database import save_booking, insert_route, setup_database
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

def load_routes_from_json():
    routes = []
    # In GitHub/Production, paths should be relative to repo root
    base_path = "safariroute/data/routes/"
    files = ['kenya_sgr.json', 'tanzania_sgr.json', 'east_africa_buses.json']
    for f in files:
        full_path = os.path.join(base_path, f)
        if os.path.exists(full_path):
            with open(full_path, 'r') as file:
                routes.extend(json.load(file))
    return routes

def book_route(route_id, operator, passenger_name):
    # Generate the unique commission code
    code = generate_safariroute_code(route_id)
    
    booking = {
        "booking_id": f"BK-{int(datetime.now().timestamp())}",
        "passenger_name": passenger_name,
        "route_id": route_id,
        "operator": operator,
        "safariroute_code": code,
        "timestamp": datetime.now().isoformat(),
        "status": "ISSUED"
    }
    
    if DB_AVAILABLE and os.getenv("RAILWAY_DB_URL"):
        try:
            save_booking(booking)
            print(f"Booking saved to PostgreSQL database.")
        except Exception as e:
            print(f"DB Error: {e}. Falling back to JSON.")
            save_to_json(booking)
    else:
        save_to_json(booking)
    
    return booking

def save_to_json(booking):
    os.makedirs("safariroute/data/bookings", exist_ok=True)
    filename = f"safariroute/data/bookings/{booking['booking_id']}.json"
    with open(filename, 'w') as f:
        json.dump(booking, f, indent=4)

if __name__ == "__main__":
    print("--- EA Safariroute: Available Routes ---")
    all_routes = load_routes_from_json()
    
    if DB_AVAILABLE and os.getenv("RAILWAY_DB_URL"):
        setup_database()
        for r in all_routes:
            insert_route(r)
            
    for i, r in enumerate(all_routes):
        print(f"{i+1}. [{r['type']}] {r['origin']} to {r['destination']} (via {r.get('operator', r.get('operators', ['Unknown'])[0])})")
    
    # Simulate a user booking
    print("\n--- Simulating a Booking for: John Doe ---")
    if all_routes:
        sample_route = all_routes[0] 
        res = book_route(sample_route['route_id'], "Madaraka Express", "John Doe")
        
        print(f"Booking Successful!")
        print(f"Passenger: {res['passenger_name']}")
        print(f"Route: {sample_route['origin']} -> {sample_route['destination']}")
        print(f"YOUR SAFARIROUTE CODE: {res['safariroute_code']}")
    else:
        print("No routes found.")