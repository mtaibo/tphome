#include "actions.h"
#include "config.h"
#include "pins.h"

void handleButtonAction(int pin, unsigned long duration) {
    if (duration == 0) return;

    if (pin == BTN_TOP) {

        if (duration < config.short_pulse) {
            blindUp();
        }

    } else if (pin == BTN_MID) {

        blindStop();

        if (duration > config.long_pulse) {
            for (int i=0; i<10; i++) {
                digitalWrite(LED_GREEN, HIGH);
                delay(1000);
                digitalWrite(LED_GREEN, LOW);
                delay(1000);
            }
        }

    } else if (pin == BTN_BOTTOM) {

        if (duration < config.short_pulse) {
            blindDown();
        }
    }
}

void blindUp() {
    digitalWrite(LED_TOP, HIGH);
    digitalWrite(RELAY_UP, HIGH);
    delay(config.up_time);
    digitalWrite(LED_TOP, LOW);
    digitalWrite(RELAY_UP, LOW);
}

void blindStop() {

    digitalWrite(LED_TOP, LOW);
    digitalWrite(LED_BOTTOM, LOW);

    digitalWrite(RELAY_UP, LOW);
    digitalWrite(RELAY_DOWN, LOW);

    digitalWrite(LED_MID, HIGH);
    delay(2000);
    digitalWrite(LED_MID, LOW);
}

void blindDown() {
    digitalWrite(LED_BOTTOM, HIGH);
    digitalWrite(RELAY_DOWN, HIGH);
    delay(config.down_time);
    digitalWrite(LED_BOTTOM, LOW);
    digitalWrite(RELAY_DOWN, LOW);
}