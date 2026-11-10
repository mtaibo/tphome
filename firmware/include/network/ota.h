#ifndef OTA_H
#define OTA_H

#include <stdint.h>

namespace OTA {
    /* version: the 3 bytes of the firmware being installed, only stored if the update succeeds */
    void start(const uint8_t* version);
}

#endif // OTA_H
