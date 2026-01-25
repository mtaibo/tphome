#include <Arduino.h>

#include <buttons.h>
#include <actions.h>
#include <config.h>
#include <pins.h>

Button::Button(int pin) : _pin(pin), _startTime(0), _isPressed(false), _waitingRelease(false){}

void Button::setup() {
    pinMode(_pin, INPUT_PULLUP);
}

unsigned long Button::get_duration() {
    bool isPressedNow = (digitalRead(_pin) == LOW); 

    if (!isPressedNow && (_isPressed || _waitingRelease || _startTime > 0)) {
        unsigned long duration = 0;

        if (!_waitingRelease && _startTime > 0) {
            duration = millis() - _startTime;
        }

        _isPressed = false;
        _waitingRelease = false;
        _startTime = 0;
        
        return duration;
    }

    if (isPressedNow && !_isPressed && !_waitingRelease) {
        _startTime = millis();
        _isPressed = true;
        return 0;
    }

    if (isPressedNow && _isPressed && (millis() - _startTime > config.long_pulse)) {
        _isPressed = false; 
        _waitingRelease = true;  
        return millis() - _startTime;
    }

    return 0; 
}

void Button::check() {
    unsigned long duration = get_duration();
    if (duration > 50) handleButtonAction(_pin, duration);
}

Button buttonTop(BTN_TOP);
Button buttonMid(BTN_MID);
Button buttonBottom(BTN_BOTTOM);