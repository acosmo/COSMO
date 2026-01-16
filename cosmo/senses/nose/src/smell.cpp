/*
Important: Connect WAK to GND
ESP32 S3 pinout to CCS811 sensor
        16   -> SDA
        18   -> SCL
        GND  -> WAK
        GND  -> GND
        3.3V -> VCC

For now, feel free to use my keys — that gives you up to 6 million smell detections each month.

# Define below in config.h

// COSMO server endpoint
const char* url = "https://rest.ably.io/channels/cosmo_face/messages";
const char* key = "CClXdw.Z3P7Fw";
const char* secret = "G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE";

const char* ssid = "";
const char* password = "";
*/

#include "config.h"   // Wi-Fi & server settings
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

#include <Wire.h>
#include "Adafruit_CCS811.h"

#define SDA_PIN 16
#define SCL_PIN 18

Adafruit_CCS811 ccs;

void setup() {
    Serial.begin(115200);
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to COSMO");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to COSMO");
    Serial.println("COSMO brain loaded");

    Wire.begin(SDA_PIN, SCL_PIN);

    if (!ccs.begin(CCS811_ADDRESS, &Wire)) {
        Serial.println("COSMO nose not found. Check wiring!");
        while (1);
    }

    Serial.println("COSMO nose activated");

    // IMPORTANT: start measurements
    ccs.setDriveMode(CCS811_DRIVE_MODE_1SEC);

    Serial.println("Warming up nose (2s)...");
    delay(2000);
}

void sendToCosmo(int sense) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    String payload = "{ \"name\": \"cURL\", \"data\": \"smell\" }";

    Serial.println("Sending to COSMO");
    Serial.println(payload);

    http.begin(url);

    http.setAuthorization(key, secret);

    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Ably-Version", "2.0");

    int httpResponseCode = http.POST(payload);

    Serial.print("HTTP code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("COSMO response: " + response);
    } else {
      Serial.println("POST failed");
    }

    http.end();
  } else {
    Serial.println("Wi-Fi not connected");
  }
}

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 10000; // 10 seconds between sends

void loop() {
  if (ccs.available()) {
    if (!ccs.readData()) {
      int eco2 = ccs.geteCO2();
      int tvoc = ccs.getTVOC();

      Serial.print("eCO2: ");
      Serial.print(eco2);
      Serial.print(" ppm | TVOC: ");
      Serial.print(tvoc);
      Serial.println(" ppb");

      // Send to COSMO if TVOC > 500 ppb
      if (tvoc > 50 && millis() - lastSendTime > sendInterval) {
        Serial.println("COSMO smell detected");
        sendToCosmo(0);
        lastSendTime = millis();
      }

    } else {
      Serial.println("COSMO nose read error");
    }
  } else {
    Serial.println("COSMO nose not ready yet...");
  }

  delay(1000);
}