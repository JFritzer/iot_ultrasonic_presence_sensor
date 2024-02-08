/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-hc-sr04-ultrasonic-arduino/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/
#include <WiFi.h>
#include <PubSubClient.h>
#define SOUND_SPEED 0.0343
const int trigPin = 5;
const int echoPin = 18;
long duration;
float distanceCm;
float distanceInch;

const char* ssid = "Pixel_6939";
const char* password = "12356789";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
const char* mqtt_server = "158.180.44.197";

void setup() {
  Serial.begin(115200);
  delay(1000);

  +WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  client.setServer(mqtt_server, 1883);
  if (client.connect("arduinoClient", "bobm", "letmein")) {
    client.publish("homie/ESP32_Studentenlabor_1/$homie","3.0", true);
    client.publish("homie/ESP32_Studentenlabor_1/$name", "ESP32_Studentenlabor_1", true);
    client.publish("homie/ESP32_Studentenlabor_1/$nodes", "distance", true);
    client.publish("homie/ESP32_Studentenlabor_1/distance/$name", "HC-SR04 Ultrasonic Sensor", true);
    client.publish("homie/ESP32_Studentenlabor_1/distance/$property", "distance", true);
    client.publish("homie/ESP32_Studentenlabor_1/distance/$unit", "cm", true);
  }
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_SPEED/2;
  
  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  char distancestr[8];
  dtostrf(distanceCm, 1, 2, distancestr);
  client.publish("homie/ESP32_Studentenlabor_1/distance", distancestr);
  delay(1000);
}