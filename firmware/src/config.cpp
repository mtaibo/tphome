#include <Preferences.h>

#include "default.h"
#include "config.h"
#include "pins.h"

Config config;
Preferences prefs;

void load_config() {

    // * Set configuration

    // Execution data
    config.is_moving = false;
    config.is_waiting = false;

    config.active_relay = -1;
    config.active_led = -1;
    config.pending_relay = -1;
    config.pending_led = -1;

    // Time execution data
    config.pause_control = false;
    config.stop_time = 0;
    config.stop_led_time = 0;
    config.current_limit = 0;

    // Blinking config
    config.is_blinking = false;
    config.blinking_led = -1;
    config.blinking_state = -1;
    config.blink_time = 500;
    config.last_blink = 0;

    // Preferences
    config.mid_led_time = 1000;
    config.motor_safe_time = 1000;

    config.short_pulse = 3000;
    config.long_pulse = 10000;


    // * Load config from flash memory, if not found, load default settings

    prefs.begin("prefs", true);

    // Device ID
    if (prefs.getString("id", config.device_id, sizeof(config.device_id)) == 0) strcpy(config.device_id, DEVICE_ID); 

    // WIFI
    if (prefs.getString("ssid", config.wifi_ssid, sizeof(config.wifi_ssid)) == 0) strcpy(config.wifi_ssid, WIFI_SSID); 
    if (prefs.getString("wifi_pass", config.wifi_pass, sizeof(config.wifi_pass)) == 0) strcpy(config.wifi_pass, WIFI_PASS); 

    // MQTT
    if (prefs.getString("ip", config.mqtt_server, sizeof(config.mqtt_server)) == 0) strcpy(config.mqtt_server, MQTT_SERVER); 
    config.mqtt_server_port = prefs.getUInt("port", MQTT_SERVER_PORT);
    
    if (prefs.getString("user", config.mqtt_user, sizeof(config.mqtt_user)) == 0) strcpy(config.mqtt_user, MQTT_USER); 
    if (prefs.getString("mqtt_pass", config.mqtt_pass, sizeof(config.mqtt_pass)) == 0) strcpy(config.mqtt_pass, MQTT_PASS); 

    // Topic
    if (prefs.getString("type", config.type, sizeof(config.type)) == 0) strcpy(config.type, TYPE); 
    if (prefs.getString("room", config.room, sizeof(config.room)) == 0) strcpy(config.room, ROOM); 
    if (prefs.getString("name", config.name, sizeof(config.name)) == 0) strcpy(config.name, NAME); 

    // Blind config
    config.up_time = prefs.getULong("up_time", UP_TIME);
    config.down_time = prefs.getULong("down_time", DOWN_TIME);
    config.current_position = prefs.getUInt("pos", 50);

    prefs.end();
}

void save_config() {

    prefs.begin("prefs", false);

    // Device ID
    prefs.putString("id", config.device_id);

    // WIFI 
    prefs.putString("ssid", config.wifi_ssid);
    prefs.putString("wifi_pass", config.wifi_pass);

    // MQTT 
    prefs.putString("ip", config.mqtt_server);
    prefs.putUInt("port", config.mqtt_server_port);
    prefs.putString("user", config.mqtt_user);
    prefs.putString("mqtt_pass", config.mqtt_pass);

    // Topic 
    prefs.putString("type", config.type);
    prefs.putString("room", config.room);
    prefs.putString("name", config.name);

    // Blind config
    prefs.putULong("up_time", config.up_time);
    prefs.putULong("down_time", config.down_time);
    prefs.putUInt("pos", config.current_position);

    prefs.end();
}

void reset_memory() {
    prefs.begin("prefs", false);
    prefs.clear();
    prefs.end();
    delay(2000);
    ESP.restart();
}

void pin_setup() {

   // This both lines below activate the pin to allow
    // the blue leds to turn on, otherwise, they'll be blocked
    pinMode(CONFIG_LED, OUTPUT);
    digitalWrite(CONFIG_LED, HIGH);

    // Loop to turn every output pin to output mode and low
    int output_pins[] = {LED_TOP, LED_MID, LED_BOTTOM, LED_GREEN, RELAY_UP, RELAY_DOWN};
    for (int i=0; i<6; i++) {
        pinMode(output_pins[i], OUTPUT);
        digitalWrite(output_pins[i], LOW);
    }
}

void config_setup() {
    pin_setup();
    load_config();
}