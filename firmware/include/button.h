#ifndef BUTTON
#define BUTTON

#include <Arduino.h>

class Button {
private:
    int _pin;
    unsigned long _startTime;
    bool _isPressed;
    
public:
    Button(int pin);
    void begin();
    
    // Devuelve la duración de la pulsación solo en el momento de soltar
    unsigned long checkPulse(); 
};

#endif