#ifndef NETWORK_H
#define NETWORK_H

#include "settings.h"
#include "commands.h"
#include "wifi.h"
#include "mqtt.h"
#include "mode.h"

namespace Network {

    /* Reboot after this long without WiFi + MQTT, the ESP8266 WiFi stack
     * sometimes gets stuck and only a restart brings it back */
    static constexpr uint32_t OFFLINE_REBOOT = 15UL * 60UL * 1000UL; // 15 min

    inline uint32_t _lastOnline = 0;

    void inline setup() {
        Wifi::setup();
        Mqtt::setup();
        Mqtt::setCallback(Commands::callback);
        Mode::set(Mode::NORMAL);
    }

    bool inline isConnected() {
        return (Wifi::isConnected() && Mqtt::isConnected());
    }

    /* busy: the device is doing something that must not be interrupted (blind moving) */
    void inline update(bool busy) {

        bool hadWifi = Wifi::isConnected();
        Wifi::update();

        if (Wifi::isConnected()) {
            Mqtt::update(busy);
            if (Mqtt::isConnected()) Commands::update();
        }
        else if (hadWifi) Mqtt::drop();

        uint32_t now = millis();
        if (isConnected()) _lastOnline = now;
        else if (!busy && Mode::is(Mode::Value::NORMAL) && now - _lastOnline >= OFFLINE_REBOOT) Settings::reboot();

        if (Mode::is(Mode::Value::NORMAL)) {
            if (isConnected()) Leds::set(Pins::LED_GREEN, Leds::OFF);
            else Leds::set(Pins::LED_GREEN, Leds::ON);
        }

        if (Mode::is(Mode::Value::CONNECTION)) {
            if (Wifi::isConnected()) Leds::set(Pins::LED_MID, Leds::BLUE);
            else Leds::set(Pins::LED_MID, Leds::RED);

            if (Mqtt::isConnected()) Leds::set(Pins::LED_BTM, Leds::BLUE);
            else Leds::set(Pins::LED_BTM, Leds::RED);
        }
    }
}

#endif // NETWORK_H
