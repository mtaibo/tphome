#if defined(DEVICE_HARDWARE_ESP8266)

#include <ESP8266WiFi.h>
#include "hardware/esp8266/driver_wifi.h"

namespace Hardware::Wifi {

    /* 16 dBm was the last value without drops, the radio barely transmits
     * so a lower value saves almost nothing and costs range */
    static constexpr float TX_POWER = 16.0;

    /* Station mode settings, they have to be applied again after the radio wakes up */
    static void configure(const char* hostname) {

        /* Set wifi on station mode to just connect and don't create any AP */
        WiFi.mode(WIFI_STA);

        /* Set a hostname to identify easily the device IP and MAC address on router via its deviceID */
        WiFi.hostname(hostname);

        /* Let the radio sleep between beacons and adjust the power the antenna transmits */
        WiFi.setSleepMode(WIFI_MODEM_SLEEP);
        WiFi.setOutputPower(TX_POWER);
    }

    void setup(const char* hostname) {

        /* Prevent the chip from saving wifi credentials on flash memory */
        WiFi.persistent(false);

        /* Prevent the chip from reconnecting on its own */
        WiFi.setAutoConnect(false);
        WiFi.setAutoReconnect(false);

        configure(hostname);
    }

    void begin(const char* ssid, const char* pass) {
        WiFi.begin(ssid, pass);
    }

    void disconnect() {
        WiFi.disconnect(false);
    }

    void sleep() {
        WiFi.disconnect(true);
        WiFi.mode(WIFI_OFF);
        WiFi.forceSleepBegin();
        delay(1); // Needed for the modem to actually go to sleep
    }

    void wake(const char* hostname) {
        WiFi.forceSleepWake();
        delay(1);
        configure(hostname);
    }

    bool isConnected() {
        return WiFi.status() == WL_CONNECTED;
    }

    void macAddress(uint8_t* mac) {
        WiFi.macAddress(mac);
    }
}

#endif // DEVICE_HARDWARE_ESP8266
