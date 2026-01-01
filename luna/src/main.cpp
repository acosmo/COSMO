#include "config.h"   // Wi-Fi & server settings
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <LittleFS.h>

ESP8266WebServer server(80);

// Motor pins
#define IN1 D1
#define IN2 D2
#define IN3 D3
#define IN4 D4
#define ENA D5
#define ENB D6

int speedVal = 120;   // Default speed works (120-200)

void listFiles() {
  Serial.println("Listing files on LittleFS:");
  Dir dir = LittleFS.openDir("/");
  while (dir.next()) {
    Serial.print("FILE: ");
    Serial.print(dir.fileName());
    Serial.print("|SIZE: ");
    Serial.println(dir.fileSize());
  }
}

// ================= UI =================
void handleRoot() {
  File file = LittleFS.open("/luna.html", "r");
  if(!file){
    server.send(500, "text/plain", "File not found");
    Serial.println("File not found: /luna.html");
    return;
  }
  server.streamFile(file, "text/html");
  file.close();
}

// ================= MOTOR FUNCTIONS =================
void forward() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);

}

void backward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
}

void left() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void right() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void stopMotor() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

// ================= CONTROL HANDLERS =================
void handleMove() {
  String dir = server.arg("dir");
  Serial.println(dir);

  if (dir == "F") forward();
  else if (dir == "B") backward();
  else if (dir == "L") left();
  else if (dir == "R") right();
  else stopMotor();

  server.send(200, "text/plain", "OK");
}

void handleSpeed() {
  speedVal = server.arg("val").toInt();
  analogWrite(ENA, speedVal);
  analogWrite(ENB, speedVal);
  server.send(200, "text/plain", "Speed Set");
}



void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  stopMotor();
  analogWrite(ENA, speedVal);
  analogWrite(ENB, speedVal);

  // Initialize LittleFS
  if(!LittleFS.begin()){
    Serial.println("Failed to mount LittleFS");
    return;
  }

  listFiles();  // <-- Debug: show all files on LittleFS

  // Setup Wi-Fi
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to COSMO");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to COSMO");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Setup server routes
  server.on("/", handleRoot);
  server.on("/move", handleMove);
  server.on("/speed", handleSpeed);

  server.begin();
  Serial.println("LUNA server started");

  // Serve all static files in LittleFS (images, css, etc.)
  server.serveStatic("/", LittleFS, "/");  
}

void loop() {
  server.handleClient();
}