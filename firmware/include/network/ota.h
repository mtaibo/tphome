#ifndef OTA_H
#define OTA_H

#include <ESP8266httpUpdate.h>
#include "settings.h"
#include "wifi.h"
#include "leds.h"

namespace OTA {

    char url[100];

    /* version: the 3 bytes of the firmware being installed, only stored if the update succeeds */
    void start(const uint8_t* version) {

        Leds::off();
        
        /* Building firmware direction */
        snprintf(url, sizeof(url), "http://%s/firmware", Settings::config.mqttIP);

        WiFiClient client;
        ESPhttpUpdate.rebootOnUpdate(false);

        if (ESPhttpUpdate.update(client, url) == HTTP_UPDATE_OK) {
            memcpy(Settings::config.version, version, 3);
            Settings::save();
            Settings::reboot();
        }

        Hardware::enableLight(); // Update failed, keep running the current firmware
    }
}

#endif // OTA_H