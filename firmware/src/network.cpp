#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <actions.h>
#include <config.h>
#include <pins.h>

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {

    if (!strcmp(topic, config.set_topic)) { 

        if (length == 2 && !memcmp(payload, "UP", 2))    handle_button_action(BTN_TOP, 200); 
        else if(length == 4) {
            if (!memcmp(payload, "STOP", 4)) handle_button_action(BTN_MID, 200);
            else if (!memcmp(payload, "DOWN", 4)) handle_button_action(BTN_BOTTOM, 200);
        }
    } 

    else if (!strcmp(topic, config.admin_topic)) {
        return;
    }
}

void topic_setup() {

    // tphome/blinds/lounge/big-blind/set
    // tphome/blinds/lounge/big-blind/state
    // tphome/admin/DEVICE_ID

    snprintf(config.set_topic, sizeof(config.set_topic), "tphome/blinds/%s/%s/set", config.room, config.name);
    snprintf(config.state_topic, sizeof(config.state_topic), "tphome/blinds/%s/%s/state", config.room, config.name);
    snprintf(config.admin_topic, sizeof(config.admin_topic), "tphome/admin/%s", config.device_id);
}

void network_setup() {

    // Wi-Fi configuration
    WiFi.mode(WIFI_STA);
    WiFi.begin(config.wifi_ssid, config.wifi_password);
    
    // MQTT server configuration
    client.setServer(config.mqtt_server, 1883);
    client.setCallback(callback);

    // Topic setup
    topic_setup();
}

// Function to connect to the MQTT server with its credentials
// and also to subscribe to the corresponding topic
bool mqtt_reconnect() {

    if (client.connect(config.device_id, config.mqtt_user, config.mqtt_pass)) {
        
        client.subscribe(config.set_topic); 
        client.subscribe(config.admin_topic);
        client.publish(config.state_topic, "CONNECTED", true);
        
        blink(LED_GREEN, 0); return true;

    } return false;
}

void network_check() {

    // This line activates the green_led while the wifi is not connected
    if (WiFi.status() != WL_CONNECTED) {if (!config.is_blinking) { blink(LED_GREEN, 1); config.blink_time = 500; } return; } 

    // Gestión de MQTT
    if (!client.connected()) {

        // Section to control blinking led when mqtt server disconnects
        if (!config.is_blinking) blink(LED_GREEN, 1);
        config.blink_time = 1000;

        // This lines below manage a 5 second delay 
        // to reattempt the connection to the MQTT server
        static unsigned long last_reconnect_attempt = 0;
        if (millis() - last_reconnect_attempt > 5000) { 
            last_reconnect_attempt = millis();

            // This line calls the mqtt_reconnect function 
            // to check if the connection is available and successful
            if (mqtt_reconnect()) last_reconnect_attempt = 0;
        }
    } 
    
    // This line continues the loop of the client while Wi-Fi and MQTT server are connected,
    // the client loop is where topics and messages are redirected to callback 
    else client.loop();
}