#ifndef DEFAULTS_H
#define DEFAULTS_H

#include <stdint.h>
#include <string.h>

#include "settings.h"

/* ---  Network  ---- */
#include "credentials.h"

/* --- Config Sizes --- */
#define IDENTITY_SIZE 16
#define WIFI_SIZE     32
#define MQTT_SIZE     24

#define NO_PIN        255

namespace Defaults {

    /* --- Identification --- */
    static constexpr char ID []   = "B364859";
    static constexpr char ROOM [] = "bedroom";
    static constexpr char NAME [] = "blind";

    /* --- Timings & Preferences --- */
    static constexpr uint16_t SHORT_PULSE      = 100;  // 1.00s
    static constexpr uint16_t LONG_PULSE       = 500;  // 5.00s
    static constexpr uint16_t UP_TIME          = 4000; // 40.00s
    static constexpr uint16_t DOWN_TIME        = 4000; // 40.00s
    static constexpr uint16_t DOWN_POSITION    = 2000; // 20.00%
    static constexpr uint16_t MOTOR_SAFE_TIME  = 100;  // 1.00s

    /* --- Initial State --- */
    static constexpr uint16_t START_POSITION   = 5000; // 50.00%

    /* Function to apply defaults settings to current settings */
    inline void apply() {

        auto& c = Settings::config;
        auto& p = Settings::prefs;
        auto& s = Settings::state;

        /* --- Identification --- */
        strlcpy(c.device_id, ID, IDENTITY_SIZE);
        strlcpy(c.room, ROOM, IDENTITY_SIZE);
        strlcpy(c.name, NAME, IDENTITY_SIZE);

        /* ---  Network  ---- */
        strlcpy(c.wifi_ssid, WIFI_SSID, WIFI_SIZE);
        strlcpy(c.wifi_pass, WIFI_PASS, WIFI_SIZE);
        strlcpy(c.mqtt_ip, MQTT_IP, MQTT_SIZE);
        strlcpy(c.mqtt_user, MQTT_USER, MQTT_SIZE);
        strlcpy(c.mqtt_pass, MQTT_PASS, MQTT_SIZE);
        c.mqtt_port = MQTT_PORT;

        /* --- Timings & Preferences --- */
        #if defined(DEVICE_TYPE_BLIND)
            p.up_time = UP_TIME;
            p.down_time = DOWN_TIME;
            p.motor_safe_time = MOTOR_SAFE_TIME;
            p.short_pulse = SHORT_PULSE;
            p.long_pulse = LONG_PULSE;

            s.current_position = START_POSITION;
            s.next_position = START_POSITION;
            s.is_moving = false;
        #endif
    }
}

#endif