#ifndef MQTT_H
#define MQTT_H

#include <PubSubClient.h>

#include "settings.h"
#include "wifi.h"
#include "diagnostics.h"

#if defined(DEVICE_HARDWARE_ESP8266)
    #include "hardware/esp8266/hardware.h"
#elif defined(DEVICE_HARDWARE_BK7231N)
    #include "hardware/bk7231n/hardware.h"
#endif

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
        bool attempted = false;
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

    /* WiFi is gone, close the socket now instead of waiting for the keepalive to expire */
    void drop() {
        _state.isConnected = false;
        _wifiClient.stop();
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
        /* connect() blocks the loop, keep every wait short on a local broker */
        _wifiClient.setTimeout(2000);
        _client.setSocketTimeout(2);
        _client.setKeepAlive(60);
    }

    /* busy: skip reconnect attempts, connect() blocks for a couple of seconds */
    void update(bool busy) {

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

            if (busy) return;
            if (_state.attempted && now - _state.lastTime < _state.reconnectInterval) return;

            /* PubSubClient sends the will message with strlen(), so it needs the terminator */
            static const char offlineMsg[] = {(char) 0xFF, '\0'};

            _state.attempted = true;
            _state.lastTime = now;
            _state.reconnectInterval = min(_state.reconnectInterval * 2, (uint32_t) RECONNECT_INTERVAL_MAX);
            _wifiClient.stop();

            _client.connect(
                Settings::config.deviceID,
                Settings::config.mqttUser,
                Settings::config.mqttPass,

                topics.state, 1, false,
                offlineMsg
            );

        } else {
            _state.isConnected = true;
            _state.lastTime = now;
            _state.reconnectInterval = RECONNECT_INTERVAL_MIN;

            if (_state.firstConnect) {
                uint8_t reason = Hardware::resetReason();
                _publishLog(LOG_BOOT, &reason, 1);
            } else _publishLog(LOG_MQTT_CONNECTED);
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
