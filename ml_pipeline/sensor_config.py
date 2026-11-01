"""
TerraFlow BioAI - Sensor Configuration
Maps physical sensors to ML feature expectations.
This is the SINGLE SOURCE OF TRUTH for sensor-to-feature alignment.

Hardware sensors available:
  1. BME280          → temperature (°C), humidity (%RH), pressure (hPa)
  2. Soil Moisture   → soil_moisture (0-100, resistive, FC-28/YL-69 style)
  3. TDS Meter V1.0  → tds_ppm (0-1000 ppm, water dissolved solids)
  4. ESP32 ADC       → reads analog signals from moisture + TDS

Features NOT directly measured by sensors but required by models:
  - N, P, K     → from soil test / lab input (NOT from TDS sensor)
  - pH          → from separate pH sensor or soil test input
  - rainfall    → from weather API (OpenWeatherMap etc.)
  - soil_type   → user configuration / classification model output
  - crop_type   → user selection
  - growth_stage → user selection / calendar-based
"""

# ── Sensor output ranges (for input validation during inference) ────────────
SENSOR_RANGES = {
    # BME280 measured
    "temperature":   {"min": -10.0, "max": 60.0,  "unit": "°C",   "sensor": "BME280"},
    "humidity":      {"min": 0.0,   "max": 100.0, "unit": "%RH",  "sensor": "BME280"},
    "pressure":      {"min": 300.0, "max": 1100.0,"unit": "hPa",  "sensor": "BME280"},

    # Soil moisture sensor (resistive)
    "soil_moisture": {"min": 0.0,   "max": 100.0, "unit": "%",    "sensor": "FC-28/YL-69"},

    # TDS meter
    "tds_ppm":       {"min": 0.0,   "max": 1000.0,"unit": "ppm",  "sensor": "TDS V1.0"},

    # From soil test / manual input
    "nitrogen":      {"min": 0.0,   "max": 200.0, "unit": "kg/ha","sensor": "soil_test"},
    "phosphorus":    {"min": 0.0,   "max": 200.0, "unit": "kg/ha","sensor": "soil_test"},
    "potassium":     {"min": 0.0,   "max": 300.0, "unit": "kg/ha","sensor": "soil_test"},
    "ph":            {"min": 3.0,   "max": 10.0,  "unit": "",     "sensor": "soil_test/pH_sensor"},

    # From weather API
    "rainfall":      {"min": 0.0,   "max": 500.0, "unit": "mm",   "sensor": "weather_api"},
}

# ── Standard ICAR / FAO Reference Soil Nutrients (Default Fallbacks) ────────
# When a real soil health card is not available, these benchmark agronomic values
# are used automatically based on the selected soil type.
DEFAULT_SOIL_NUTRIENTS = {
    "Black":    {"nitrogen": 70.0, "phosphorus": 35.0, "potassium": 210.0, "ph": 7.6},
    "Red":      {"nitrogen": 40.0, "phosphorus": 18.0, "potassium": 100.0, "ph": 6.2},
    "Alluvial": {"nitrogen": 85.0, "phosphorus": 45.0, "potassium": 140.0, "ph": 7.0},
    "Sandy":    {"nitrogen": 25.0, "phosphorus": 15.0, "potassium": 65.0,  "ph": 8.0},
    "Clayey":   {"nitrogen": 55.0, "phosphorus": 25.0, "potassium": 180.0, "ph": 7.2},
    "Loamy":    {"nitrogen": 95.0, "phosphorus": 45.0, "potassium": 160.0, "ph": 6.8},
}

# General agricultural average fallback
DEFAULT_NUTRIENTS = {"nitrogen": 70.0, "phosphorus": 40.0, "potassium": 120.0, "ph": 7.0}

SOIL_TYPES = ["Black", "Red", "Alluvial", "Sandy", "Clayey", "Loamy"]

# ── Crops from TerraFlow report Section 6.2 ─────────────────────────────────
TERRAFLOW_CROPS = [
    "Rice", "Wheat", "Maize", "Cotton", "Soybean",
    "Groundnut", "Chickpea", "Tomato", "Onion", "Potato"
]

# ── Growth stages from TerraFlow report Section 6.3 ────────────────────────
GROWTH_STAGES = ["Initial", "Development", "Mid-season", "Late-season"]

# ── Seasons ─────────────────────────────────────────────────────────────────
SEASONS = ["Kharif", "Rabi", "Zaid"]

# ── Model feature specifications ────────────────────────────────────────────
# Each model specifies EXACTLY which features it expects at inference time.
# This ensures sensor readings map directly to training features.

MODEL_FEATURES = {
    "crop_recommendation": {
        "features": ["nitrogen", "phosphorus", "potassium",
                      "temperature", "humidity", "ph", "rainfall"],
        "target": "crop_label",
        "sensor_sources": {
            "nitrogen":    "soil_test input",
            "phosphorus":  "soil_test input",
            "potassium":   "soil_test input",
            "temperature": "BME280",
            "humidity":    "BME280",
            "ph":          "soil_test / pH sensor",
            "rainfall":    "weather API",
        },
        "description": "Predicts which crop to grow given soil nutrients + environment"
    },

    "fertilizer_recommendation": {
        "features": ["temperature", "humidity", "soil_moisture",
                      "soil_type_encoded", "crop_type_encoded",
                      "nitrogen", "phosphorus", "potassium"],
        "target": "fertilizer_name",
        "sensor_sources": {
            "temperature":   "BME280",
            "humidity":      "BME280",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor",
            "soil_type_encoded":  "user config / soil classifier output",
            "crop_type_encoded":  "user selection",
            "nitrogen":      "soil_test input",
            "phosphorus":    "soil_test input",
            "potassium":     "soil_test input",
        },
        "description": "Recommends fertilizer type based on environment + soil nutrients"
    },

    "soil_type_classification": {
        "features": ["temperature", "humidity", "soil_moisture",
                      "nitrogen", "phosphorus", "potassium", "ph"],
        "target": "soil_type",
        "sensor_sources": {
            "temperature":   "BME280",
            "humidity":      "BME280",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor",
            "nitrogen":      "soil_test input",
            "phosphorus":    "soil_test input",
            "potassium":     "soil_test input",
            "ph":            "soil_test / pH sensor",
        },
        "description": "Classifies soil type from environmental + nutrient readings"
    },

    "irrigation_prediction": {
        "features": ["temperature", "humidity", "soil_moisture",
                      "soil_type_encoded", "crop_type_encoded",
                      "nitrogen", "phosphorus", "potassium",
                      "ph", "rainfall"],
        "target": "irrigation_needed",
        "sensor_sources": {
            "temperature":   "BME280",
            "humidity":      "BME280",
            "soil_moisture": "FC-28/YL-69 soil moisture sensor",
            "soil_type_encoded":  "user config / soil classifier",
            "crop_type_encoded":  "user selection",
            "nitrogen":      "soil_test input",
            "phosphorus":    "soil_test input",
            "potassium":     "soil_test input",
            "ph":            "soil_test / pH sensor",
            "rainfall":      "weather API",
        },
        "description": "Predicts whether irrigation is needed (binary classification)"
    },
}

