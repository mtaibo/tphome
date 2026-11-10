#ifndef HARDWARE_H
#define HARDWARE_H

#include "defaults.h"
#include "hardware/esp8266/pinout.h"
#include "hardware/esp8266/driver_input.h"
#include "hardware/esp8266/driver_output.h"
#include "hardware/esp8266/driver_wifi.h"

namespace Hardware { // Hardware for ESP8266

    // --- BUTTONS ---
    using BtnBtm = InputPin<Pins::BTN_BTM, Defaults::LONG_PULSE>;
    using BtnMid = InputPin<Pins::BTN_MID, Defaults::LONG_PULSE>;
    using BtnTop = InputPin<Pins::BTN_TOP, Defaults::LONG_PULSE>;

    // --- LEDS ---
    using LedConfig = OutputPin<Pins::LED_CONFIG>;
    using LedGreen  = OutputPin<Pins::LED_GREEN>;
    using LedBtm    = OutputPin<Pins::LED_BTM>;
    using LedMid    = OutputPin<Pins::LED_MID>;
    using LedTop    = OutputPin<Pins::LED_TOP>;

    // --- RELAYS ---
    using RelayUp   = OutputPin<Pins::RELAY_UP>;
    using RelayDown = OutputPin<Pins::RELAY_DOWN>;

    inline void relaysOff() {RelayUp::off(); RelayDown::off();}

    // --- LIGHT CONTROL ---
    inline void enableLight() {LedConfig::setup(); LedConfig::on();}
    inline void disableLight() {LedConfig::off();}

    // --- LED CONTROL ---
    void setState(uint8_t pin, bool state);

    // --- SYSTEM ---
    /* Why the chip last started: 0 power on, 1 hw watchdog, 2 exception,
     * 3 sw watchdog, 4 software restart, 5 deep sleep wake, 6 reset pin */
    uint8_t resetReason();

    // --- GLOBAL SETUP ---
    void setup();
}

#endif // HARDWARE_H
