#include "config.h"   // Wi-Fi & server settings
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// for different cable/charger/power supply you need to cilibrate and find your TOUCH_THRESHOLD
// short  cables > 50-70K
// medium cables > 70-90K
// long   cables > 90-100K
#define TOUCH_THRESHOLD 100000 // 100K USB PC | 90K Socket Cable

#define DEBOUNCE_MS 5000   // 5 seconds

// Last time we sent for each pin
unsigned long lastSendTime4 = 0;
unsigned long lastSendTime7 = 0;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to COSMO");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to COSMO");
}

void sendToCosmo(int sense) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = String(serverUrl) + "/ask" + String(sense);

    Serial.println("Activating COSMO " + String(url) + " via " + WiFi.localIP().toString());

    http.begin(url); // HTTP GET request
    int httpResponseCode = http.GET(); // send GET request

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("COSMO response: " + response);
    } else {
      Serial.println("Error sending: " + String(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("Wi-Fi not connected");
  }
}

void loop() {
  unsigned long now = millis();

  // COSMO with 6 touch senses: GPIO pins 2–7 fully functional.
  int pin2 = touchRead(2);
  int pin3 = touchRead(3);
  int pin4 = touchRead(4); //Speech
  int pin5 = touchRead(5);
  int pin6 = touchRead(6);
  int pin7 = touchRead(7); //Joke

  // pin 4
  if (pin4 > TOUCH_THRESHOLD && (now - lastSendTime4 > DEBOUNCE_MS)) {
    Serial.print("Sense Touch and Speech:"); Serial.println(pin4);
    sendToCosmo(4);
    lastSendTime4 = now;
  }

  // pin 7
  if (pin7 > TOUCH_THRESHOLD && (now - lastSendTime7 > DEBOUNCE_MS)) {
    Serial.print("Sense Joke:"); Serial.println(pin7);
    sendToCosmo(7);
    lastSendTime7 = now;
  }

  delay(50);
}