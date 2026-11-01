"""
TerraFlow BioAI - Dataset Preparation
Downloads / generates all 4 datasets aligned with TerraFlow sensor configuration.

Datasets:
  1. Crop Recommendation    - from Kaggle (atharvaingle/crop-recommendation-dataset)
  2. Fertilizer Recommendation - from Kaggle (gdabhishek/fertilizer-prediction), augmented
  3. Soil Type Classification   - GENERATED from agronomic references (FAO, ICAR)
  4. Irrigation Prediction      - GENERATED from FAO-56 crop water requirement logic
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent / "datasets"
np.random.seed(42)


def prepare_crop_recommendation():
    """
    Load and clean the Kaggle Crop Recommendation dataset.
    Features: N, P, K, temperature, humidity, ph, rainfall → crop label

    Sensor alignment:
      - temperature, humidity → BME280
      - N, P, K, pH → soil test input
      - rainfall → weather API
    """
    path = DATASET_DIR / "Crop_recommendation.csv"
    df = pd.read_csv(path)

    # Drop unnamed/empty columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Standardize column names
    df.columns = ['nitrogen', 'phosphorus', 'potassium',
                  'temperature', 'humidity', 'ph', 'rainfall', 'label']

    # Validate ranges
    assert df['temperature'].between(-10, 60).all(), "Temperature out of BME280 range"
    assert df['humidity'].between(0, 100).all(), "Humidity out of BME280 range"

    print(f"[Crop Recommendation] Shape: {df.shape}")
    print(f"  Crops: {df['label'].nunique()} unique → {sorted(df['label'].unique())}")
    print(f"  Temperature range: {df['temperature'].min():.1f} - {df['temperature'].max():.1f} °C")
    print(f"  Humidity range: {df['humidity'].min():.1f} - {df['humidity'].max():.1f} %")

    out_path = DATASET_DIR / "crop_recommendation_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"  Saved to: {out_path}")
    return df


def prepare_fertilizer_recommendation():
    """
    Load, clean, and augment the Kaggle Fertilizer Prediction dataset.
    Only 99 rows originally → augment to ~2000 with realistic noise.

    Features: Temperature, Humidity, Moisture, Soil_Type, Crop_Type, N, P, K → Fertilizer

    Sensor alignment:
      - Temperature, Humidity → BME280
      - Moisture → soil moisture sensor (FC-28/YL-69)
      - Soil_Type → user config
      - Crop_Type → user selection
      - N, P, K → soil test input
    """
    path = DATASET_DIR / "Fertilizer Prediction.csv"
    df = pd.read_csv(path)

    # Standardize column names (original has typos and trailing spaces)
    df.columns = ['temperature', 'humidity', 'soil_moisture',
                  'soil_type', 'crop_type', 'nitrogen',
                  'potassium', 'phosphorus', 'fertilizer_name']

    # Standardize crop names to match TerraFlow standards
    crop_mapping = {
        'Paddy': 'Rice',
        'Ground Nuts': 'Groundnut',
        'Oil seeds': 'Oilseeds',
    }
    df['crop_type'] = df['crop_type'].replace(crop_mapping)

    # Augment by adding Gaussian noise to numeric columns
    augmented_dfs = [df.copy()]
    for i in range(19):  # 19 more copies = ~2000 total
        noisy = df.copy()
        for col in ['temperature', 'humidity', 'soil_moisture', 'nitrogen', 'potassium', 'phosphorus']:
            noise = np.random.normal(0, df[col].std() * 0.15, len(df))
            noisy[col] = np.clip(noisy[col] + noise, 0, None)
        # Round to realistic precision
        noisy['temperature'] = noisy['temperature'].round(1)
        noisy['humidity'] = np.clip(noisy['humidity'].round(1), 0, 100)
        noisy['soil_moisture'] = np.clip(noisy['soil_moisture'].round(1), 0, 100)
        noisy['nitrogen'] = noisy['nitrogen'].round(0).astype(int)
        noisy['potassium'] = noisy['potassium'].round(0).astype(int)
        noisy['phosphorus'] = noisy['phosphorus'].round(0).astype(int)
        augmented_dfs.append(noisy)

    df_aug = pd.concat(augmented_dfs, ignore_index=True)

    # Shuffle
    df_aug = df_aug.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"[Fertilizer Recommendation] Shape: {df_aug.shape} (augmented from {len(df)})")
    print(f"  Soil types: {sorted(df_aug['soil_type'].unique())}")
    print(f"  Crops: {sorted(df_aug['crop_type'].unique())}")
    print(f"  Fertilizers: {sorted(df_aug['fertilizer_name'].unique())}")
    print(f"  Temperature range: {df_aug['temperature'].min():.1f} - {df_aug['temperature'].max():.1f} °C")
    print(f"  Moisture range: {df_aug['soil_moisture'].min():.1f} - {df_aug['soil_moisture'].max():.1f} %")

    out_path = DATASET_DIR / "fertilizer_recommendation_clean.csv"
    df_aug.to_csv(out_path, index=False)
    print(f"  Saved to: {out_path}")
    return df_aug


def generate_soil_type_dataset(n_samples=3000):
    """
    Generate a synthetic soil type classification dataset using agronomic references.

    Each soil type has characteristic ranges for nutrients, pH, moisture retention,
    and typical environmental conditions where they are found (based on Indian agro-
    climatic zones, ICAR references, and FAO soil classification).

    Sensor alignment:
      - temperature, humidity → BME280
      - soil_moisture → FC-28/YL-69 sensor
      - N, P, K, pH → soil test input
    """
    # Soil characteristics from ICAR / FAO references for Indian soils
    soil_profiles = {
        "Black": {
            # Vertisols - high clay, high moisture retention, neutral to alkaline
            "nitrogen":     (40, 90),    # Low to medium N
            "phosphorus":   (15, 50),    # Variable P
            "potassium":    (150, 280),  # High K (rich in potassium)
            "ph":           (7.0, 8.5),  # Alkaline
            "soil_moisture":(45, 85),    # High moisture retention
            "temperature":  (25, 42),    # Deccan Plateau / Central India
            "humidity":     (40, 80),    # Moderate to high
        },
        "Red": {
            # Alfisols - low fertility, acidic, well-drained
            "nitrogen":     (20, 60),    # Low N
            "phosphorus":   (5, 30),     # Low P
            "potassium":    (50, 150),   # Low to medium K
            "ph":           (5.0, 6.8),  # Acidic to slightly acidic
            "soil_moisture":(20, 50),    # Low moisture retention
            "temperature":  (22, 38),    # Southern / Eastern peninsular
            "humidity":     (50, 85),    # Often in humid zones
        },
        "Alluvial": {
            # Entisols/Inceptisols - fertile, river deposits, variable
            "nitrogen":     (50, 120),   # Medium to high N
            "phosphorus":   (20, 70),    # Medium to high P
            "potassium":    (80, 200),   # Medium to high K
            "ph":           (6.0, 8.0),  # Near neutral (varies old vs new alluvial)
            "soil_moisture":(35, 70),    # Moderate retention
            "temperature":  (15, 40),    # Indo-Gangetic plains, wide range
            "humidity":     (45, 90),    # Variable, river plains
        },
        "Sandy": {
            # Aridisols - low nutrients, low retention, alkaline
            "nitrogen":     (10, 40),    # Very low N
            "phosphorus":   (5, 25),     # Low P
            "potassium":    (30, 100),   # Low K
            "ph":           (7.0, 9.0),  # Alkaline (arid regions)
            "soil_moisture":(5, 30),     # Very low retention
            "temperature":  (25, 48),    # Rajasthan / arid zones, hot
            "humidity":     (15, 50),    # Low humidity (desert/arid)
        },
        "Clayey": {
            # Heavy clay soils - high retention, can be waterlogged
            "nitrogen":     (35, 80),    # Medium N
            "phosphorus":   (10, 45),    # Low to medium P
            "potassium":    (120, 260),  # Medium to high K
            "ph":           (6.5, 8.0),  # Neutral to slightly alkaline
            "soil_moisture":(50, 90),    # Very high retention
            "temperature":  (20, 38),    # Various regions
            "humidity":     (55, 90),    # Often humid
        },
        "Loamy": {
            # Ideal agricultural soil - balanced properties
            "nitrogen":     (60, 130),   # Medium to high N
            "phosphorus":   (25, 65),    # Medium to high P
            "potassium":    (100, 220),  # Medium to high K
            "ph":           (6.0, 7.5),  # Near neutral (ideal)
            "soil_moisture":(30, 65),    # Moderate retention
            "temperature":  (18, 38),    # Wide adaptability
            "humidity":     (45, 80),    # Moderate
        },
    }

    samples_per_type = n_samples // len(soil_profiles)
    records = []

    for soil_type, profile in soil_profiles.items():
        for _ in range(samples_per_type):
            record = {"soil_type": soil_type}
            for feature, (low, high) in profile.items():
                # Use truncated normal for more realistic distribution
                mean = (low + high) / 2
                std = (high - low) / 4  # ~95% within range
                value = np.random.normal(mean, std)
                value = np.clip(value, low * 0.85, high * 1.15)  # Allow slight spillover

                if feature in ['nitrogen', 'phosphorus', 'potassium']:
                    record[feature] = max(0, round(value))
                elif feature == 'ph':
                    record[feature] = round(np.clip(value, 3.5, 9.5), 1)
                elif feature == 'soil_moisture':
                    record[feature] = round(np.clip(value, 0, 100), 1)
                elif feature == 'temperature':
                    record[feature] = round(np.clip(value, -5, 55), 1)
                elif feature == 'humidity':
                    record[feature] = round(np.clip(value, 0, 100), 1)
            records.append(record)

    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"[Soil Type Classification] Shape: {df.shape}")
    print(f"  Soil types: {sorted(df['soil_type'].unique())}")
    print(f"  Samples per type: {df['soil_type'].value_counts().to_dict()}")

    out_path = DATASET_DIR / "soil_type_classification.csv"
    df.to_csv(out_path, index=False)
    print(f"  Saved to: {out_path}")
    return df


def generate_irrigation_dataset(n_samples=5000):
    """
    Generate a synthetic irrigation prediction dataset using FAO-56 logic.

    The irrigation decision is based on:
      - Soil moisture vs crop-specific thresholds (from FAO-56 depletion fractions)
      - Temperature and humidity (VPD proxy → evapotranspiration demand)
      - Rainfall (recent rain reduces irrigation need)
      - Growth stage affects water demand
      - Soil type affects drainage and retention

    This is the CORE model for TerraFlow's irrigation control loop.

    Sensor alignment:
      - temperature, humidity → BME280
      - soil_moisture → FC-28/YL-69 sensor
      - N, P, K, pH → soil test input
      - rainfall → weather API
      - soil_type → user config
      - crop_type → user selection
    """
    # Crop water demand characteristics (simplified from FAO-56)
    crop_water_profiles = {
        "Rice":      {"moisture_threshold": 70, "kc_mid": 1.20, "water_demand": "high"},
        "Wheat":     {"moisture_threshold": 45, "kc_mid": 1.15, "water_demand": "medium"},
        "Maize":     {"moisture_threshold": 50, "kc_mid": 1.20, "water_demand": "medium-high"},
        "Cotton":    {"moisture_threshold": 55, "kc_mid": 1.15, "water_demand": "medium"},
        "Tomato":    {"moisture_threshold": 55, "kc_mid": 1.15, "water_demand": "medium-high"},
        "Potato":    {"moisture_threshold": 50, "kc_mid": 1.15, "water_demand": "medium"},
        "Onion":     {"moisture_threshold": 45, "kc_mid": 1.05, "water_demand": "medium"},
        "Chickpea":  {"moisture_threshold": 35, "kc_mid": 1.00, "water_demand": "low"},
        "Soybean":   {"moisture_threshold": 50, "kc_mid": 1.15, "water_demand": "medium"},
        "Groundnut": {"moisture_threshold": 40, "kc_mid": 1.05, "water_demand": "medium-low"},
    }

    soil_moisture_retention = {
        "Black":    {"base_moisture": 60, "drainage": "slow"},
        "Red":      {"base_moisture": 35, "drainage": "fast"},
        "Alluvial": {"base_moisture": 50, "drainage": "moderate"},
        "Sandy":    {"base_moisture": 20, "drainage": "very_fast"},
        "Clayey":   {"base_moisture": 65, "drainage": "very_slow"},
        "Loamy":    {"base_moisture": 45, "drainage": "moderate"},
    }

    records = []
    soil_types = list(soil_moisture_retention.keys())
    crops = list(crop_water_profiles.keys())

    for _ in range(n_samples):
        crop = np.random.choice(crops)
        soil = np.random.choice(soil_types)
        crop_profile = crop_water_profiles[crop]
        soil_profile = soil_moisture_retention[soil]

        # Generate environmental readings (BME280)
        temperature = round(np.random.uniform(15, 45), 1)
        humidity = round(np.random.uniform(20, 95), 1)

        # Soil moisture (FC-28/YL-69 sensor reading)
        soil_base = soil_profile["base_moisture"]
        soil_moisture = round(np.clip(
            np.random.normal(soil_base, 15), 5, 95
        ), 1)

        # Soil nutrients (from soil test)
        nitrogen = max(0, round(np.random.normal(60, 30)))
        phosphorus = max(0, round(np.random.normal(40, 20)))
        potassium = max(0, round(np.random.normal(100, 50)))
        ph = round(np.clip(np.random.normal(6.8, 0.8), 4.0, 9.0), 1)

        # Rainfall (from weather API)
        # 40% chance of no rain, otherwise 0-50mm
        if np.random.random() < 0.4:
            rainfall = 0.0
        else:
            rainfall = round(np.random.exponential(10), 1)
            rainfall = min(rainfall, 100.0)

        # ── IRRIGATION DECISION LOGIC (FAO-56 inspired) ──────────────────
        # This is the ground truth label generation based on agronomic rules

        moisture_threshold = crop_profile["moisture_threshold"]

        # Factor 1: Soil moisture depletion
        moisture_deficit = moisture_threshold - soil_moisture
        needs_water_moisture = soil_moisture < moisture_threshold

        # Factor 2: Evapotranspiration demand (VPD proxy)
        # Higher temperature + lower humidity = higher ET demand
        # Simplified VPD: es = 0.6108 * exp(17.27*T / (T+237.3))
        es = 0.6108 * np.exp(17.27 * temperature / (temperature + 237.3))
        ea = es * humidity / 100.0
        vpd = es - ea  # kPa
        high_et_demand = vpd > 1.5  # High atmospheric demand

        # Factor 3: Recent rainfall reduces need
        rain_sufficient = rainfall > 10.0  # >10mm rain is significant
        rain_moderate = rainfall > 5.0

        # Factor 4: Soil drainage factor
        drainage = soil_profile["drainage"]
        if drainage == "very_fast":
            drainage_factor = 1.3  # Sandy drains fast → needs more water
        elif drainage == "fast":
            drainage_factor = 1.15
        elif drainage == "moderate":
            drainage_factor = 1.0
        elif drainage == "slow":
            drainage_factor = 0.85
        else:  # very_slow
            drainage_factor = 0.7  # Clayey retains → needs less

        # Combined irrigation decision
        effective_moisture_need = moisture_deficit * drainage_factor

        if rain_sufficient:
            irrigation_needed = 0  # Recent rain covers the need
        elif soil_moisture < moisture_threshold * 0.6:
            irrigation_needed = 1  # Critical depletion → always irrigate
        elif needs_water_moisture and high_et_demand and not rain_moderate:
            irrigation_needed = 1  # Below threshold + high demand + no rain
        elif needs_water_moisture and effective_moisture_need > 10:
            irrigation_needed = 1  # Significant deficit considering drainage
        elif soil_moisture > moisture_threshold * 1.2:
            irrigation_needed = 0  # Well above threshold
        else:
            # Borderline cases: probabilistic based on conditions
            prob = 0.3
            if needs_water_moisture:
                prob += 0.3
            if high_et_demand:
                prob += 0.15
            if temperature > 35:
                prob += 0.1
            if rainfall > 0:
                prob -= 0.2
            irrigation_needed = 1 if np.random.random() < prob else 0

        records.append({
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture,
            "soil_type": soil,
            "crop_type": crop,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph,
            "rainfall": rainfall,
            "irrigation_needed": irrigation_needed,
        })

    df = pd.DataFrame(records)

    # Verify class balance
    balance = df['irrigation_needed'].value_counts(normalize=True)
    print(f"[Irrigation Prediction] Shape: {df.shape}")
    print(f"  Class balance: {balance.to_dict()}")
    print(f"  Crops: {sorted(df['crop_type'].unique())}")
    print(f"  Soil types: {sorted(df['soil_type'].unique())}")
    print(f"  Temperature range: {df['temperature'].min():.1f} - {df['temperature'].max():.1f} °C")
    print(f"  Moisture range: {df['soil_moisture'].min():.1f} - {df['soil_moisture'].max():.1f} %")

    out_path = DATASET_DIR / "irrigation_prediction.csv"
    df.to_csv(out_path, index=False)
    print(f"  Saved to: {out_path}")
    return df


if __name__ == "__main__":
    print("=" * 70)
    print("TerraFlow BioAI - Dataset Preparation")
    print("=" * 70)
    print()

    print("1. Preparing Crop Recommendation dataset...")
    df_crop = prepare_crop_recommendation()
    print()

    print("2. Preparing Fertilizer Recommendation dataset...")
    df_fert = prepare_fertilizer_recommendation()
    print()

    print("3. Generating Soil Type Classification dataset...")
    df_soil = generate_soil_type_dataset(n_samples=3000)
    print()

    print("4. Generating Irrigation Prediction dataset...")
    df_irr = generate_irrigation_dataset(n_samples=5000)
    print()

    print("=" * 70)
    print("All datasets ready!")
    print("=" * 70)

