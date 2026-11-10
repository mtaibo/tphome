#include <Arduino.h>

#include "settings.h"
#include "network.h"
#include "actions.h"
#include "leds.h"
#include "buttons.h"
#include "hardware/board.h"

#if defined(DEVICE_TYPE_BLIND)
    #include "blinds.h"
#elif defined(DEVICE_TYPE_LIGHT)
    #include "lights.h"
#endif

void setup() {
    Settings::setup();
    Hardware::setup();
    Network::setup();
}

void loop() {

    #if defined(DEVICE_TYPE_BLIND)
        const bool busy = !Blinds::isIdle();
    #else
        const bool busy = false;
    #endif

    Network::update(busy);

    /* Check inputs */
    Actions::check();

    /* Update interface */
    Leds::update();
    Buttons::update();

    /* Update device functions */
    #if defined(DEVICE_TYPE_BLIND)
        Blinds::update();
    #elif defined(DEVICE_TYPE_LIGHT)
        Lights::update();
    #endif

    /* Give the CPU idle time so the WiFi modem can sleep between beacons,
     * 10 ms is the resolution every timer in the firmware already works with */
    delay(10);
}
