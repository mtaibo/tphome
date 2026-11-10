#include "mode.h"
#include "leds.h"

namespace Mode {

    static Value current = NORMAL;

    bool is(Value mode) { return current == mode; }

    void set(Value mode) {

        if (mode == current) return;

        if (mode == NORMAL) {
            Leds::set(Pins::LED_TOP, Leds::OFF);
            Leds::set(Pins::LED_MID, Leds::OFF);
            Leds::set(Pins::LED_BTM, Leds::OFF);
            Leds::set(Pins::LED_GREEN, Leds::OFF);
        }

        else if (mode == CONNECTION) {
            Leds::set(Pins::LED_TOP, Leds::BLINK);
            Leds::set(Pins::LED_MID, Leds::ON);
            Leds::set(Pins::LED_BTM, Leds::ON);
            Leds::set(Pins::LED_GREEN, Leds::OFF);
        }

        current = mode;
    }
}
