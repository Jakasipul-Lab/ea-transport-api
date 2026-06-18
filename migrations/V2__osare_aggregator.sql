-- migrations/V2__osare_aggregator.sql
-- Schema for OSARE Transit Search & Revenue Engine

-- 1. SCRAPER CACHE: Stores real-time SGR and Bus availability
CREATE TABLE IF NOT EXISTS scraper_cache (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) NOT NULL,
    transport_type VARCHAR(20), -- 'SGR', 'BUS'
    departure_time TIMESTAMP NOT NULL,
    seats_available INT DEFAULT 0,
    base_price NUMERIC(10, 2),
    currency VARCHAR(5) DEFAULT 'KES',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_route_time ON scraper_cache(route_id, departure_time);

-- 2. REVENUE TRACKER: Logs commissions and convenience fees
CREATE TABLE IF NOT EXISTS osare_revenue (
    booking_id VARCHAR(50) PRIMARY KEY,
    passenger_name VARCHAR(100),
    base_fare NUMERIC(10, 2),
    agency_commission NUMERIC(10, 2), -- 5% cut
    convenience_fee NUMERIC(10, 2),    -- KES 30-50 fixed fee
    total_paid NUMERIC(10, 2),
    payment_status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, PAID, FAILED
    mpesa_reference VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. MY TRIPS: Encrypted QR storage for user history
CREATE TABLE IF NOT EXISTS user_trips (
    trip_id VARCHAR(50) PRIMARY KEY,
    booking_id VARCHAR(50) REFERENCES osare_revenue(booking_id),
    qr_payload TEXT, -- Secure hashed data for the station turnstile
    travel_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);