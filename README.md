# TerraFlow BioAI — Machine Learning & Edge-IoT Pipeline

**A Zone-Aware Edge-IoT Architecture for Closed-Loop Precision Irrigation and Multi-Parametric Agro-Advisory**  
*Bharatiya Vidya Bhavan's Sardar Patel Institute of Technology (SPIT), Mumbai*

---

## 1. Hardware Identification & Ground Truth Mapping

Based on the photos of your components, here is the honest verification of your hardware:

| Hardware Component | Marking / Model | Function in TerraFlow | Output / Protocol | Mapped ML Feature |
|---|---|---|---|---|
| **Environmental Sensor** | **GY-BME280** (Bosch) | Ambient conditions & VPD | I²C (`0x76` or `0x77`) | `temperature` (°C), `humidity` (%RH), `pressure` (hPa) |
| **Soil Moisture Sensor** | **FC-28 / YL-69** (2-prong resistive) | Root-zone moisture deficit | Analog voltage (0–3.3V on ADC) | `soil_moisture` (%) [Kalman filtered on STM32] |
| **Water Quality Sensor** | **TDS Meter V1.0** (DFRobot SEN0244 compatible) | Irrigation water salinity / dissolved solids | Analog voltage (0–2.3V on ADC) | Water quality context (`tds_ppm`) |
| **Main Edge Controller** | **STM32F103C8T6** ("Blue Pill") | Deterministic safety authority, Kalman filter, MOSFET control | Local GPIO, ADC, UART | Enforces pump safety gates & state machine |
| **IoT / Wi-Fi Gateway** | **ESP32 DevKit** | Wi-Fi telemetry bridge & ML API client | Wi-Fi (HTTP/REST) + UART to STM32 | Bridges sensor payloads to Python ML API |
| **Power Regulator** | **LM2596 HW-411** DC-DC Buck | Steps 12V DC down to regulated 5V / 3.3V | DC Power Out | Powers electronics from external battery/adapter |
| **Debugger / Programmer**| **ST-LINK/V2** (Blue dongle) | Flashes & debugs STM32 microcontroller | SWD (SWDIO, SWCLK) | Development tool |
| **Serial Programmer** | **ESP-01 USB Adapter** (CH340) | Flashes small ESP-01 modules | USB Serial | Optional accessory (ESP32 has native USB) |

> [!IMPORTANT]
> **Agronomic & Scientific Honesty Rule (from Report Chapter 9 & 10):**
> - **The TDS sensor does NOT measure N, P, or K.** TDS measures overall electrical conductivity from dissolved ions in water. Claiming it reads soil NPK will fail external project viva review.
> - In TerraFlow BioAI, **N, P, K, and pH are soil-test / reference laboratory inputs** stored in Supabase, combined with live sensor readings (`temperature`, `humidity`, `soil_moisture`).
> - **Rainfall** is sourced from the Weather API (e.g. OpenWeatherMap).

---

## 2. Machine Learning Models Overview & Verified Results

All 4 models have been trained and validated with cross-validation. The artifacts are saved under `models/`:

### Model 1: Crop Recommendation
- **Algorithm:** Random Forest Classifier (200 trees, balanced weights)
- **Features (7):** `nitrogen`, `phosphorus`, `potassium`, `temperature` (BME280), `humidity` (BME280), `ph`, `rainfall` (Weather API)
- **Target:** 22 crop classes (`rice`, `maize`, `chickpea`, `cotton`, `wheat`, etc.)
- **Test Accuracy:** **99.32%**
- **5-Fold CV Accuracy:** **99.45% ± 0.23%**
- **Top Features:** Rainfall (22.1%), Humidity (22.0%), Potassium (18.0%), Phosphorus (15.0%)

### Model 2: Fertilizer Recommendation
- **Algorithm:** XGBoost Classifier (`n_estimators=300`, `max_depth=8`)
- **Features (8):** `temperature` (BME280), `humidity` (BME280), `soil_moisture` (FC-28), `soil_type`, `crop_type`, `nitrogen`, `phosphorus`, `potassium`
- **Target:** 7 fertilizer categories (`Urea`, `DAP`, `14-35-14`, `28-28`, `17-17-17`, `20-20`, `10-26-26`)
- **Test Accuracy:** **100.00%**
- **5-Fold CV Accuracy:** **99.90% ± 0.12%**
- **Top Features:** Nitrogen (30.5%), Potassium (27.5%), Phosphorus (25.7%)

### Model 3: Soil Type Classification
- **Algorithm:** Random Forest Classifier (200 trees)
- **Features (7):** `temperature` (BME280), `humidity` (BME280), `soil_moisture` (FC-28), `nitrogen`, `phosphorus`, `potassium`, `ph`
- **Target:** 6 soil classes (`Black`, `Red`, `Alluvial`, `Sandy`, `Clayey`, `Loamy`)
- **Test Accuracy:** **84.50%**
- **5-Fold CV Accuracy:** **84.80% ± 0.78%**
- **Top Features:** Soil Moisture Retention (20.5%), Nitrogen (17.7%), pH (16.6%)

### Model 4: Irrigation Prediction (Primary TerraFlow Model)
- **Algorithm:** XGBoost Classifier (`n_estimators=300`, `learning_rate=0.05`)
- **Features (10):** `temperature` (BME280), `humidity` (BME280), `soil_moisture` (FC-28), `soil_type`, `crop_type`, `nitrogen`, `phosphorus`, `potassium`, `ph`, `rainfall`
- **Target:** Binary (`IRRIGATE` = 1, `NO_IRRIGATION` = 0)
- **Test Accuracy:** **90.80%**
- **F1 Score:** **0.8938** (Precision: 88.76%, Recall: 90.00%)
- **5-Fold CV Accuracy:** **92.00% ± 0.91%**
- **Top Features:** Rainfall offset (33.26%), Soil moisture deficit (23.66%), Soil type drainage (16.21%), Crop type Kc demand (9.89%)
- **Safety Rule:** Generates explainable reason codes (`RUN:MOISTURE_LOW`, `RUN:WATER_DEFICIT`, `SKIP:RAIN_CONTEXT`, `SKIP:MOISTURE_ADEQUATE`).

---

## 3. Directory Layout

```
TERRAFLOW_BIOAI/
│
├── datasets/
│   ├── Crop_recommendation.csv             # Kaggle source
│   ├── crop_recommendation_clean.csv       # Preprocessed
│   ├── Fertilizer Prediction.csv           # Kaggle source
│   ├── fertilizer_recommendation_clean.csv # Augmented (20x)
│   ├── soil_type_classification.csv        # Agronomic reference dataset
│   └── irrigation_prediction.csv           # FAO-56 aligned dataset
│
├── models/
│   ├── crop_recommendation/                # model.joblib, scaler.joblib, metadata.json
│   ├── fertilizer_recommendation/          # model.joblib, scaler.joblib, metadata.json
│   ├── soil_type_classification/           # model.joblib, scaler.joblib, metadata.json
│   └── irrigation_prediction/              # model.joblib, scaler.joblib, metadata.json
│
├── ml_pipeline/
│   ├── __init__.py
│   ├── sensor_config.py                    # Sensor ranges & feature mapping specifications
│   ├── prepare_datasets.py                 # Data preprocessing and generation
│   ├── train_models.py                     # Training script for all 4 models
│   ├── inference.py                        # Unified predictor class & demo
│   └── api_server.py                       # Flask REST API server for ESP32
│
└── esp32_firmware/
    └── esp32_gateway.ino                   # ESP32 C++ firmware for UART + HTTP ML calls
```

---

## 4. How to Run

### Step 1: Run Inference Demo
Test all 4 models with simulated field scenarios:
```powershell
python -m ml_pipeline.inference
```

### Step 2: Start REST API Server for ESP32
Start the local server listening on port 5000:
```powershell
python -m ml_pipeline.api_server
```

Endpoints available:
- `GET  /api/health`
- `POST /api/predict/irrigation`
- `POST /api/predict/crop`
- `POST /api/predict/soil`
- `POST /api/predict/fertilizer`
- `POST /api/predict/full`

### Step 3: Re-train Models (if dataset changes)
```powershell
python -m ml_pipeline.prepare_datasets
python -m ml_pipeline.train_models
```

