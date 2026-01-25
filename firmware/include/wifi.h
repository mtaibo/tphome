#ifndef WIFI
#define WIFI

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

extern WiFiClient espClient;
extern PubSubClient client;

void setup_wifi();
void reconnect();
void callback(char* topic, byte* payload, unsigned int length);

#endif