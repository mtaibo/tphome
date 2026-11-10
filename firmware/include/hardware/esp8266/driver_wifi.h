#ifndef DRIVER_WIFI_H
#define DRIVER_WIFI_H

#include <stdint.h>

namespace Hardware::Wifi {

    void setup(const char* hostname);
    void begin(const char* ssid, const char* pass);
    void disconnect();

    /* Turn the radio fully off, used while waiting between reconnect attempts */
    void sleep();
    void wake(const char* hostname);

    bool isConnected();
    void macAddress(uint8_t* mac); // 6 bytes
}

#endif // DRIVER_WIFI_H
