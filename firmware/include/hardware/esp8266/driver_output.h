#ifndef DRIVER_OUTPUT_H
#define DRIVER_OUTPUT_H

#include <Arduino.h>

template <uint8_t _pin>

class OutputPin {
  public:
    static void setup() {pinMode(_pin, OUTPUT); off();}
    static inline void on() {digitalWrite(_pin, HIGH);}
    static inline void off() {digitalWrite(_pin, LOW);}
    static inline void deactivate() {pinMode(_pin, INPUT);}
};

#endif // DRIVER_OUTPUT_H
