#ifndef COMMANDS_H
#define COMMANDS_H

#include <stdint.h>

namespace Commands {

    void publishState(); // Report blind position and motor state

    /* Sends delayed answers, call it while MQTT is connected */
    void update();

    void callback(char* topic, uint8_t* payload, unsigned int length);
}

#endif // COMMANDS_H
