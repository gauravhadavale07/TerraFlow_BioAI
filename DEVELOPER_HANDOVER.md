# TerraFlow BioAI — Developer Handover & API Contract

**For:** Full-Stack / Backend & Frontend Developer  
**From:** Machine Learning & Sensor Pipeline Lead  
**Project:** TerraFlow BioAI (SPIT Major Project)

---

## 1. Quick Summary

The Machine Learning pipeline for all **4 agricultural intelligence tasks** is fully built, trained, and tested:
1. **Irrigation Prediction** (Primary Model — XGBoost, 90.8% test accuracy, 92.0% 5-fold CV)
2. **Crop Recommendation** (Random Forest, 99.3% test accuracy, 99.4% 5-fold CV)
3. **Fertilizer Recommendation** (XGBoost, 100% test accuracy, 99.9% 5-fold CV)
4. **Soil Type Classification** (Random Forest, 84.5% test accuracy, 84.8% 5-fold CV)

The trained model artifacts (`model.joblib`, `scaler.joblib`, `label_encoders.joblib`, `metadata.json`) are stored in the `/models` directory.

A **Flask REST API Server** is already built and ready to run. It exposes clean JSON endpoints for your Node.js backend or React frontend.

---

## 2. How to Start the ML Server

From the root project folder:
```powershell
python -m ml_pipeline.api_server
```
The server will start listening at:  
👉 **`http://localhost:5000`** (or `http://<your-machine-ip>:5000` over local Wi-Fi).

---

## 3. The Main API Endpoint You Should Call

Instead of calling separate endpoints, you can get all predictions in **a single POST request**:

### **`POST /api/predict/full`**

#### **Request Body (JSON):**
```json
{
  "temperature": 32.5,
  "humidity": 65.0,
  "soil_moisture": 28.0,
  "soil_type": "Black",
  "crop_type": "Rice",
  "nitrogen": 80.0,
  "phosphorus": 40.0,
  "potassium": 150.0,
  "ph": 7.2,
  "rainfall": 0.0
}
```

#### **Important Rules about Fields:**
- **From Sensors (Mandatory):** `temperature` (BME280), `humidity` (BME280), `soil_moisture` (FC-28 / STM32 Kalman filter).
- **From Zone Configuration (Mandatory):** `soil_type` (`"Black"`, `"Red"`, `"Alluvial"`, `"Sandy"`, `"Clayey"`, `"Loamy"`), `crop_type` (`"Rice"`, `"Wheat"`, `"Maize"`, `"Cotton"`, `"Tomato"`, `"Potato"`, `"Onion"`, `"Chickpea"`, `"Soybean"`, `"Groundnut"`).
- **Nutrients (Optional):** `nitrogen`, `phosphorus`, `potassium`, `ph`.
  > **Note:** If the user has NOT entered soil test data, you can omit these fields or pass `null`. The API **automatically injects standard ICAR regional baseline values** for the selected `soil_type`.
- **From Weather API (Optional):** `rainfall` (in mm, defaults to `0.0` if omitted).

---

#### **Response Body (JSON):**
```json
{
  "timestamp": "2026-11-01T13:40:40.033849",
  "sensor_readings": {
    "temperature": 32.5,
    "humidity": 65.0,
    "soil_moisture": 28.0,
    "soil_type_input": "Black",
    "crop_type_input": "Rice",
    "nitrogen": 80.0,
    "phosphorus": 40.0,
    "potassium": 150.0,
    "ph": 7.2,
    "rainfall": 0.0
  },
  "irrigation": {
    "model": "irrigation_prediction",
    "prediction": "IRRIGATE",
    "confidence": 0.9998,
    "irrigate_probability": 0.9998,
    "evidence_status": "HIGH",
    "reason_code": "RUN:MOISTURE_LOW",
    "note": "ML decision support only. STM32 retains pump safety authority."
  },
  "crop_recommendation": {
    "model": "crop_recommendation",
    "prediction": "rice",
    "confidence": 0.9129,
    "top_5_recommendations": [
      { "crop": "rice", "confidence": 0.9129 },
      { "crop": "jute", "confidence": 0.0521 },
      { "crop": "maize", "confidence": 0.0150 },
      { "crop": "coffee", "confidence": 0.0100 },
      { "crop": "cotton", "confidence": 0.0050 }
    ]
  },
  "fertilizer_recommendation": {
    "model": "fertilizer_recommendation",
    "prediction": "Urea",
    "confidence": 0.9984,
    "all_recommendations": [
      { "fertilizer": "Urea", "confidence": 0.9984 },
      { "fertilizer": "DAP", "confidence": 0.0010 },
      { "fertilizer": "28-28", "confidence": 0.0004 }
    ]
  },
  "soil_classification": {
    "model": "soil_type_classification",
    "prediction": "Black",
    "confidence": 0.8845
  }
}
```

---

## 4. Other Individual Endpoints (If Needed)

If you only want one specific prediction instead of all 4:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | `GET` | Healthcheck (returns status of loaded models) |
| `/api/predict/irrigation` | `POST` | Only predicts irrigation (`IRRIGATE` / `NO_IRRIGATION` + reason code) |
| `/api/predict/crop` | `POST` | Only returns Top 5 crop recommendations |
| `/api/predict/fertilizer` | `POST` | Only returns recommended fertilizer |
| `/api/predict/soil` | `POST` | Classifies soil type from inputs |

---

## 5. What the Frontend Dashboard Needs to Display

To match our SPIT Project Report:
1. **Live Cards:** Air Temperature (°C), Humidity (%), Soil Moisture (%), Water TDS (ppm).
2. **Zone Settings Form:** Dropdowns for `Crop Type` and `Soil Type`, plus inputs for $N, P, K, \text{pH}$ with an *"Autofill ICAR Baseline"* toggle.
3. **Actuation Card:**
   - Pump status (`RUNNING` / `OFF`)
   - Target volume vs Delivered volume progress bar
   - Max runtime safety guard (auto-cutoff at 180s)
4. **Advisory Card:**
   - Display `advisory.irrigation.prediction` (`IRRIGATE` or `NO_IRRIGATION`)
   - Display `advisory.irrigation.reason_code` (e.g. `RUN:MOISTURE_LOW`, `SKIP:RAIN_CONTEXT`)
   - Display `advisory.fertilizer_recommendation.prediction` (e.g. `Urea`, `DAP`)
   - Display Top 5 crop recommendations list.
5. **Chart:** Soil moisture over time (showing the moisture rising after irrigation stops).

---

## 6. Crucial Rule for Viva / Professors

- **Do NOT claim that our hardware sensors measure N, P, or K.**
- The TDS sensor measures water quality (dissolved solids), not soil NPK.
- In TerraFlow, NPK values come from soil test health cards (or ICAR regional baseline data).
- The edge controller always retains local pump safety authority (maximum runtime cutoff, manual override); the ML model advises whether irrigation is needed.

