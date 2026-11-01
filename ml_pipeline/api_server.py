"""
TerraFlow BioAI - ESP32 Integration Layer
Provides the REST API endpoint that ESP32 calls to get ML predictions.

This runs on the backend (Node.js calls this, or directly as a Flask server).
The ESP32 → UART → backend → this module → prediction → response.

Endpoints:
  POST /api/predict/irrigation    → irrigation decision
  POST /api/predict/crop          → crop recommendation
  POST /api/predict/soil          → soil type classification
  POST /api/predict/fertilizer    → fertilizer recommendation
  POST /api/predict/full          → complete advisory (all 4 models)
"""

import json
from datetime import datetime
from pathlib import Path

# Simple HTTP server for testing (production would use Node.js/Express)
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from ml_pipeline.inference import TerraFlowPredictor
from ml_pipeline.sensor_config import DEFAULT_SOIL_NUTRIENTS, DEFAULT_NUTRIENTS


def get_nutrient_defaults(soil_type, data):
    """Retrieve nutrients from request or fallback to standard ICAR soil reference values."""
    defaults = DEFAULT_SOIL_NUTRIENTS.get(str(soil_type).strip().title(), DEFAULT_NUTRIENTS)
    n = float(data['nitrogen']) if data.get('nitrogen') is not None else defaults['nitrogen']
    p = float(data['phosphorus']) if data.get('phosphorus') is not None else defaults['phosphorus']
    k = float(data['potassium']) if data.get('potassium') is not None else defaults['potassium']
    ph = float(data['ph']) if data.get('ph') is not None else defaults['ph']
    return n, p, k, ph


def create_app():
    """Create the Flask application for ML predictions."""
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing for remote laptops & React
    predictor = TerraFlowPredictor()

    @app.route('/api/predict/irrigation', methods=['POST'])
    def predict_irrigation():
        """
        ESP32 sensor payload → irrigation prediction.
        Nutrients (N, P, K, pH) are optional: if omitted, ICAR reference benchmarks are used.
        """
        data = request.get_json() or {}
        try:
            soil_type = str(data.get('soil_type', 'Black'))
            crop_type = str(data.get('crop_type', 'Rice'))
            n, p, k, ph = get_nutrient_defaults(soil_type, data)

            result = predictor.predict_irrigation(
                temperature=float(data.get('temperature', 25.0)),
                humidity=float(data.get('humidity', 60.0)),
                soil_moisture=float(data.get('soil_moisture', 30.0)),
                soil_type=soil_type,
                crop_type=crop_type,
                nitrogen=n,
                phosphorus=p,
                potassium=k,
                ph=ph,
                rainfall=float(data.get('rainfall', 0.0))
            )
            result['timestamp'] = datetime.now().isoformat()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/predict/crop', methods=['POST'])
    def predict_crop():
        data = request.get_json()
        try:
            result = predictor.predict_crop(
                nitrogen=float(data['nitrogen']),
                phosphorus=float(data['phosphorus']),
                potassium=float(data['potassium']),
                temperature=float(data['temperature']),
                humidity=float(data['humidity']),
                ph=float(data['ph']),
                rainfall=float(data.get('rainfall', 0.0))
            )
            result['timestamp'] = datetime.now().isoformat()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/predict/soil', methods=['POST'])
    def predict_soil():
        data = request.get_json()
        try:
            result = predictor.predict_soil_type(
                temperature=float(data['temperature']),
                humidity=float(data['humidity']),
                soil_moisture=float(data['soil_moisture']),
                nitrogen=float(data['nitrogen']),
                phosphorus=float(data['phosphorus']),
                potassium=float(data['potassium']),
                ph=float(data['ph'])
            )
            result['timestamp'] = datetime.now().isoformat()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/predict/fertilizer', methods=['POST'])
    def predict_fertilizer():
        data = request.get_json() or {}
        try:
            soil_type = str(data.get('soil_type', 'Black'))
            crop_type = str(data.get('crop_type', 'Rice'))
            n, p, k, _ = get_nutrient_defaults(soil_type, data)

            result = predictor.predict_fertilizer(
                temperature=float(data.get('temperature', 25.0)),
                humidity=float(data.get('humidity', 60.0)),
                soil_moisture=float(data.get('soil_moisture', 30.0)),
                soil_type=soil_type,
                crop_type=crop_type,
                nitrogen=n,
                phosphorus=p,
                potassium=k
            )
            result['timestamp'] = datetime.now().isoformat()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/predict/full', methods=['POST'])
    def predict_full():
        """Complete TerraFlow advisory using all 4 models."""
        data = request.get_json() or {}
        try:
            soil_type = str(data.get('soil_type', 'Black'))
            crop_type = str(data.get('crop_type', 'Rice'))
            n, p, k, ph = get_nutrient_defaults(soil_type, data)

            result = predictor.get_full_advisory(
                temperature=float(data.get('temperature', 25.0)),
                humidity=float(data.get('humidity', 60.0)),
                soil_moisture=float(data.get('soil_moisture', 30.0)),
                soil_type=soil_type,
                crop_type=crop_type,
                nitrogen=n,
                phosphorus=p,
                potassium=k,
                ph=ph,
                rainfall=float(data.get('rainfall', 0.0))
            )
            result['timestamp'] = datetime.now().isoformat()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "ok",
            "service": "TerraFlow BioAI ML",
            "models": ["irrigation_prediction", "crop_recommendation",
                       "soil_type_classification", "fertilizer_recommendation"]
        })

    return app


if __name__ == '__main__':
    if not HAS_FLASK:
        print("Flask not installed. Install with: pip install flask")
        print("Running inference demo instead...")
        import ml_pipeline.inference
    else:
        app = create_app()
        print("TerraFlow BioAI ML API starting on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)

