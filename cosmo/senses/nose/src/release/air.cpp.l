/*
Important: Connect GND from EXT USB/supply to BOTH:
  (1) Senseair S8 GND 
  (2) ESP32 GND 

ESP32 S3 pinout to Senseair S8 CO2 sensor
        TX  -> 9
        RX  -> 10
        GND -> GND from EXT USB/supply
        5V  -> +5V from EXT USB/supply

For now, feel free to use my keys — that gives you up to 6 million smell detections each month.

# Define below WIFI SSID/password in config.h

// COSMO server endpoint
const char* url = "https://rest.ably.io/channels/cosmo_face/messages";
const char* key = "CClXdw.Z3P7Fw";
const char* secret = "G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE";

const char* ssid = "";
const char* password = "";
*/

#include "config.h"
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// =======================
// Senseair S8 UART config
// =======================
#define CO2_RX_PIN 9   // ESP32 RX  ← S8 TX
#define CO2_TX_PIN 10  // ESP32 TX  → S8 RX

HardwareSerial co2Serial(1);

// Senseair S8 CO₂ read command
uint8_t readCO2Cmd[7] = {0xFE, 0x44, 0x00, 0x08, 0x02, 0x9F, 0x25};
uint8_t response[7];

// =======================
// COSMO timing
// =======================
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 10000; // 10 seconds

// =======================
// WiFi + COSMO
// =======================
void sendToCosmo(int co2ppm) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi not connected");
    return;
  }

  HTTPClient http;

   String payload = "{ \"name\": \"cURL\", \"data\": \"air\" }";

  Serial.println("Sending to COSMO:");
  Serial.println(payload);

  http.begin(url);
  http.setAuthorization(key, secret);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Ably-Version", "2.0");

  int httpResponseCode = http.POST(payload);

  Serial.print("HTTP code: ");
  Serial.println(httpResponseCode);

  if (httpResponseCode > 0) {
    Serial.println("COSMO response:");
    Serial.println(http.getString());
  } else {
    Serial.println("POST failed");
  }

  http.end();
}

// =======================
// Setup
// =======================
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("START");

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to COSMO");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to COSMO");
  Serial.println("COSMO brain loaded");

  // Senseair S8 UART
  co2Serial.begin(9600, SERIAL_8N1, CO2_RX_PIN, CO2_TX_PIN);

  Serial.println("COSMO nose (Senseair S8) initialized");

  Serial.println("Warming up nose (60s recommended)...");
}

// =======================
// Loop
// =======================
void loop() {
  // Request CO₂
  co2Serial.write(readCO2Cmd, 7);
  
  // Wait a little for response
  delay(100);

  // Read response safely
  int bytes = co2Serial.available();
  if (bytes >= 7) {
    for (int i = 0; i < 7; i++) {
      response[i] = co2Serial.read();
    }

    int co2ppm = response[3] * 256 + response[4];

    Serial.print("CO2: ");
    Serial.print(co2ppm);
    Serial.println(" ppm");

    // Send to COSMO if CO₂ > threshold
    if (co2ppm > 1200 && millis() - lastSendTime > sendInterval) {
      Serial.println("COSMO need fresh air");
      sendToCosmo(co2ppm);
      lastSendTime = millis();
    }

  } else {
    Serial.print("COSMO nose not ready, bytes available: ");
    Serial.println(bytes);
  }

  delay(2000);
}