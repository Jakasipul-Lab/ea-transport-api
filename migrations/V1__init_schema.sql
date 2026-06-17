-- migrations/V1__init_schema.sql
-- Updated schema to match user requirements

DROP TABLE IF EXISTS bookings CASCADE;

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50),
    passenger_name VARCHAR(100),
    price INT,
    operator VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);