/*
 * TerraFlow BioAI - ESP32 Gateway Firmware Sample
 * 
 * Hardware:
 *   - ESP32 DevKit V1
 *   - UART connection to STM32F103C8T6 (UART2: GPIO 16 RX, GPIO 17 TX)
 *   - Wi-Fi connection to LAN / Cloud backend
 * 
 * Function:
 *   1. Receives filtered sensor telemetry from STM32 over UART
 *   2. Formats payload matching the ML Pipeline API
 *   3. Calls POST /api/predict/full (or /api/predict/irrigation)
 *   4. Forwards ML decision support & reason codes back to STM32
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Wi-Fi Credentials
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// TerraFlow ML API Server URL
const char* ML_SERVER_URL = "http://192.168.1.100:5000/api/predict/full";

// UART2 for communication with STM32F103C8T6
#define RXD2 16
#define TXD2 17

// Zone Static Configuration (matches Supabase zones table)
const char* ZONE_ID   = "Z01";
const char* SOIL_TYPE = "Black";
const char* CROP_TYPE = "Rice";

// Default / latest soil test inputs (from Supabase soil_tests)
float soil_n  = 80.0;
float soil_p  = 40.0;
float soil_k  = 150.0;
float soil_ph = 7.2;

void setup() {
  Serial.begin(115200);      // USB Debug Console
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2); // Link to STM32

  Serial.println("\n[TerraFlow BioAI] ESP32 Gateway starting...");

  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[Wi-Fi] Connected! IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\n[Wi-Fi] Connection failed. Will run offline buffering.");
  }
}

void loop() {
  // Check if STM32 has sent a telemetry packet over Serial2
  if (Serial2.available()) {
    String incomingJson = Serial2.readStringUntil('\n');
    incomingJson.trim();

    if (incomingJson.length() > 0) {
      Serial.println("[STM32 RX]: " + incomingJson);
      processTelemetry(incomingJson);
    }
  }

  delay(50);
}

void processTelemetry(String rawJson) {
  // Parse incoming STM32 packet
  StaticJsonDocument<512> stmDoc;
  DeserializationError err = deserializeJson(stmDoc, rawJson);
  if (err) {
    Serial.print("[JSON] Parse failed: ");
    Serial.println(err.c_str());
    return;
  }

  // Extract STM32 sensor readings
  // BME280 readings
  float temp     = stmDoc["air_temp"] | 28.0;
  float humidity = stmDoc["humidity"] | 60.0;
  // Soil moisture (Kalman-filtered by STM32)
  float moisture = stmDoc["moisture"] | 30.0;
  // Water TDS (from TDS Meter V1.0)
  float tds      = stmDoc["tds"]      | 200.0;

  // Prepare ML payload
  StaticJsonDocument<512> reqDoc;
  reqDoc["temperature"]   = temp;
  reqDoc["humidity"]      = humidity;
  reqDoc["soil_moisture"] = moisture;
  reqDoc["soil_type"]     = SOIL_TYPE;
  reqDoc["crop_type"]     = CROP_TYPE;
  reqDoc["nitrogen"]      = soil_n;
  reqDoc["phosphorus"]    = soil_p;
  reqDoc["potassium"]     = soil_k;
  reqDoc["ph"]            = soil_ph;
  reqDoc["rainfall"]      = 0.0; // In production, fetch from OpenWeatherMap API

  String reqBody;
  serializeJson(reqDoc, reqBody);

  // Call TerraFlow ML Server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(ML_SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(reqBody);
    if (httpCode == HTTP_CODE_OK) {
      String response = http.getString();
      Serial.println("[ML Server Response]: " + response);

      // Parse ML decision and send advice packet back to STM32
      StaticJsonDocument<1024> respDoc;
      deserializeJson(respDoc, response);

      const char* decision   = respDoc["irrigation"]["prediction"] | "NO_IRRIGATION";
      float confidence       = respDoc["irrigation"]["confidence"] | 0.0;
      const char* reasonCode = respDoc["irrigation"]["reason_code"] | "UNKNOWN";

      // Build advice frame for STM32
      StaticJsonDocument<256> adviceDoc;
      adviceDoc["type"]       = "ADVISORY";
      adviceDoc["irrigate"]   = (strcmp(decision, "IRRIGATE") == 0) ? 1 : 0;
      adviceDoc["confidence"] = confidence;
      adviceDoc["reason"]     = reasonCode;

      String advicePacket;
      serializeJson(adviceDoc, advicePacket);
      advicePacket += "\n";

      // Send to STM32 local safety authority
      Serial2.print(advicePacket);
      Serial.println("[STM32 TX Advice]: " + advicePacket);
    } else {
      Serial.printf("[HTTP] POST failed, error: %s (code %d)\n", http.errorToString(httpCode).c_str(), httpCode);
    }
    http.end();
  } else {
    Serial.println("[Gateway] Offline. STM32 operates autonomously under local safety rules.");
  }
}

