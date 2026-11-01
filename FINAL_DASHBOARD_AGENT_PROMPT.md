# ==============================================================================
# TERRAFLOW BIOAI — MASTER AGENT PROMPT: FULL-STACK DASHBOARD & SYSTEM BUILD
# ==============================================================================
# Copy and paste this ENTIRE block into your AI Coding Agent (Cursor, Antigravity,
# Claude Code, or ChatGPT). It contains the complete architectural specification,
# database schema, API contracts, formulas, and UI widgets for TerraFlow BioAI.
# ==============================================================================

You are the Full-Stack Lead Engineer building the complete connected Dashboard and Backend system for "TerraFlow BioAI", an edge-IoT and AI-driven precision irrigation and multi-parametric agro-advisory platform (SPIT Mumbai Major Project).

The Machine Learning models, datasets, sensor mapping, and database schemas are already built and pushed to GitHub:
Repository: https://github.com/gauravhadavale07/TerraFlow_BioAI.git

Your job is to execute the setup, connect Supabase, run the ML API server, and build a production-grade, highly polished React web dashboard.

---

### PART 1: SETUP REPOSITORY & ML SERVER (DO THIS FIRST)
1. Clone the repository into your workspace:
   ```bash
   git clone https://github.com/gauravhadavale07/TerraFlow_BioAI.git
   cd TerraFlow_BioAI
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask ML API server in the background:
   ```bash
   python -m ml_pipeline.api_server
   ```
   (The server listens at `http://localhost:5000` with CORS enabled).

---

### PART 2: DATABASE & AGRONOMIC KNOWLEDGE BASE (SUPABASE)
The repo contains the official SQL scripts in the `/supabase` folder:
1. `supabase/schema.sql`: Contains the complete DDL for all 10 project tables:
   - `zones`, `soil_profiles`, `crop_profiles`, `crop_stages` (FAO-56 phenological stages), `irrigation_rules`, `fertilizer_rules`, `sensor_data`, `soil_tests`, `irrigation_events`, `advisories`.
2. `supabase/seed_data.sql`: Contains 80+ pre-populated rows derived from FAO-56 and ICAR standards:
   - Official FAO-56 Crop Coefficients (Kc) for Rice, Wheat, Maize, Tomato across Initial, Development, Mid-season, Late-season stages.
   - Soil hydrology baselines (Field Capacity, Wilting Point, Drainage rates) for Black, Red, Alluvial, Sandy, Clayey, Loamy soils.
   - ICAR STCR fertilizer response rules and explainable reason codes.

*Setup Instructions:* Run `schema.sql` and `seed_data.sql` in the Supabase SQL Editor. If Supabase is not configured yet, use local mock state initialized with these exact data structures so the UI never breaks.

---

### PART 3: FRONTEND APP ARCHITECTURE (REACT + VITE + TAILWIND)
Inside the project, create a new web app in a folder named `dashboard` using:
- **Framework:** Vite + React (TypeScript or JavaScript)
- **Styling:** Tailwind CSS (Dark-slate & emerald agricultural theme)
- **Icons:** `lucide-react`
- **Visualizations:** `recharts`

---

### PART 4: MANDATORY DASHBOARD SECTIONS & SPECIFICATIONS

Build a modern, single-page command console divided into 5 distinct cards/sections:

#### 1. HEADER & SYSTEM STATUS:
- Title: **"TerraFlow BioAI — Precision Irrigation & Agro-Advisory Console"**
- Metadata Badges:
  - Node: `TF01` | Management Zone: `Z01` (Plot Alpha) | Connectivity: `Online (ESP32 Gateway)`
- Operating Mode Toggle:
  - `[AUTO]` (ML & agronomic need-based automatic pump control)
  - `[MANUAL]` (Operator benchtop testing mode)
  - `[OFF]` (Emergency lock, pump disabled)
- "Demo / Simulation Mode" Toggle Switch: If toggled ON, feeds realistic simulated telemetry so the entire dashboard can be demonstrated live even without physical hardware plugged in.

#### 2. SECTION 1: LIVE SENSOR TELEMETRY & AGRO-CLIMATIC INDICES:
- **Soil Moisture Meter:**
  - Displays Kalman-Filtered Soil Moisture (%) and Raw ADC (%)
  - Visual gauge with color ranges: Red (<30% Deficit), Green (30–65% Optimal), Blue (>65% Saturated)
- **Ambient Climate Cards (BME280):**
  - Temperature (°C)
  - Relative Humidity (%RH)
  - Atmospheric Pressure (hPa)
- **Water Quality Card (TDS Meter V1.0):**
  - Total Dissolved Solids in ppm
  - Status indicator: Safe (<500 ppm), Moderate (500–1000 ppm), Saline (>1000 ppm)
- **Derived Vapor Pressure Deficit (VPD Index):**
  - Displays atmospheric drying stress in kPa:
    $$\text{VPD} = e_s - e_a \quad \text{where } e_s = 0.6108 \cdot \exp\left(\frac{17.27 \cdot T}{T + 237.3}\right), \quad e_a = e_s \cdot \frac{\text{RH}}{100}$$
  - Badge: Low Demand (<0.8 kPa), Normal (0.8–1.5 kPa), High Drying Demand (>1.5 kPa)

#### 3. SECTION 2: ZONE Z01 & SOIL TEST CONFIGURATION PANEL:
- Dropdown for **Crop**: `Rice`, `Wheat`, `Maize`, `Cotton`, `Tomato`, `Potato`, `Onion`, `Chickpea`, `Soybean`, `Groundnut`
- Dropdown for **Soil Profile**: `Black`, `Red`, `Alluvial`, `Sandy`, `Clayey`, `Loamy`
- Dropdown for **Growth Stage**: `Initial`, `Development`, `Mid-season`, `Late-season`
- Number Input for **Zone Area ($m^2$)**: Default `2.0` $m^2$
- **Soil Test NPK Inputs:**
  - Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$) in kg/ha, and $\text{pH}$
  - **"Autofill ICAR Baseline" Button:** When clicked, automatically fills standard regional ICAR benchmark values for the selected soil type (e.g. Black Soil $\rightarrow$ N=70, P=35, K=210, pH=7.6)
- **"Evaluate Zone / Run AI Advisory" Button:** Sends payload to the ML backend.

#### 4. SECTION 3: ACTUATION & CLOSED-LOOP PUMP CONTROL (EDGE AUTHORITY):
- **Pump Status Badge:** Animated glowing Green `[RUNNING]` or Slate `[IDLE]`
- **Agronomic Water Volume Math (Chapter 7):**
  $$\text{Target Volume (L)} = \text{Target Irrigation Depth (mm)} \times \text{Zone Area } (m^2)$$
  $$\text{Estimated Runtime (min)} = \frac{\text{Target Volume (L)}}{\text{Flow Rate (L/min)}}$$
- **Delivery Progress Bar:** Target Volume (L) vs Delivered Volume (L) calculated from pulse-flow sensor integration
- **Edge Hardware Safety Interlocks (STM32 Gateways):**
  - Tank Level (Float Switch): `[✓ TANK SAFE]` or `[⚠️ FAULT: TANK LOW (Pump Blocked)]`
  - Max Runtime Guard: Automatically aborts if continuous runtime exceeds 180 seconds
- **Manual Pump Action Buttons:** `[MANUAL START]` and `[EMERGENCY STOP]`

#### 5. SECTION 4: AI AGRO-ADVISORY (ML PREDICTIONS FROM `/api/predict/full`):
- **Irrigation Decision Card:**
  - Status: Big bold `IRRIGATE` (Red/Amber) or `NO_IRRIGATION` (Green)
  - Model Confidence Bar (e.g. `99.98%`) & Evidence Status (`HIGH`, `MEDIUM`, `LOW`)
  - Explainable Reason Code badge:
    - `RUN:MOISTURE_LOW`: Soil moisture below crop threshold
    - `RUN:HIGH_ET_DEMAND`: High VPD & heat causing accelerated evapotranspiration
    - `RUN:WATER_DEFICIT`: Contextual depletion exceeds allowable fraction
    - `SKIP:RAIN_CONTEXT`: Recent or forecast rainfall offset (>10 mm)
    - `SKIP:MOISTURE_ADEQUATE`: Soil water content optimal
- **Fertilizer Advisory Card:**
  - Prescribed Fertilizer: e.g. `Urea`, `DAP`, `10-26-26`, `14-35-14`, `17-17-17`
  - Nutrient deficit rationale (e.g. "Low Nitrogen (25 kg/ha) detected $\rightarrow$ Prescribed 46% N Urea top-dressing")
- **Crop Suitability Card:**
  - Top 5 suitable crops ranked with percentage score bars (e.g. Rice 91%, Maize 85%, Wheat 78%...)
- **Soil Classification Card:**
  - Identified soil class and texture description

#### 6. SECTION 5: LIVE TRENDS & CLOSED-LOOP FEEDBACK PROOF:
- **Recharts Line Graph:** Real-time plot of Soil Moisture (%) and Temperature (°C) over time
- **Closed-Loop Feedback Proof:** Demonstrates moisture rising by 15–25% after the pump finishes an irrigation event
- **Recent Events Table:**
  - Columns: Timestamp, Event Type, Target (L), Delivered (L), Reason Code, Safety Status

---

### PART 5: ML API CONNECTION SPECIFICATION
When "Evaluate Zone" is triggered, make a POST request:
`POST http://localhost:5000/api/predict/full`

Request Body JSON:
```json
{
  "temperature": 32.5,
  "humidity": 65.0,
  "soil_moisture": 28.0,
  "soil_type": "Black",
  "crop_type": "Rice",
  "nitrogen": 70.0,
  "phosphorus": 35.0,
  "potassium": 210.0,
  "ph": 7.6,
  "rainfall": 0.0
}
```
*(Note: nitrogen, phosphorus, potassium, ph can be omitted or null; the server auto-fills ICAR defaults).*

Update all advisory cards with the returned response.

---

### PART 6: 5 VIVA DEMO SCENARIOS TO TEST
Make sure the UI allows testing these 5 distinct academic scenarios via buttons or presets:
1. **Scenario 1 (Drought Stress):** Dry soil (20%), High Temp (35°C), No rain $\rightarrow$ Triggers `IRRIGATE` (`RUN:MOISTURE_LOW`), Pump runs until target volume is reached.
2. **Scenario 2 (Rainfall Offset):** Dry soil (25%), but Rainfall = 25 mm $\rightarrow$ Triggers `NO_IRRIGATION` (`SKIP:RAIN_CONTEXT`).
3. **Scenario 3 (Safety Interlock):** Tank Float Switch is LOW $\rightarrow$ Blocks actuation, raises `FAULT:TANK_LOW`.
4. **Scenario 4 (Fertilizer Deficit):** Input N=20 kg/ha $\rightarrow$ Advises `Urea`; Input P=8 kg/ha $\rightarrow$ Advises `DAP`.
5. **Scenario 5 (Crop Suitability):** Changes zone soil/climate $\rightarrow$ Dynamically updates Top 5 ranked crop percentages.

Now, generate the project, install dependencies, build the complete dashboard, and launch it!
