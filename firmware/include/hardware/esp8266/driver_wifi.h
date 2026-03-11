#ifndef DRIVER_WIFI_H
#define DRIVER_WIFI_H

#include <ESP8266WiFi.h>

namespace Hardware::Wifi {

    static void setup(const char* hostname) {

        /* Prevent the chip from reconnecting on its own */
        WiFi.setAutoConnect(false);
        WiFi.setAutoReconnect(false);

        /* Prevent the chip from saving wifi credentials on flash memory */
        WiFi.persistent(false);

        /* Adjust the frequency and the power the wifi antenna transmits */
        WiFi.setSleepMode(WIFI_MODEM_SLEEP);
        WiFi.setOutputPower(18.5);

        /* Set wifi on station mode to just connect and don't create any AP */
        WiFi.mode(WIFI_STA);

        /* Set a hostname to identify easily the device IP and MAC address on router via its deviceID */
        WiFi.hostname(hostname);
    }

    static void disconnect() {
        WiFi.disconnect(true);
    }

    static void begin(const char* ssid, const char* pass) {
        WiFi.begin(ssid, pass);
    }

    static bool isConnected() {
        return WiFi.status() == WL_CONNECTED;
    }
}

#endif