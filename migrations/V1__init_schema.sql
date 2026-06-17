-- V1__init_schema.sql
-- Initial schema for EA SafariRoutes Unified Tiers

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INT PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CORE: Inter-city Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    booking_id VARCHAR(50) UNIQUE NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    route_id VARCHAR(50) NOT NULL,
    operator VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'PAID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIER 1: Freight Logistics
CREATE TABLE IF NOT EXISTS transit_freight_codes (
    consignment_id VARCHAR(50) PRIMARY KEY,
    container_bill_of_lading VARCHAR(50) UNIQUE,
    cargo_destination VARCHAR(50),
    rects_seal_number VARCHAR(50),
    current_corridor_node VARCHAR(50),
    clearance_status VARCHAR(50),
    how_to_claim_instructions TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIER 2: Aviation & Escrow Marketplace
CREATE TABLE IF NOT EXISTS customer_bookings_escrow_qr (
    booking_reference VARCHAR(50) PRIMARY KEY,
    listing_id VARCHAR(50),
    customer_identifier VARCHAR(100),
    gross_payment_usd NUMERIC(10, 2),
    commission_earned_usd NUMERIC(10, 2),
    vendor_payout_held_usd NUMERIC(10, 2),
    payment_escrow_status VARCHAR(50) DEFAULT 'HELD',
    qr_security_token VARCHAR(255) UNIQUE,
    qr_scan_status VARCHAR(50) DEFAULT 'UNSCANNED'
);