#ifndef LEDS_H
#define LEDS_H

#include <stdint.h>
#include "hardware/board.h" // Pins used by every caller

namespace Leds {

    /* Enums to simplify code */
    enum Mode { OFF, ON, BLINK, BLUE = OFF, RED = ON };
    enum Speed { SLOW = 100, MEDIUM = 50, FAST = 25 }; // 1s, 0.5s, 0.25s

    /* duration: centiseconds until the led turns off, 0 keeps it */
    void set(uint8_t pin, Mode mode, Speed speed = MEDIUM, uint16_t blinks = 0, uint16_t duration = 0);
    void off(); // Turn every led and the backlight off
    void update();
}

#endif // LEDS_H
