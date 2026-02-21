# 🏠 TPHome Switches

**TPHome Switches** is a comprehensive firmware collection designed to take full control of commercial smart switches. This project focuses on replacing restrictive stock firmwares with a unified, MQTT-based solution for home automation.

This repository includes custom logic for specific hardware brands like **Matismo** blinds and **BSeed** lighting, ensuring each device operates with its maximum potential.

---

### 📑 Supported Devices & Hardware

#### 🪟 Blind Controllers (Matismo & others)
* [**TYWE3S (ESP8266)**](#tywe3s-esp8266) - Old Matismo standard for WiFi blinds chips. **[Current Stable]**
* [**Beken BK7231**](#beken-series) - New Matismo hardware. *(Upcoming support)*

#### 💡 Light Switches (BSeed & others)
* [**Realtek RTL8710**](#realtek-rtl-series) - Common in BSeed WiFi switches. *(In progress)*
* [**ESP32-WROOM**](#esp32-wroom) - Custom retrofitted switches. *(In progress)*

---

## 🔧 TYWE3S (ESP8266)

The **TYWE3S** is a low-power 32-bit CPU commonly found in Tuya devices. It details the pinout configuration and logic for the chip when used for blind motor control.

This documentation details the pinout configuration and logic for the TYWE3S chip when used for blind motor control, including LED indicators, button behaviors, and relay assignments.

**Quick Navigation:**
[📍 Pin Distribution](#pin-distribution) | [⚙️ Component Logic](#component-logic) | [🖱️ Input Actions](#input-actions) | [📡 MQTT Interface](#mqtt-commands)

### Pin Distribution

The following table maps the available pins to their respective hardware.


> **Note:** Pins 1 and 3 are reserved for Serial Communication (TX/RX). Avoid using them for other tasks if you need to see the Serial Monitor. Also pins 6 to 11 are dedicated to internal flash memory; using them as general GPIO pins may cause the chip to crash.

| Pins | 0 | 1 | 2 | 3 | 5 | 12 | 13 | 14 | 15 | 16 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LEDs** | Green | | Low | | | | | Mid | | Top |
| **Buttons**| | | | Mid | Low | Top | | | | |
| **Relays** | | | | | | | **L1** | | **L3** | |
| **TX/RX** | | **X** | | **X** | | | | | | |

### Component Logic

#### 💡 LEDs
* **Green LED (Pin 0):** Simple network state indicator.
    * `HIGH`: LED On (Green).
    * `LOW`: LED Off.
* **Status LEDs (Mid/Top/Low):** These are dual-color LEDs.
    * `HIGH`: **Red** (Busy/Error).
    * `LOW`: **Blue** (Idle/OK).

#### 🖱️ Buttons (Active Low)
All buttons follow standard pull-up logic:
* **Pressed:** `LOW` (0).
* **Released:** `HIGH` (1).

#### 🔌 Relays (Blind Motor Control)
Relays control the current flow to the motor.
* `HIGH`: Relay Active (Current ON).
* `LOW`: Relay Inactive (Current OFF).
* **Assignments:** Pin 13 is mapped to **L1** and Pin 15 to **L3**.

---

### Input Actions

Button behavior is determined by the duration of the press.

| Button | Short Press | Medium Press (3s) | Long Press (10s) |
| :--- | :--- | :--- | :--- |
| **Top** | `blind_up` | *(Unassigned)* | `access_point` |
| **Middle** | `blind_stop` | `save_config` | `reset_memory` |
| **Bottom** | `blind_down` | *(Unassigned)* | `network_setup` |

---

### MQTT Commands

Control and monitor the device using the following topics:

| Topic | Payload | Action |
| :--- | :--- | :--- |
| `device/blinds/set` | `UP`, `DOWN`, `STOP` | Controls the motor state |
| `device/blinds/status` | `string` | Reports current state |

[↑ Back to Top](#smart-blinds-firmware-collection)

---

## 🔧 Realtek RTL Series
*(Documentation in progress...)*

[↑ Back to Top](#smart-blinds-firmware-collection)

---

## 🔧 ESP32 WROOM
*(Documentation in progress...)*

[↑ Back to Top](#smart-blinds-firmware-collection)
