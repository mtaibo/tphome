# TYWE3S Controller Reference

This documentation details the pinout configuration and logic for the **TYWE3S** chip when used for blind motor control, including LED indicators, button behaviors, and relay assignments.

## Pin Distribution

The following table maps the available pins to their respective functions. 

> **Note:** Pins 1 and 3 are reserved for Serial Communication (TX/RX). Avoid using them for other tasks if you need to use the Serial Monitor.

| Function | 0 | 1 | 2 | 3 | 5 | 12 | 13 | 14 | 15 | 16 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LEDs** | Green | | Low | | | | | Mid | | Top |
| **Buttons**| | | | Mid | Low | Top | | | | |
| **Relays** | | | | | | | L1 | | L3 | |
| **TX/RX** | | **X** | | **X** | | | | | | |

---

Prueba

## Component Logic

### LEDs
* **Green LED (Pin 0):** Simple state indicator.
    * `HIGH`: LED On (Green).
    * `LOW`: LED Off.
* **Status LEDs (Mid/Top/Low):** These are dual-color LEDs.
    * `HIGH`: Red.
    * `LOW`: Blue.

### Buttons (Active Low)
All buttons follow standard pull-up logic:
* **Pressed:** `LOW` (0).
* **Released:** `HIGH` (1).

### Relays (Blind Motor Control)
Relays control the current flow to the motor.
* `HIGH`: Relay Active (Current ON).
* `LOW`: Relay Inactive (Current OFF).
* **Assignments:** Pin 13 is mapped to **L1** and Pin 15 to **L3**.

### Special Purpose Pins
* **TX/RX (Pins 1 & 3):** Reserved for Serial communication. For reliable data transmission, ensure these pins are not held in a specific state by external hardware during flashing or debugging.
* **Flash Memory (Pins 6-11):** These pins are dedicated to the internal flash memory. **Do not** attempt to use them for GPIO tasks, as this will cause the chip to crash.

---

## Input Actions

Button behavior is determined by the duration of the press.

### **Top Button**
* **Short Press:** `blind_up`
* **Medium Press:** *(Unassigned)*
* **Long Press:** `access_point` (Enter AP Mode)

### **Middle Button**
* **Short Press:** `blind_stop`
* **Medium Press:** `save_config`
* **Long Press:** `reset_memory` (Factory Reset)

### **Bottom Button**
* **Short Press:** `blind_down`
* **Medium Press:** *(Unassigned)*
* **Long Press:** `network_setup()`

---

## MQTT Commands

| Topic | Payload | Action |
| :--- | :--- | :--- |
| `device/blinds/set` | `UP`, `DOWN`, `STOP` | Controls the motor state |
| `device/blinds/status` | `string` | Reports curren
