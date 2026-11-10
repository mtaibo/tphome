#ifndef MQTT_H
#define MQTT_H

#include <stdint.h>
#include "defaults.h"

namespace Mqtt {

    using Callback = void (*)(char* topic, uint8_t* payload, unsigned int length);

    struct Topics {
        char def[Sizes::MQTT];
        char global[Sizes::MQTT];
        char cmd[Sizes::MQTT];
        char admin[Sizes::MQTT];
        char state[Sizes::MQTT];
        char log[Sizes::MQTT];
    };

    extern Topics topics;

    void setup();
    void setCallback(Callback callback);
    bool isConnected();

    /* WiFi is gone, close the socket now instead of waiting for the keepalive to expire */
    void drop();

    /* busy: skip reconnect attempts, connect() blocks for a couple of seconds */
    void update(bool busy);

    bool publish(const char* topic, const uint8_t* payload, unsigned int length);
}

#endif // MQTT_H
