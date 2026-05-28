#ifndef WIFI_H
#define WIFI_H

#include "settings.h"

#if defined(DEVICE_HARDWARE_ESP8266)
    #include "hardware/esp8266/driver_wifi.h"
#elif defined(DEVICE_HARDWARE_BK7231N)
    #include "hardware/bk7231n/driver_wifi.h"
#endif

#define RECONNECT_INTERVAL 5000

namespace Wifi {

    struct State {
        uint32_t lastTime = 0;
        bool isConnected = false;
    };

    inline static State _state;

    inline bool isConnected() {
        return _state.isConnected;
    }

    inline void setup() {

        Hardware::Wifi::setup(Settings::config.deviceID);

        Hardware::Wifi::begin(Settings::config.wifiSSID, Settings::config.wifiPass);
        _state.lastTime = millis();
    }

    inline void update() {

        uint32_t now = (uint32_t) millis();

        if (_state.isConnected) {

            if (now - _state.lastTime < 60000) return;
            
            if (!Hardware::Wifi::isConnected()) {
                _state.isConnected = false;
                _state.lastTime = now;
            } 

            return;
        }

        if (!Hardware::Wifi::isConnected()) {

            if (now - _state.lastTime > RECONNECT_INTERVAL) {
                WiFi.disconnect(false);
                _state.lastTime = now;
                Hardware::Wifi::begin(Settings::config.wifiSSID, Settings::config.wifiPass);
            }
        } 
        
        else {
            _state.isConnected = true;
            _state.lastTime = now;
        }
    }
}

#endif