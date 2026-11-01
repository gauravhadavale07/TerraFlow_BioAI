"""
TerraFlow BioAI - Inference Engine
This module loads trained models and makes predictions from sensor readings.

Usage at deployment time:
    from ml_pipeline.inference import TerraFlowPredictor

    predictor = TerraFlowPredictor()

    # From ESP32 sensor readings:
    result = predictor.predict_irrigation(
        temperature=32.5,       # BME280
        humidity=65.0,          # BME280
        soil_moisture=35.0,     # FC-28/YL-69
        soil_type="Black",      # user config
        crop_type="Rice",       # user selection
        nitrogen=80,            # soil test
        phosphorus=40,          # soil test
        potassium=150,          # soil test
        ph=7.2,                 # soil test / pH sensor
        rainfall=0.0            # weather API
    )
    # result = {"prediction": "IRRIGATE", "confidence": 0.87, "reason_code": "RUN:MOISTURE_LOW"}
"""

import json
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List

BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models"


class TerraFlowPredictor:
    """
    Unified prediction interface for all TerraFlow BioAI ML models.
    Loads models lazily on first prediction call.
    """

    def __init__(self, model_dir: Optional[Path] = None):
        self.model_dir = model_dir or MODEL_DIR
        self._models = {}
        self._scalers = {}
        self._encoders = {}
        self._metadata = {}

    def _load_model(self, model_name: str):
        """Load a model and its artifacts from disk."""
        if model_name in self._models:
            return

        model_path = self.model_dir / model_name
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model '{model_name}' not found at {model_path}. "
                f"Run train_models.py first."
            )

        self._models[model_name] = joblib.load(model_path / "model.joblib")

        scaler_path = model_path / "scaler.joblib"
        if scaler_path.exists():
            self._scalers[model_name] = joblib.load(scaler_path)

        encoder_path = model_path / "label_encoders.joblib"
        if encoder_path.exists():
            self._encoders[model_name] = joblib.load(encoder_path)

        with open(model_path / "metadata.json", "r") as f:
            self._metadata[model_name] = json.load(f)

    def _validate_range(self, value: float, name: str,
                         min_val: float, max_val: float) -> str:
        """Validate a sensor reading is within expected range."""
        if value < min_val or value > max_val:
            return (f"WARNING: {name}={value} outside expected range "
                    f"[{min_val}, {max_val}]")
        return ""

    def predict_crop(self, nitrogen: float, phosphorus: float,
                      potassium: float, temperature: float,
                      humidity: float, ph: float,
                      rainfall: float) -> Dict[str, Any]:
        """
        Predict the best crop to grow.

        Args:
            nitrogen:    Soil N content (kg/ha) — from soil test
            phosphorus:  Soil P content (kg/ha) — from soil test
            potassium:   Soil K content (kg/ha) — from soil test
            temperature: Ambient temp (°C) — from BME280
            humidity:    Relative humidity (%RH) — from BME280
            ph:          Soil pH — from soil test / pH sensor
            rainfall:    Rainfall (mm) — from weather API

        Returns:
            Dict with prediction, confidence, and top-5 recommendations
        """
        self._load_model("crop_recommendation")

        # Validate inputs
        warnings = []
        warnings.append(self._validate_range(temperature, "temperature", -10, 60))
        warnings.append(self._validate_range(humidity, "humidity", 0, 100))
        warnings.append(self._validate_range(ph, "ph", 3, 10))
        warnings = [w for w in warnings if w]

        # Prepare feature vector (same order as training)
        features = np.array([[nitrogen, phosphorus, potassium,
                               temperature, humidity, ph, rainfall]])

        # Scale
        features_scaled = self._scalers["crop_recommendation"].transform(features)

        # Predict with probabilities
        model = self._models["crop_recommendation"]
        pred_encoded = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]

        le = self._encoders["crop_recommendation"]["target"]
        predicted_crop = le.inverse_transform([pred_encoded])[0]

        # Top 5 recommendations
        top_indices = np.argsort(proba)[::-1][:5]
        top_5 = [
            {"crop": le.inverse_transform([idx])[0],
             "confidence": round(float(proba[idx]), 4)}
            for idx in top_indices
        ]

        return {
            "prediction": predicted_crop,
            "confidence": round(float(proba[pred_encoded]), 4),
            "top_5_recommendations": top_5,
            "warnings": warnings,
            "model": "crop_recommendation",
        }

    def predict_fertilizer(self, temperature: float, humidity: float,
                            soil_moisture: float, soil_type: str,
                            crop_type: str, nitrogen: float,
                            phosphorus: float, potassium: float) -> Dict[str, Any]:
        """
        Recommend the appropriate fertilizer.

        Args:
            temperature:  Ambient temp (°C) — from BME280
            humidity:     Relative humidity (%RH) — from BME280
            soil_moisture: Soil moisture (%) — from FC-28/YL-69 sensor
            soil_type:    Soil type — user config / soil classifier output
            crop_type:    Crop being grown — user selection
            nitrogen:     Soil N content (kg/ha) — from soil test
            phosphorus:   Soil P content (kg/ha) — from soil test
            potassium:    Soil K content (kg/ha) — from soil test

        Returns:
            Dict with recommended fertilizer and confidence
        """
        self._load_model("fertilizer_recommendation")

        encoders = self._encoders["fertilizer_recommendation"]
        le_soil = encoders["soil_type"]
        le_crop = encoders["crop_type"]
        le_target = encoders["target"]

        # Standardize and map soil type
        soil_clean = str(soil_type).strip().title()
        if soil_clean not in le_soil.classes_:
            soil_map = {"Alluvial": "Loamy", "Sand": "Sandy", "Clay": "Clayey"}
            soil_clean = soil_map.get(soil_clean, soil_clean)
            if soil_clean not in le_soil.classes_:
                return {
                    "error": f"Unknown soil_type '{soil_type}'. Valid: {list(le_soil.classes_)}",
                    "prediction": "Unknown",
                    "confidence": 0.0,
                    "all_recommendations": []
                }

        # Standardize and map crop type
        crop_clean = str(crop_type).strip().title()
        crop_aliases = {
            'Rice': 'Rice',
            'Paddy': 'Rice',
            'Wheat': 'Wheat',
            'Maize': 'Maize',
            'Corn': 'Maize',
            'Cotton': 'Cotton',
            'Groundnut': 'Groundnut',
            'Ground Nuts': 'Groundnut',
            'Chickpea': 'Pulses',
            'Pulses': 'Pulses',
            'Soybean': 'Oilseeds',
            'Oilseeds': 'Oilseeds',
            'Tomato': 'Pulses',
            'Potato': 'Wheat',
            'Onion': 'Maize'
        }
        if crop_clean not in le_crop.classes_:
            crop_clean = crop_aliases.get(crop_clean, crop_clean)
            if crop_clean not in le_crop.classes_:
                return {
                    "error": f"Unknown crop_type '{crop_type}'. Valid: {list(le_crop.classes_)}",
                    "prediction": "Unknown",
                    "confidence": 0.0,
                    "all_recommendations": []
                }

        soil_encoded = le_soil.transform([soil_clean])[0]
        crop_encoded = le_crop.transform([crop_clean])[0]

        features = np.array([[temperature, humidity, soil_moisture,
                               soil_encoded, crop_encoded,
                               nitrogen, phosphorus, potassium]])

        features_scaled = self._scalers["fertilizer_recommendation"].transform(features)

        model = self._models["fertilizer_recommendation"]
        pred_encoded = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]

        predicted_fertilizer = le_target.inverse_transform([pred_encoded])[0]

        # All recommendations sorted by confidence
        all_recs = []
        for idx in np.argsort(proba)[::-1]:
            all_recs.append({
                "fertilizer": le_target.inverse_transform([idx])[0],
                "confidence": round(float(proba[idx]), 4)
            })

        return {
            "prediction": predicted_fertilizer,
            "confidence": round(float(proba[pred_encoded]), 4),
            "all_recommendations": all_recs,
            "model": "fertilizer_recommendation",
        }

    def predict_soil_type(self, temperature: float, humidity: float,
                           soil_moisture: float, nitrogen: float,
                           phosphorus: float, potassium: float,
                           ph: float) -> Dict[str, Any]:
        """
        Classify the soil type from sensor readings and soil test.

        Args:
            temperature:  Ambient temp (°C) — from BME280
            humidity:     Relative humidity (%RH) — from BME280
            soil_moisture: Soil moisture (%) — from FC-28/YL-69 sensor
            nitrogen:     Soil N content (kg/ha) — from soil test
            phosphorus:   Soil P content (kg/ha) — from soil test
            potassium:    Soil K content (kg/ha) — from soil test
            ph:           Soil pH — from soil test / pH sensor

        Returns:
            Dict with predicted soil type and confidence
        """
        self._load_model("soil_type_classification")

        features = np.array([[temperature, humidity, soil_moisture,
                               nitrogen, phosphorus, potassium, ph]])

        features_scaled = self._scalers["soil_type_classification"].transform(features)

        model = self._models["soil_type_classification"]
        pred_encoded = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]

        le = self._encoders["soil_type_classification"]["target"]
        predicted_soil = le.inverse_transform([pred_encoded])[0]

        all_types = []
        for idx in np.argsort(proba)[::-1]:
            all_types.append({
                "soil_type": le.inverse_transform([idx])[0],
                "confidence": round(float(proba[idx]), 4)
            })

        return {
            "prediction": predicted_soil,
            "confidence": round(float(proba[pred_encoded]), 4),
            "all_soil_types": all_types,
            "model": "soil_type_classification",
        }

    def predict_irrigation(self, temperature: float, humidity: float,
                            soil_moisture: float, soil_type: str,
                            crop_type: str, nitrogen: float,
                            phosphorus: float, potassium: float,
                            ph: float, rainfall: float) -> Dict[str, Any]:
        """
        Predict whether irrigation is needed — TerraFlow's PRIMARY decision support.

        This prediction supports (but does NOT override) the STM32 safety authority.
        See TerraFlow report Section 10: "ML is a separate support layer, not the
        owner of the pump."

        Args:
            temperature:  Ambient temp (°C) — from BME280
            humidity:     Relative humidity (%RH) — from BME280
            soil_moisture: Soil moisture (%) — from FC-28/YL-69 sensor
            soil_type:    Soil type — user config / soil classifier
            crop_type:    Crop being grown — user selection
            nitrogen:     Soil N content (kg/ha) — from soil test
            phosphorus:   Soil P content (kg/ha) — from soil test
            potassium:    Soil K content (kg/ha) — from soil test
            ph:           Soil pH — from soil test / pH sensor
            rainfall:     Rainfall (mm) — from weather API

        Returns:
            Dict with IRRIGATE/NO_IRRIGATION prediction, confidence, and reason code
        """
        self._load_model("irrigation_prediction")

        encoders = self._encoders["irrigation_prediction"]
        le_soil = encoders["soil_type"]
        le_crop = encoders["crop_type"]

        # Standardize and map soil type
        soil_clean = str(soil_type).strip().title()
        if soil_clean not in le_soil.classes_:
            return {
                "error": f"Unknown soil_type '{soil_type}'. Valid: {list(le_soil.classes_)}",
                "prediction": "UNKNOWN",
                "confidence": 0.0,
                "reason_code": "FAULT:SENSOR_INVALID"
            }

        # Standardize and map crop type
        crop_clean = str(crop_type).strip().title()
        crop_aliases = {
            'Paddy': 'Rice',
            'Corn': 'Maize',
        }
        crop_clean = crop_aliases.get(crop_clean, crop_clean)
        if crop_clean not in le_crop.classes_:
            return {
                "error": f"Unknown crop_type '{crop_type}'. Valid: {list(le_crop.classes_)}",
                "prediction": "UNKNOWN",
                "confidence": 0.0,
                "reason_code": "FAULT:SENSOR_INVALID"
            }

        soil_encoded = le_soil.transform([soil_clean])[0]
        crop_encoded = le_crop.transform([crop_clean])[0]

        features = np.array([[temperature, humidity, soil_moisture,
                               soil_encoded, crop_encoded,
                               nitrogen, phosphorus, potassium,
                               ph, rainfall]])

        features_scaled = self._scalers["irrigation_prediction"].transform(features)

        model = self._models["irrigation_prediction"]
        pred = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]

        prediction_label = "IRRIGATE" if pred == 1 else "NO_IRRIGATION"
        confidence = round(float(proba[pred]), 4)

        # Generate reason code aligned with TerraFlow report Section 11.2
        if pred == 1:
            if soil_moisture < 30:
                reason_code = "RUN:MOISTURE_LOW"
            elif rainfall < 2 and humidity < 40:
                reason_code = "RUN:HIGH_ET_DEMAND"
            else:
                reason_code = "RUN:WATER_DEFICIT"
        else:
            if rainfall > 10:
                reason_code = "SKIP:RAIN_CONTEXT"
            elif soil_moisture > 60:
                reason_code = "SKIP:MOISTURE_ADEQUATE"
            else:
                reason_code = "SKIP:CONDITIONS_OK"

        # Evidence status (from TerraFlow report Section 11.3)
        if confidence > 0.85:
            evidence_status = "HIGH"
        elif confidence > 0.65:
            evidence_status = "MEDIUM"
        else:
            evidence_status = "LOW"

        return {
            "prediction": prediction_label,
            "confidence": confidence,
            "irrigate_probability": round(float(proba[1]), 4),
            "reason_code": reason_code,
            "evidence_status": evidence_status,
            "note": "ML decision support only. STM32 retains pump safety authority.",
            "model": "irrigation_prediction",
        }

    def get_full_advisory(self, temperature: float, humidity: float,
                           soil_moisture: float, soil_type: str,
                           crop_type: str, nitrogen: float,
                           phosphorus: float, potassium: float,
                           ph: float, rainfall: float) -> Dict[str, Any]:
        """
        Get a complete TerraFlow advisory using all 4 models.

        Returns predictions for irrigation, crop recommendation,
        soil classification, and fertilizer recommendation.
        """
        advisory = {
            "timestamp": None,  # To be set by caller
            "sensor_readings": {
                "temperature": temperature,
                "humidity": humidity,
                "soil_moisture": soil_moisture,
                "soil_type_input": soil_type,
                "crop_type_input": crop_type,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "ph": ph,
                "rainfall": rainfall,
            },
        }

        # 1. Irrigation (primary)
        advisory["irrigation"] = self.predict_irrigation(
            temperature, humidity, soil_moisture, soil_type, crop_type,
            nitrogen, phosphorus, potassium, ph, rainfall
        )

        # 2. Crop recommendation
        advisory["crop_recommendation"] = self.predict_crop(
            nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
        )

        # 3. Soil type classification
        advisory["soil_classification"] = self.predict_soil_type(
            temperature, humidity, soil_moisture, nitrogen, phosphorus,
            potassium, ph
        )

        # 4. Fertilizer recommendation
        advisory["fertilizer_recommendation"] = self.predict_fertilizer(
            temperature, humidity, soil_moisture, soil_type, crop_type,
            nitrogen, phosphorus, potassium
        )

        return advisory


# ═══════════════════════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║   TerraFlow BioAI — Inference Demo                        ║")
    print("║   Simulating sensor readings from ESP32 node TF01         ║")
    print("╚" + "═" * 58 + "╝")
    print()

    predictor = TerraFlowPredictor()

    # Simulate a real sensor reading scenario:
    # Hot afternoon, low soil moisture, rice field in black soil, no rain
    print("Scenario: Hot afternoon, dry rice field, no rain")
    print("-" * 50)

    result = predictor.get_full_advisory(
        temperature=35.5,       # BME280: hot
        humidity=45.0,          # BME280: relatively dry air
        soil_moisture=28.0,     # FC-28: soil is dry
        soil_type="Black",      # Configured as black soil
        crop_type="Rice",       # Growing rice
        nitrogen=75,            # From soil test
        phosphorus=35,          # From soil test
        potassium=180,          # From soil test
        ph=7.5,                 # From soil test / pH sensor
        rainfall=0.0            # Weather API: no rain
    )

    print(f"\n🌾 IRRIGATION: {result['irrigation']['prediction']}")
    print(f"   Confidence: {result['irrigation']['confidence']}")
    print(f"   Reason: {result['irrigation']['reason_code']}")
    print(f"   Evidence: {result['irrigation']['evidence_status']}")

    print(f"\n🌱 CROP RECOMMENDATION: {result['crop_recommendation']['prediction']}")
    print(f"   Top 5:")
    for rec in result['crop_recommendation']['top_5_recommendations']:
        print(f"     - {rec['crop']:15s} ({rec['confidence']:.2%})")

    print(f"\n🪨 SOIL TYPE: {result['soil_classification']['prediction']}")
    print(f"   Confidence: {result['soil_classification']['confidence']}")

    print(f"\n🧪 FERTILIZER: {result['fertilizer_recommendation']['prediction']}")
    print(f"   Confidence: {result['fertilizer_recommendation']['confidence']}")

    # Scenario 2: After rain
    print("\n" + "=" * 50)
    print("Scenario: After heavy rain, wheat field, cool morning")
    print("-" * 50)

    result2 = predictor.get_full_advisory(
        temperature=22.0,       # BME280: cool
        humidity=85.0,          # BME280: humid (after rain)
        soil_moisture=72.0,     # FC-28: soil is wet
        soil_type="Alluvial",   # Alluvial soil
        crop_type="Wheat",      # Growing wheat
        nitrogen=90,            # From soil test
        phosphorus=50,          # From soil test
        potassium=120,          # From soil test
        ph=6.8,                 # From soil test
        rainfall=25.0           # Weather API: heavy rain
    )

    print(f"\n🌾 IRRIGATION: {result2['irrigation']['prediction']}")
    print(f"   Confidence: {result2['irrigation']['confidence']}")
    print(f"   Reason: {result2['irrigation']['reason_code']}")
    print()

