#include <ESP8266WiFi.h>
#include <ESP8266httpUpdate.h>

#include "ota.h"
#include "settings.h"
#include "leds.h"
#include "hardware/board.h"

namespace OTA {

    void start(const uint8_t* version) {

        Leds::off();
        
        /* Building firmware direction */
        char url[100];
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
