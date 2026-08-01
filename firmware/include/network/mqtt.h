#ifndef MQTT_H
#define MQTT_H

#include <PubSubClient.h>

#include "settings.h"
#include "wifi.h"

#define RECONNECT_INTERVAL 5000

namespace Mqtt {

    struct State {
        uint32_t lastTime = 0;
        bool isConnected = false;
    };

    struct Topics {

        char def[Sizes::MQTT];
        char global[Sizes::MQTT];

        char cmd[Sizes::MQTT];
        char admin[Sizes::MQTT];
        char state[Sizes::MQTT];
    };

    static Topics topics;

    static State _state;
    static WiFiClient _wifiClient;
    static PubSubClient _client(_wifiClient);

    void setCallback(MQTT_CALLBACK_SIGNATURE) {
        _client.setCallback(callback);
    }

    bool isConnected() {
        return _state.isConnected;
    }

    void setup() {

        if (strlen(Settings::config.deviceID) == 4) {
            snprintf(topics.def, Sizes::MQTT, "def/%s/a", Settings::config.deviceID);
            snprintf(topics.state, Sizes::MQTT, "def/%s/s",  Settings::config.deviceID);
        }

        else {
            snprintf(topics.cmd,   Sizes::MQTT, "tp/%s/c",  Settings::config.deviceID);
            snprintf(topics.admin, Sizes::MQTT, "tp/%s/a",  Settings::config.deviceID);
            snprintf(topics.state, Sizes::MQTT, "tp/%s/s",  Settings::config.deviceID);
        }
            
        snprintf(topics.global, Sizes::MQTT, "tp/a/c");

        _client.setServer(Settings::config.mqttIP, Settings::config.mqttPort);
        _client.setBufferSize(Sizes::MQTT_BUFFER); 
        _client.setSocketTimeout(10);
        _client.setKeepAlive(30); 
    }

    void update() {

        uint32_t now = millis();

        if (_state.isConnected) {

            if (!_client.connected()) {
                _state.isConnected = false;
                _state.lastTime = now;
            } 

            else _client.loop();
            return;
        }

        if (!_client.connected()) {

            if (_state.lastTime == 0) {_state.lastTime = now + 3000; return;}

            if (now - _state.lastTime > RECONNECT_INTERVAL) {

                const char offlineByte = 0xFF;

                _state.lastTime = now;
                _client.disconnect();

                _client.connect(
                    Settings::config.deviceID,
                    Settings::config.mqttUser,
                    Settings::config.mqttPass,

                    topics.state, 1, false,
                    &offlineByte, 1
                );
            }

        } else {
            _state.isConnected = true;
            _state.lastTime = now;

            if (strlen(Settings::config.deviceID) == 4) _client.subscribe(topics.def);
            else {
                _client.subscribe(topics.cmd);
                _client.subscribe(topics.admin);
            }

            _client.subscribe(topics.global);
        }
    }
}

#endif // MQTT_H