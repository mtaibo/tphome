#include "button.h"

Button::Button(int pin) : _pin(pin), _startTime(0), _isPressed(false) {}

void Button::begin() {
    pinMode(_pin, INPUT_PULLUP);
}

unsigned long Button::checkPulse() {
    bool currentState = (digitalRead(_pin) == LOW); // LOW significa pulsado
    
    // Flanco de bajada: El botón se acaba de pulsar
    if (currentState && !_isPressed) {
        _startTime = millis();
        _isPressed = true;
        return 0;
    }
    
    // Flanco de subida: El botón se acaba de soltar
    if (!currentState && _isPressed) {
        unsigned long duration = millis() - _startTime;
        _isPressed = false;
        return duration; // Retornamos cuánto tiempo estuvo pulsado
    }
    
    return 0; // No ha pasado nada relevante
}