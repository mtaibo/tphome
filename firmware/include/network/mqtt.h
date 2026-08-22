#ifndef MQTT_H
#define MQTT_H

#include <PubSubClient.h>

#include "settings.h"
#include "wifi.h"
#include "diagnostics.h"

#define RECONNECT_INTERVAL_MIN  5000
#define RECONNECT_INTERVAL_MAX 60000

namespace Mqtt {

    enum LogEvent : uint8_t {
        LOG_BOOT           = 0x01,
        LOG_MQTT_CONNECTED = 0x20,
        LOG_FLASH_WRITE    = 0x30,
    };

    struct State {
        uint32_t lastTime = 0;
        uint32_t reconnectInterval = RECONNECT_INTERVAL_MIN;
        bool isConnected = false;
        bool firstConnect = true;
        uint16_t lastReportedFlashWrites = 0;
    };

    struct Topics {
        char def[Sizes::MQTT];
        char global[Sizes::MQTT];
        char cmd[Sizes::MQTT];
        char admin[Sizes::MQTT];
        char state[Sizes::MQTT];
        char log[Sizes::MQTT];
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

    inline void _publishLog(uint8_t code) {
        _client.publish(topics.log, &code, 1);
    }

    inline void _publishLog(uint8_t code, const uint8_t* data, uint8_t len) {
        uint8_t buf[8];
        buf[0] = code;
        memcpy(buf + 1, data, len < 7 ? len : 7);
        _client.publish(topics.log, buf, 1 + (len < 7 ? len : 7));
    }

    inline void _checkAndReportFlashWrites() {
        if (Diagnostics::flashWrites != _state.lastReportedFlashWrites) {
            _state.lastReportedFlashWrites = Diagnostics::flashWrites;
            uint8_t data[2] = {
                (uint8_t)(Diagnostics::flashWrites & 0xFF),
                (uint8_t)(Diagnostics::flashWrites >> 8)
            };
            _publishLog(LOG_FLASH_WRITE, data, 2);
        }
    }

    void setup() {

        if (strlen(Settings::config.deviceID) == 4) {
            snprintf(topics.def,   Sizes::MQTT, "def/%s/a", Settings::config.deviceID);
            snprintf(topics.state, Sizes::MQTT, "def/%s/s", Settings::config.deviceID);
        }
        else {
            snprintf(topics.cmd,   Sizes::MQTT, "tp/%s/c",  Settings::config.deviceID);
            snprintf(topics.admin, Sizes::MQTT, "tp/%s/a",  Settings::config.deviceID);
            snprintf(topics.state, Sizes::MQTT, "tp/%s/s",  Settings::config.deviceID);
        }

        snprintf(topics.global, Sizes::MQTT, "tp/a/c");
        snprintf(topics.log,    Sizes::MQTT, "tp/%s/l",  Settings::config.deviceID);

        _client.setServer(Settings::config.mqttIP, Settings::config.mqttPort);
        _client.setBufferSize(Sizes::MQTT_BUFFER);
        _client.setSocketTimeout(10);
        _client.setKeepAlive(60);
    }

    void update() {

        uint32_t now = millis();

        if (_state.isConnected) {

            if (!_client.connected()) {
                _state.isConnected = false;
                _state.lastTime = now;
            }
            else {
                _client.loop();
                _checkAndReportFlashWrites();
            }
            return;
        }

        if (!_client.connected()) {

            if (_state.lastTime == 0) {_state.lastTime = now + 3000; return;}

            if (now - _state.lastTime > _state.reconnectInterval) {

                const char offlineByte = 0xFF;

                _state.lastTime = now;
                _state.reconnectInterval = min(_state.reconnectInterval * 2, (uint32_t) RECONNECT_INTERVAL_MAX);
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
            _state.reconnectInterval = RECONNECT_INTERVAL_MIN;

            _publishLog(_state.firstConnect ? LOG_BOOT : LOG_MQTT_CONNECTED);
            _state.firstConnect = false;
            _checkAndReportFlashWrites();

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
