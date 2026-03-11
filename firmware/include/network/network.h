#ifndef NETWORK_H
#define NETWORK_H

#include "settings.h"
#include "wifi.h"
#include "mqtt.h"

namespace Network {

    void inline setup() {
        Wifi::setup();
        Mqtt::setup();
    }

    void inline update() {
        Wifi::update();
        Mqtt::update();
    }
}

#endif // NETWORK_H