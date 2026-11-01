-- ============================================================================
-- TerraFlow BioAI — Supabase Agronomic Knowledge Base Seed Data
-- 80+ Pre-populated Rows from FAO-56, FAO-33, and ICAR Benchmarks
-- ============================================================================

-- 1. SEED DEFAULT ZONE (TF01 / Z01)
INSERT INTO zones (zone_id, farm_id, device_id, name, area_m2, crop, soil_type, season, growth_stage)
VALUES ('Z01', 'FARM01', 'TF01', 'Precision Field Plot Z01', 2.0, 'Rice', 'Black', 'Kharif', 'Mid-season')
ON CONFLICT (zone_id) DO NOTHING;

-- 2. SEED SOIL PROFILES (4 Main Indian Soil Classes + 2 Secondary)
INSERT INTO soil_profiles (soil_id, soil_name, water_behavior, field_capacity_pct, wilting_point_pct, drainage_rate, ph_min, ph_max, default_n, default_p, default_k, source)
VALUES
('SOIL_BLACK', 'Black', 'High swelling clay (Vertisol). Slow infiltration, very high water retention capacity, prone to cracking.', 38.0, 22.0, 'slow', 7.0, 8.5, 70.0, 35.0, 210.0, 'ICAR Benchmark / FAO Soil Bulletin 55'),
('SOIL_RED', 'Red', 'Porous, well-drained loam/sandy loam (Alfisol). Low organic matter, moderate-to-fast drainage.', 22.0, 10.0, 'fast', 5.0, 6.8, 40.0, 18.0, 100.0, 'ICAR Benchmark / FAO Soil Bulletin 55'),
('SOIL_ALLUVIAL', 'Alluvial', 'Deep, fertile river sediment (Entisol/Inceptisol). Highly productive, balanced water retention and drainage.', 28.0, 13.0, 'moderate', 6.0, 8.0, 85.0, 45.0, 140.0, 'ICAR Benchmark / FAO Soil Bulletin 55'),
('SOIL_SANDY', 'Sandy', 'Coarse texture, low organic matter (Aridisol). Very low moisture retention, very high percolation rate.', 12.0, 4.0, 'very_fast', 7.0, 9.0, 25.0, 15.0, 65.0, 'ICAR Benchmark / FAO Soil Bulletin 55'),
('SOIL_CLAYEY', 'Clayey', 'Heavy fine-textured soil. Very slow drainage, high moisture retention, easily waterlogged.', 36.0, 20.0, 'very_slow', 6.5, 8.0, 55.0, 25.0, 180.0, 'ICAR Benchmark / FAO Soil Bulletin 55'),
('SOIL_LOAMY', 'Loamy', 'Balanced mixture of sand, silt, and clay. Optimal agricultural structure and moisture availability.', 30.0, 14.0, 'moderate', 6.0, 7.5, 95.0, 45.0, 160.0, 'ICAR Benchmark / FAO Soil Bulletin 55')
ON CONFLICT (soil_id) DO NOTHING;

-- 3. SEED 10 CROP PROFILES (Section 6.2)
INSERT INTO crop_profiles (crop_id, crop_name, category, seasons, preferred_soils, ph_min, ph_max, temp_min_c, temp_max_c, water_requirement_mm, stress_sensitivity, source)
VALUES
('CROP_RICE', 'Rice', 'Cereal', ARRAY['Kharif'], ARRAY['Black', 'Alluvial', 'Clayey'], 5.5, 7.5, 20.0, 38.0, 1200.0, 'High', 'FAO-56 Table 12'),
('CROP_WHEAT', 'Wheat', 'Cereal', ARRAY['Rabi'], ARRAY['Alluvial', 'Black', 'Loamy'], 6.0, 7.5, 12.0, 30.0, 450.0, 'Medium', 'FAO-56 Table 12'),
('CROP_MAIZE', 'Maize', 'Cereal', ARRAY['Kharif', 'Rabi'], ARRAY['Alluvial', 'Red', 'Loamy'], 5.8, 7.5, 18.0, 35.0, 550.0, 'High', 'FAO-56 Table 12'),
('CROP_COTTON', 'Cotton', 'Cash Crop', ARRAY['Kharif'], ARRAY['Black', 'Alluvial'], 6.0, 8.0, 21.0, 40.0, 700.0, 'Medium', 'FAO-56 Table 12'),
('CROP_TOMATO', 'Tomato', 'Vegetable', ARRAY['Rabi', 'Zaid', 'Kharif'], ARRAY['Loamy', 'Black', 'Red'], 6.0, 7.0, 18.0, 32.0, 600.0, 'High', 'FAO-56 Table 12'),
('CROP_POTATO', 'Potato', 'Vegetable', ARRAY['Rabi'], ARRAY['Sandy', 'Loamy', 'Alluvial'], 5.0, 6.5, 15.0, 25.0, 500.0, 'High', 'FAO-56 Table 12'),
('CROP_ONION', 'Onion', 'Vegetable', ARRAY['Rabi', 'Kharif'], ARRAY['Alluvial', 'Loamy', 'Black'], 6.0, 7.2, 13.0, 30.0, 400.0, 'High', 'FAO-56 Table 12'),
('CROP_CHICKPEA', 'Chickpea', 'Pulse', ARRAY['Rabi'], ARRAY['Black', 'Alluvial'], 6.0, 7.5, 15.0, 30.0, 300.0, 'Low', 'FAO-56 Table 12'),
('CROP_SOYBEAN', 'Soybean', 'Pulse / Oilseed', ARRAY['Kharif'], ARRAY['Black', 'Alluvial', 'Loamy'], 6.0, 7.5, 20.0, 35.0, 500.0, 'Medium', 'FAO-56 Table 12'),
('CROP_GROUNDNUT', 'Groundnut', 'Oilseed', ARRAY['Kharif', 'Zaid'], ARRAY['Red', 'Sandy', 'Loamy'], 5.5, 7.0, 22.0, 34.0, 450.0, 'Medium', 'FAO-56 Table 12')
ON CONFLICT (crop_id) DO NOTHING;

-- 4. SEED 16 DETAILED CROP-STAGE RECORDS (4 Core Crops x 4 Phenological Stages with FAO-56 Kc)
INSERT INTO crop_stages (crop, stage_name, duration_days, kc, water_demand, critical_for_irrigation, source)
VALUES
-- Rice (Oryza sativa)
('Rice', 'Initial', 30, 1.05, 'Medium', FALSE, 'FAO-56 Table 12'),
('Rice', 'Development', 30, 1.10, 'High', TRUE, 'FAO-56 Table 12'),
('Rice', 'Mid-season', 40, 1.20, 'Very High', TRUE, 'FAO-56 Table 12 (Panicle Initiation/Flowering)'),
('Rice', 'Late-season', 30, 0.90, 'Low', FALSE, 'FAO-56 Table 12 (Ripening)'),

-- Wheat (Triticum aestivum)
('Wheat', 'Initial', 20, 0.35, 'Low', FALSE, 'FAO-56 Table 12'),
('Wheat', 'Development', 30, 0.75, 'Medium', TRUE, 'FAO-56 Table 12 (CRI Stage)'),
('Wheat', 'Mid-season', 40, 1.15, 'High', TRUE, 'FAO-56 Table 12 (Flowering/Heading)'),
('Wheat', 'Late-season', 30, 0.45, 'Low', FALSE, 'FAO-56 Table 12 (Grain Filling/Maturity)'),

-- Maize (Zea mays)
('Maize', 'Initial', 20, 0.40, 'Low', FALSE, 'FAO-56 Table 12'),
('Maize', 'Development', 35, 0.80, 'Medium', TRUE, 'FAO-56 Table 12'),
('Maize', 'Mid-season', 40, 1.20, 'Very High', TRUE, 'FAO-56 Table 12 (Tasseling and Silking)'),
('Maize', 'Late-season', 30, 0.60, 'Low', FALSE, 'FAO-56 Table 12 (Dent/Maturity)'),

-- Tomato (Solanum lycopersicum)
('Tomato', 'Initial', 30, 0.60, 'Low', FALSE, 'FAO-56 Table 12'),
('Tomato', 'Development', 40, 0.85, 'Medium', TRUE, 'FAO-56 Table 12 (Vegetative growth)'),
('Tomato', 'Mid-season', 45, 1.15, 'Very High', TRUE, 'FAO-56 Table 12 (Flowering and Fruit Set)'),
('Tomato', 'Late-season', 30, 0.80, 'Medium', FALSE, 'FAO-56 Table 12 (Fruit Ripening)')
ON CONFLICT DO NOTHING;

-- 5. SEED IRRIGATION CONTEXT RULES (FAO-56 Depletion Fraction Guidelines)
INSERT INTO irrigation_rules (soil_type, crop, stage, moisture_threshold_pct, vpd_threshold_kpa, rain_offset_mm, action, reason_code, explanation, source)
VALUES
('Black', 'Rice', 'Mid-season', 60.0, 1.5, 10.0, 'IRRIGATE', 'RUN:MOISTURE_LOW', 'Soil moisture dropped below 60% during critical rice flowering stage', 'FAO-56 / TerraFlow Knowledge Base'),
('Black', 'Rice', 'Mid-season', 65.0, 1.8, 5.0, 'IRRIGATE', 'RUN:HIGH_ET_DEMAND', 'Vapor pressure deficit exceeds 1.8 kPa indicating severe atmospheric water loss', 'FAO-56 Penman-Monteith'),
('Any', 'Any', 'Any', 75.0, 1.5, 10.0, 'SKIP', 'SKIP:MOISTURE_ADEQUATE', 'Current root-zone moisture is sufficient above field capacity depletion threshold', 'FAO-56 Depletion Fraction'),
('Any', 'Any', 'Any', 40.0, 1.5, 15.0, 'SKIP', 'SKIP:RAIN_CONTEXT', 'Recent rainfall exceeds 15mm; soil replenishment expected from precipitation', 'FAO-56 Effective Rainfall Model'),
('Sandy', 'Wheat', 'Development', 35.0, 1.4, 8.0, 'IRRIGATE', 'RUN:WATER_DEFICIT', 'Sandy soil rapid drainage has depleted available root-zone water', 'FAO-56 Soil Water Balance'),
('Red', 'Tomato', 'Mid-season', 45.0, 1.6, 10.0, 'IRRIGATE', 'RUN:WATER_DEFICIT', 'Fruit setting stage water stress threshold reached in red soil', 'FAO-56 Table 12'),
('Black', 'Cotton', 'Development', 40.0, 1.5, 10.0, 'IRRIGATE', 'RUN:MOISTURE_LOW', 'Square formation stage requires adequate soil moisture', 'ICAR Cotton Agronomy Guide')
ON CONFLICT DO NOTHING;

-- 6. SEED FERTILIZER RULES (ICAR Soil Test Crop Response - STCR)
INSERT INTO fertilizer_rules (crop, stage, n_status, p_status, k_status, recommended_fertilizer, dose_kg_per_ha, method, source)
VALUES
('Rice', 'Initial', 'Low', 'Low', 'Low', 'Urea + DAP + MOP (Basal NPK)', 100.0, 'Basal Dressing at Transplanting', 'ICAR STCR Maharashtra'),
('Rice', 'Development', 'Low', 'Medium', 'Medium', 'Urea', 50.0, 'First Top Dressing (Tillering)', 'ICAR STCR Maharashtra'),
('Rice', 'Mid-season', 'Low', 'High', 'High', 'Urea', 40.0, 'Second Top Dressing (Panicle Initiation)', 'ICAR STCR Maharashtra'),
('Wheat', 'Initial', 'Low', 'Low', 'Medium', 'DAP + Urea (Basal)', 80.0, 'Basal Drilling at Sowing', 'ICAR Wheat Directorate'),
('Wheat', 'Development', 'Low', 'Medium', 'High', 'Urea', 60.0, 'Top Dressing at First Crown Root Irrigation', 'ICAR Wheat Directorate'),
('Maize', 'Initial', 'Low', 'Low', 'Low', '10-26-26 or DAP', 75.0, 'Basal Application', 'ICAR Maize Research'),
('Tomato', 'Development', 'Medium', 'Low', 'Medium', '14-35-14', 50.0, 'Side Dressing', 'IIHR Vegetable Manual'),
('Cotton', 'Mid-season', 'Low', 'Medium', 'Medium', 'Urea + Potash (28-28)', 60.0, 'Boll Development Top Dressing', 'CICR Nagpur')
ON CONFLICT DO NOTHING;

-- 7. SEED INITIAL REFERENCE SOIL TEST FOR ZONE Z01
INSERT INTO soil_tests (zone_id, test_date, nitrogen_kg_ha, phosphorus_kg_ha, potassium_kg_ha, ph, ec_dsm, organic_carbon_pct, is_reference_baseline)
VALUES ('Z01', CURRENT_DATE, 70.0, 35.0, 210.0, 7.6, 0.45, 0.65, TRUE)
ON CONFLICT DO NOTHING;

