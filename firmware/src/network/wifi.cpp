#include <Arduino.h>

#include "wifi.h"
#include "settings.h"
#include "hardware/board.h"

namespace Wifi {

    static constexpr uint32_t ATTEMPT_WINDOW = 15000; // Time each attempt gets to join the network
    static constexpr uint32_t RETRY_MIN      =  5000; // Radio off time after the first failed attempt
    static constexpr uint32_t RETRY_MAX      = 60000; // Longest radio off time between attempts

    /* The radio is only on while connected or trying to connect, a device that
     * can't reach the router spends most of the time with the radio off */
    enum class Phase : uint8_t { Online, Joining, Asleep };

    struct State {
        Phase phase = Phase::Joining;
        uint32_t lastTime = 0;
        uint32_t retryInterval = RETRY_MIN;
    };

    static State _state;

    bool isConnected() {
        return _state.phase == Phase::Online;
    }

    static void _attempt(uint32_t now) {
        Hardware::Wifi::begin(Settings::config.wifiSSID, Settings::config.wifiPass);
        _state.phase = Phase::Joining;
        _state.lastTime = now;
    }

    void setup() {
        Hardware::Wifi::setup(Settings::config.deviceID);
        _attempt(millis());
    }

    void update() {

        uint32_t now = millis();
        bool linked = Hardware::Wifi::isConnected();

        switch (_state.phase) {

            case Phase::Online: // Connection dropped, try again right away
                if (!linked) {
                    _state.retryInterval = RETRY_MIN;
                    Hardware::Wifi::disconnect();
                    _attempt(now);
                } break;

            case Phase::Joining:
                if (linked) {
                    _state.phase = Phase::Online;
                    _state.retryInterval = RETRY_MIN;
                }

                /* Attempt failed, turn the radio off until the next one */
                else if (now - _state.lastTime >= ATTEMPT_WINDOW) {
                    Hardware::Wifi::sleep();
                    _state.phase = Phase::Asleep;
                    _state.lastTime = now;
                } break;

            case Phase::Asleep:
                if (now - _state.lastTime >= _state.retryInterval) {
                    _state.retryInterval = min(_state.retryInterval * 2, RETRY_MAX);
                    Hardware::Wifi::wake(Settings::config.deviceID);
                    _attempt(now);
                } break;
        }
    }
}
