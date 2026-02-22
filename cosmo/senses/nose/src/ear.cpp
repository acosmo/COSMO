#include "config.h"       // contains: const char* ssid / password / server
#include <Arduino.h>
#include <driver/i2s.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <math.h>

// ------------------- I2S Pins -------------------
#define I2S_WS   17  // LRCL
#define I2S_SD   15  // DOUT
#define I2S_SCK  18  // BCLK

// ------------------- WebSocket -------------------
WebSocketsClient webSocket;

// ------------------- VAD -------------------
const int16_t VAD_THRESHOLD = 100;       // RMS threshold
const int VAD_SILENCE_FRAMES = 10;       // padding frames to avoid cutting speech
int silenceCounter = 0;

// ------------------- RMS / flush timing -------------------
unsigned long lastRMSPrint = 0;
#define FLUSH_INTERVAL_MS 300
unsigned long lastFlush = 0;

// ------------------- Send buffer -------------------
#define SEND_BUFFER_SIZE 512
static int16_t sendBuffer[SEND_BUFFER_SIZE];
int sendBufferIndex = 0;

// ------------------- RMS calculation -------------------
float calcRMS(int16_t* buffer, int samples) {
  if (samples <= 0) return 0;
  uint64_t sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += (int32_t)buffer[i] * (int32_t)buffer[i];
  }
  return sqrt((float)sum / samples);
}

// ------------------- VAD detection -------------------
bool hasSound(int16_t* buffer, int samples) {
  for (int i = 0; i < samples; i++) {
    if (abs(buffer[i]) > VAD_THRESHOLD) return true;
  }
  return false;
}

// ------------------- WebSocket events -------------------
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_CONNECTED:
      Serial.println("[WS] Connected");
      break;
    case WStype_DISCONNECTED:
      Serial.println("[WS] Disconnected");
      break;
    case WStype_TEXT:
      Serial.print("[SERVER] "); Serial.println((char*)payload);
      break;
    case WStype_ERROR:
      Serial.println("[WS] Error");
      break;
    default: break;
  }
}

// ------------------- Setup -------------------
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("START");

  // -------- WiFi --------
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // -------- I2S configuration --------
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = 0,
    .dma_buf_count = 4,
    .dma_buf_len = 256,
    .use_apll = false
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num  = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num  = I2S_SD
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
  Serial.println("INMP441 initialized!");

  // -------- WebSocket --------
  webSocket.begin(cosmo_stt_server, cosmo_stt_server_port, "/");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(3000);
}

// ------------------- Main Loop -------------------
void loop() {
  webSocket.loop();

  static int32_t i2sBuffer[256];
  size_t bytesRead;
  i2s_read(I2S_NUM_0, i2sBuffer, sizeof(i2sBuffer), &bytesRead, portMAX_DELAY);
  int samples = bytesRead / 4;

  // Convert 32-bit -> 16-bit PCM
  int16_t pcm16[256];
  for (int i = 0; i < samples; i++) {
    pcm16[i] = i2sBuffer[i] >> 14;
  }

  // Compute RMS & VAD
  float rms = calcRMS(pcm16, samples);
  bool soundDetected = rms > VAD_THRESHOLD;

  // Update silence counter
  if (soundDetected) {
    silenceCounter = 0;
  } else {
    silenceCounter++;
  }

  // Append samples to send buffer
  for (int i = 0; i < samples; i++) {
    sendBuffer[sendBufferIndex++] = pcm16[i];

    // If buffer full, flush
    if (sendBufferIndex >= SEND_BUFFER_SIZE) {
      if (webSocket.isConnected()) {
        webSocket.sendBIN((uint8_t*)sendBuffer, sendBufferIndex * 2);
      }
      sendBufferIndex = 0;
    }
  }

  // -------- Flush logic --------
  unsigned long now = millis();

  // Flush immediately when we detect silence (end of speech)
  if (!soundDetected && sendBufferIndex > 0) {
      float bufferRMS = calcRMS(sendBuffer, sendBufferIndex);
      if (bufferRMS > VAD_THRESHOLD) {   // Only send if meaningful audio
          if (webSocket.isConnected()) {
              webSocket.sendBIN((uint8_t*)sendBuffer, sendBufferIndex * 2);
          }
      }
      sendBufferIndex = 0;
  } 
  // Otherwise, periodic flush every FLUSH_INTERVAL_MS
  else if (now - lastFlush >= FLUSH_INTERVAL_MS) {
      lastFlush = now;
      if (sendBufferIndex > 0) {
          float bufferRMS = calcRMS(sendBuffer, sendBufferIndex);
          if (bufferRMS > VAD_THRESHOLD) {  // Only send if audio exists
              if (webSocket.isConnected()) {
                  webSocket.sendBIN((uint8_t*)sendBuffer, sendBufferIndex * 2);
              }
          }
          sendBufferIndex = 0;
      }
  }

  // -------- Print RMS for debug --------
  if (now - lastRMSPrint >= 1000) {
    lastRMSPrint = now;
    if (soundDetected) {
      Serial.printf("[VAD] SOUND  RMS=%.2f\n", rms);
    } else {
      Serial.printf("[VAD] SILENCE RMS=%.2f\n", rms);
    }
  }
}