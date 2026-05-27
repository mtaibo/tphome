#ifndef NETWORK_H
#define NETWORK_H

#include "settings.h"
#include "commands.h"
#include "wifi.h"
#include "mqtt.h"
#include "mode.h"

namespace Network {

    void inline setup() {
        Wifi::setup();
        Mqtt::setup();
        Mqtt::setCallback(Commands::callback);
        Mode::set(Mode::NORMAL);
    }

    bool inline isConnected() {
        return (Wifi::isConnected() && Mqtt::isConnected());
    }

    void inline update() {
        Wifi::update();
        if (Wifi::isConnected()) Mqtt::update();

        if (Mode::is(Mode::Value::NORMAL)) {
            if (Wifi::isConnected() && Mqtt::isConnected()) Leds::set(Pins::LED_GREEN, Leds::OFF);
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