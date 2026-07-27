import sqlite3

conn = sqlite3.connect("transport.db")
cursor = conn.cursor()

# Ensure table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator TEXT,
    origin TEXT,
    destination TEXT,
    time TEXT,
    price TEXT,
    price_kes INTEGER,
    category TEXT,
    info TEXT
)
''')

# Clear old mixed data
cursor.execute("DELETE FROM routes")

sample_routes = [
    # --- EAsafari: Lucrative Tourism & Regional Safari Routes ---
    ("Mara Land Cruiser Safaris", "Nairobi CBD / JKIA", "Masai Mara (Talek / Sekenani Gate)", "06:00 AM Daily", "KES 15,000", 15000, "safari", "4x4 Tour Van / Land Cruiser - Game Drives Included"),
    ("Amboseli Express Shuttles", "Nairobi", "Amboseli National Park (Kimana Gate)", "07:30 AM Daily", "KES 4,500", 4500, "safari", "Tourist Overland Shuttle"),
    ("Madaraka Express SGR", "Nairobi Terminus (Syokimau)", "Mombasa Terminus (Miritini)", "08:00 AM & 03:00 PM", "KES 1,500 (First Class KES 4,500)", 1500, "safari", "High-speed rail to the Coast"),
    ("Coastline Luxury Overland", "Mombasa", "Diani Beach / Ukunda", "Hourly", "KES 1,200", 1200, "safari", "Air-conditioned Tourist Transfer"),
    ("Riverside Express Coach", "Nairobi", "Kampala (Uganda)", "06:00 PM Overnight", "KES 3,800", 3800, "safari", "Cross-Border VIP Luxury Bus"),
    ("Tsavo Tourist Transfer", "Mombasa", "Tsavo East (Voi Gate)", "06:30 AM", "KES 3,500", 3500, "safari", "Safari Game Park Shuttle"),

    # --- Jakasipul: Local Commuter Routes ---
    ("Super Metro", "Nairobi CBD (Archives)", "Rongai / Kiserian", "Every 5 mins", "KES 100", 100, "local", "Express commuter via Langata Rd"),
    ("Citi Hoppa", "Nairobi CBD", "Kasarani / Mamboleo", "Every 10 mins", "KES 80", 80, "local", "City commuter route"),
    ("Likoni Shuttle", "Mombasa Island", "Likoni Mainland", "Continuous", "KES 50", 50, "local", "Ferry connection commuter"),
    ("Kondele Express", "Kisumu CBD", "Kondele / Mamboleo", "Every 5 mins", "KES 50", 50, "local", "Matatu town service")
]

cursor.executemany('''
INSERT INTO routes (operator, origin, destination, time, price, price_kes, category, info)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sample_routes)

conn.commit()
conn.close()
print("✅ Database updated! Tourism Safari and Local Commuter routes are now clearly separated.")
