#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"

#define SENSOR_PIN 10
#define MAINS_VOLTAGE 250
#define COEFF 2.85

const int samples = 4000;

// SCT-013-030 calibration
// Adjust after testing with known load
float calibrationFactor = 30.0;

// Remove idle sensor reading
float zeroOffset = 0.35;

// Ignore readings below this
float noiseThreshold = 0.05;

WiFiClient espClient;
PubSubClient mqttClient(espClient);

void connectWiFi()
{
  Serial.print("Connecting to WiFi");

  WiFi.begin(
      WIFI_SSID,
      WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void connectMQTT()
{
  while (!mqttClient.connected())
  {

    Serial.print("Connecting MQTT...");

    if (mqttClient.connect(
            "ESP32S3-SCT013",
            MQTT_USER,
            MQTT_PASSWORD))
    {

      Serial.println("connected");
    }
    else
    {

      Serial.print("failed ");
      Serial.println(mqttClient.state());

      delay(5000);
    }
  }
}

float readCurrent()
{

  double sum = 0;
  double sumSquares = 0;

  // Find ADC midpoint

  for (int i = 0; i < samples; i++)
  {

    int adc = analogRead(SENSOR_PIN);

    sum += adc;

    delayMicroseconds(80);
  }

  float offset = sum / samples;

  // RMS calculation

  for (int i = 0; i < samples; i++)
  {

    int adc = analogRead(SENSOR_PIN);

    float signal = adc - offset;

    sumSquares += signal * signal;

    delayMicroseconds(80);
  }

  float rmsADC =
      sqrt(sumSquares / samples);

  // ADC volts

  float rmsVoltage =
      rmsADC *
      (3.3 / 4095.0);

  // SCT-013-030
  // 1V RMS = 30A RMS

  float current =
      rmsVoltage *
      calibrationFactor;

  // Remove idle noise

  current -= zeroOffset;

  if (current < noiseThreshold)
  {
    current = 0;
  }

  return current;
}

void setup()
{

  Serial.begin(115200);

  delay(2000);

  Serial.println();
  Serial.println("ESP32-S3 SCT-013-030 Energy Monitor");

  analogReadResolution(12);

  analogSetPinAttenuation(
      SENSOR_PIN,
      ADC_11db);

  connectWiFi();

  mqttClient.setServer(
      MQTT_SERVER,
      MQTT_PORT);
}

void loop()
{

  if (!mqttClient.connected())
  {
    connectMQTT();
  }

  mqttClient.loop();

  float current = readCurrent();

  // Calculate watts
  int watts =
      current * MAINS_VOLTAGE * COEFF;

  if (watts < 10)
  {
    watts = 0;
  }

  Serial.print("Current: ");
  Serial.print(current, 2);
  Serial.println(" A");

  Serial.print("Power: ");
  Serial.print(watts);
  Serial.println(" W");

  char payload[20];

  snprintf(
      payload,
      sizeof(payload),
      "%d",
      watts);

  // Publish watts
  mqttClient.publish(
      MQTT_TOPIC,
      payload,
      true);

  delay(5000);
}