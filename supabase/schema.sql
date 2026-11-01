-- ============================================================================
-- TerraFlow BioAI — Supabase Database Schema (DDL)
-- Aligned with SPIT Final Major Project Report (Chapters 6, 12, 15)
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ZONES TABLE (Management zone definition)
CREATE TABLE IF NOT EXISTS zones (
    zone_id VARCHAR(50) PRIMARY KEY,
    farm_id VARCHAR(50) NOT NULL DEFAULT 'FARM01',
    device_id VARCHAR(50) NOT NULL DEFAULT 'TF01',
    name VARCHAR(100) NOT NULL DEFAULT 'Plot Alpha',
    area_m2 NUMERIC(10, 2) NOT NULL DEFAULT 2.0,
    crop VARCHAR(50) NOT NULL DEFAULT 'Rice',
    soil_type VARCHAR(50) NOT NULL DEFAULT 'Black',
    season VARCHAR(20) NOT NULL DEFAULT 'Kharif',
    growth_stage VARCHAR(30) NOT NULL DEFAULT 'Mid-season',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. SOIL PROFILES (Agronomic reference profiles)
CREATE TABLE IF NOT EXISTS soil_profiles (
    soil_id VARCHAR(50) PRIMARY KEY,
    soil_name VARCHAR(50) NOT NULL,
    water_behavior TEXT NOT NULL,
    field_capacity_pct NUMERIC(5, 2) NOT NULL,
    wilting_point_pct NUMERIC(5, 2) NOT NULL,
    drainage_rate VARCHAR(30) NOT NULL, -- 'slow', 'moderate', 'fast', 'very_fast'
    ph_min NUMERIC(3, 1) NOT NULL,
    ph_max NUMERIC(3, 1) NOT NULL,
    default_n NUMERIC(6, 1) NOT NULL,
    default_p NUMERIC(6, 1) NOT NULL,
    default_k NUMERIC(6, 1) NOT NULL,
    source VARCHAR(100) DEFAULT 'ICAR / FAO Soil Database'
);

-- 3. CROP PROFILES (10 crops from Section 6.2)
CREATE TABLE IF NOT EXISTS crop_profiles (
    crop_id VARCHAR(50) PRIMARY KEY,
    crop_name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Cereal', 'Pulse', 'Cash Crop', 'Vegetable'
    seasons TEXT[] NOT NULL,       -- ['Kharif', 'Rabi']
    preferred_soils TEXT[] NOT NULL,
    ph_min NUMERIC(3, 1) NOT NULL,
    ph_max NUMERIC(3, 1) NOT NULL,
    temp_min_c NUMERIC(4, 1) NOT NULL,
    temp_max_c NUMERIC(4, 1) NOT NULL,
    water_requirement_mm NUMERIC(6, 1) NOT NULL,
    stress_sensitivity VARCHAR(30) NOT NULL, -- 'High', 'Medium', 'Low'
    source VARCHAR(100) DEFAULT 'FAO-56 Table 12 & ICAR Package of Practices'
);

-- 4. CROP STAGES (FAO-56 phenological stage Kc values for core crops)
CREATE TABLE IF NOT EXISTS crop_stages (
    stage_id SERIAL PRIMARY KEY,
    crop VARCHAR(50) NOT NULL,
    stage_name VARCHAR(50) NOT NULL, -- 'Initial', 'Development', 'Mid-season', 'Late-season'
    duration_days INT NOT NULL,
    kc NUMERIC(4, 2) NOT NULL,        -- FAO-56 Crop Coefficient
    water_demand VARCHAR(30) NOT NULL,
    critical_for_irrigation BOOLEAN DEFAULT FALSE,
    source VARCHAR(100) DEFAULT 'FAO-56 Irrigation and Drainage Paper No. 56'
);

-- 5. IRRIGATION RULES (Context rules with explainable reason codes)
CREATE TABLE IF NOT EXISTS irrigation_rules (
    rule_id SERIAL PRIMARY KEY,
    soil_type VARCHAR(50),
    crop VARCHAR(50),
    stage VARCHAR(50),
    moisture_threshold_pct NUMERIC(5, 2) NOT NULL,
    vpd_threshold_kpa NUMERIC(4, 2) DEFAULT 1.5,
    rain_offset_mm NUMERIC(5, 2) DEFAULT 10.0,
    action VARCHAR(20) NOT NULL,      -- 'IRRIGATE' or 'SKIP'
    reason_code VARCHAR(50) NOT NULL, -- 'RUN:MOISTURE_LOW', 'SKIP:RAIN_CONTEXT', etc.
    explanation TEXT NOT NULL,
    source VARCHAR(100) DEFAULT 'FAO-56 Depletion Fraction (p) Model'
);

-- 6. FERTILIZER RULES (Soil test reference rules from Section 9)
CREATE TABLE IF NOT EXISTS fertilizer_rules (
    rule_id SERIAL PRIMARY KEY,
    crop VARCHAR(50) NOT NULL,
    stage VARCHAR(50) NOT NULL,
    n_status VARCHAR(20) NOT NULL,    -- 'Low', 'Medium', 'High'
    p_status VARCHAR(20) NOT NULL,
    k_status VARCHAR(20) NOT NULL,
    recommended_fertilizer VARCHAR(100) NOT NULL,
    dose_kg_per_ha NUMERIC(6, 1) NOT NULL,
    method VARCHAR(100) NOT NULL,     -- 'Basal Dressing', 'Top Dressing'
    source VARCHAR(100) DEFAULT 'ICAR Soil Test Crop Response (STCR) Guidelines'
);

-- 7. SENSOR DATA (Time-series telemetry from TF01)
CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    zone_id VARCHAR(50) REFERENCES zones(zone_id),
    device_id VARCHAR(50) DEFAULT 'TF01',
    soil_moisture_raw NUMERIC(5, 2),
    soil_moisture_filtered NUMERIC(5, 2) NOT NULL, -- 1-D Kalman Filtered
    air_temp_c NUMERIC(5, 2) NOT NULL,            -- BME280
    humidity_pct NUMERIC(5, 2) NOT NULL,          -- BME280
    pressure_hpa NUMERIC(6, 2),                   -- BME280
    tds_ppm NUMERIC(6, 2),                        -- TDS Meter V1.0
    lux NUMERIC(8, 2),                            -- BH1750
    soil_temp_c NUMERIC(5, 2),                    -- DS18B20
    flow_rate_lpm NUMERIC(5, 2) DEFAULT 0.0,      -- Flow sensor
    tank_status VARCHAR(20) DEFAULT 'NORMAL'      -- Float switch: 'NORMAL' / 'LOW'
);

-- 8. SOIL TESTS (Entered / reference lab test records)
CREATE TABLE IF NOT EXISTS soil_tests (
    test_id SERIAL PRIMARY KEY,
    zone_id VARCHAR(50) REFERENCES zones(zone_id),
    test_date DATE DEFAULT CURRENT_DATE,
    nitrogen_kg_ha NUMERIC(6, 2) NOT NULL,
    phosphorus_kg_ha NUMERIC(6, 2) NOT NULL,
    potassium_kg_ha NUMERIC(6, 2) NOT NULL,
    ph NUMERIC(3, 1) NOT NULL,
    ec_dsm NUMERIC(4, 2),
    organic_carbon_pct NUMERIC(4, 2),
    is_reference_baseline BOOLEAN DEFAULT FALSE
);

-- 9. IRRIGATION EVENTS (Actuation history & closed-loop verification)
CREATE TABLE IF NOT EXISTS irrigation_events (
    event_id SERIAL PRIMARY KEY,
    zone_id VARCHAR(50) REFERENCES zones(zone_id),
    device_id VARCHAR(50) DEFAULT 'TF01',
    start_time TIMESTAMPTZ DEFAULT NOW(),
    stop_time TIMESTAMPTZ,
    runtime_seconds INT,
    target_volume_liters NUMERIC(6, 2) NOT NULL,
    delivered_volume_liters NUMERIC(6, 2) DEFAULT 0.0,
    flow_sensor_pulses INT,
    reason_code VARCHAR(50) NOT NULL,
    mode VARCHAR(20) DEFAULT 'AUTO', -- 'AUTO', 'MANUAL'
    post_moisture_rise_pct NUMERIC(5, 2), -- Closed-loop feedback validation
    fault_code VARCHAR(50)
);

-- 10. ADVISORIES (Machine learning & agronomic decision logs)
CREATE TABLE IF NOT EXISTS advisories (
    advisory_id SERIAL PRIMARY KEY,
    zone_id VARCHAR(50) REFERENCES zones(zone_id),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    irrigation_decision VARCHAR(30) NOT NULL,
    irrigation_confidence NUMERIC(5, 4),
    reason_code VARCHAR(50) NOT NULL,
    crop_recommendations JSONB,
    fertilizer_advisory JSONB,
    soil_classification JSONB,
    evidence_status VARCHAR(20) DEFAULT 'HIGH',
    model_version VARCHAR(30) DEFAULT 'v1.0-rf-xgb'
);

-- Indexes for time-series queries
CREATE INDEX IF NOT EXISTS idx_sensor_data_zone_ts ON sensor_data(zone_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_irrigation_events_zone ON irrigation_events(zone_id, start_time DESC);
CREATE INDEX IF NOT EXISTS idx_advisories_zone ON advisories(zone_id, timestamp DESC);
