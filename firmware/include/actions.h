#ifndef ACTIONS
#define ACTIONS

#include <Arduino.h>

// Secondary actions
void startBlink(int led);

// Main button actions
void blindUp();
void blindDown();
void blindStop();

// Main actions handlers
void handleButtonAction(int pin, unsigned long duration);
void updateActions();

#endif