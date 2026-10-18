<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/banner/dark.svg">
  <img src="images/banner/light.svg" alt="TPHome" width="100%" />
</picture>

<br/>
<br/>

**Home automation, from the chip to the browser.**

<br/>

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Hardware](https://img.shields.io/badge/hardware-ESP8266-lightgrey)
![Made with](https://img.shields.io/badge/made%20with-C%2B%2B%20%7C%20Python%20%7C%20Vue-blue)

</div>

---

TPHome is the home automation system that runs my house. I replaced the factory firmware on commercial blind controllers with my own, and built every layer on top of it: C++ firmware on the chips, a Python backend on a Raspberry Pi, and a Vue control panel with a live floor plan of the house. It's one of the modules of my personal cloud, [tpcloud](https://github.com/mtaibo/tpcloud), and it's also a tab in my native app, [tpapp](https://github.com/mtaibo/tpapp).

## Why I built it

I got tired of needing a different app, account and cloud for every brand of device in the house. They barely talk to each other, they stop working when the internet goes down, and none of them let me change how a device behaves. So I opened the switches, flashed my own firmware, and wrote the rest.

- **Local first** — the devices only talk to a broker on my LAN, with no vendor cloud involved
- **No black boxes** — every byte on the wire is my own binary protocol
- **My rules** — a blind stops at 20% on the first press down and only closes fully on the second
- **One screen** — every device in the house on a single floor plan, on the web or on my phone

## The system

<table>
<tr>
<td width="33%" valign="top">

### 🔌 [`firmware`](firmware/)
Custom firmware flashed over the factory one on commercial switches. Motor state machine with position tracking, triple-button input, LED feedback, binary MQTT protocol, WiFi provisioning through an access point, and OTA updates.

**C++17 · PlatformIO · Arduino**

</td>
<td width="33%" valign="top">

### ⚙️ [`api`](api/)
Backend on the Raspberry Pi next to a Mosquitto broker. Bridges REST commands to MQTT, parses device state, persists it, pushes live events over WebSocket, discovers and provisions new devices, and serves firmware for OTA.

**Python · FastAPI · Mosquitto · SQLite**

</td>
<td width="33%" valign="top">

### 🗺️ [`frontend`](frontend/)
Control panel with an interactive SVG floor plan of the house. Open a blind to slide it to any position, and manage devices, map placement, firmware and logs from the settings.

**Vue 3 · Pinia · Tailwind CSS · Nginx**

</td>
</tr>
</table>

## Architecture

```
          browser                      tpapp (iOS · macOS)
             │                                 │
             └───────────────┬─────────────────┘
                             │ HTTPS · WSS
┌────────────────────────────▼─────────────────────────────┐
│      tpcloud gateway · Caddy + Cloudflare Tunnel          │
│        tphome.migueltaibo.com · protected by auth         │
└───────────────┬──────────────────────────┬───────────────┘
                │                          │
┌───────────────▼────────────┐ ┌───────────▼───────────────┐
│         frontend/          │ │           api/             │
│   Vue 3 · Nginx container  │ │  FastAPI · SQLite · OTA    │
└────────────────────────────┘ └───────────┬───────────────┘
                                           │ MQTT (binary)
                               ┌───────────▼───────────────┐
                               │   Mosquitto broker (LAN)   │
                               └───────────┬───────────────┘
                                           │ WiFi
                               ┌───────────▼───────────────┐
                               │        firmware/           │
                               │  blind switches · ESP8266  │
                               └───────────────────────────┘
```

Everything above the broker runs in Docker on the Raspberry Pi. TPHome doesn't have its own reverse proxy: the [tpcloud](https://github.com/mtaibo/tpcloud) gateway reaches its containers over a shared Docker network and puts them behind the same login as the rest of my services.

## How it works

Pressing "down" on a blind, from the floor plan:

```
Frontend sends POST /commands/B0101/down
        │
        ▼
API publishes 0xC1 to tp/B0101/c
        │
        ▼
Switch receives the byte, closes the relay and starts the motor
        │
        ▼
Switch publishes a 2-byte state (position + motor state) every second while moving
        │
        ▼
API parses it, saves it to SQLite and pushes a WebSocket event
        │
        ▼
Floor plan animates the blind in real time
```

### The protocol

Every message on the wire is binary, and the first byte says what it is. Each device has an ID like `B0102` (blind, zone 01, device 02) and its own set of topics:

| Topic | Direction | Purpose |
|---|---|---|
| `tp/{ID}/c` | to device | Control: `0x00`–`0x64` sets a position, `0xC0` up, `0xC1` down, `0xC2` stop, `0xC3` ping, `0xC4` state |
| `tp/{ID}/a` | to device | Admin: OTA, reboot, factory reset, device info, position override, preferences |
| `tp/{ID}/s` | from device | State: 2 bytes, position (0–100) and motor state |
| `tp/a/c` | to all | Broadcast: every device answers with its ID, after a random delay so they don't collide |

If a switch drops off the network, the broker publishes its last will (`0xFF`) on its state topic and the API marks it offline straight away.

### Adding a new device

```
Fresh switch boots with no ID
        │
        ▼
Derives a temporary ID from its MAC and announces itself on def/{MAC4}/s
        │
        ▼
Shows up as "pending" in the frontend's device settings
        │
        ▼
I assign it a zone and number, the API sends the ID to def/{MAC4}/a
        │
        ▼
Switch saves the ID to flash, reboots and starts listening on tp/{ID}/*
```

If a switch can't reach the WiFi or the broker, a short press on the middle button in connection mode turns it into an access point named after its ID. Connecting to it and opening `http://192.168.4.1` shows a form to enter new WiFi and MQTT credentials.

### Inside the firmware

The firmware is split into four layers, each one only depending on the ones below it, so porting to a new chip only means rewriting `hardware/`:

| Layer | Responsibility |
|---|---|
| `logic/` | Device behaviour: blind motor, buttons, LEDs, button-to-action mapping |
| `network/` | WiFi, MQTT, OTA and access-point provisioning |
| `settings/` | Device ID, credentials and preferences persisted in flash |
| `hardware/` | Pin drivers and chip-specific code |

A few rules I kept to, since the ESP8266 only has 80KB of RAM:

- **Non-blocking loop** — no `delay()` anywhere in the main path, everything runs on `millis()` timers
- **No dynamic allocation** — no `new`, `malloc` or `std::vector`, all state lives in fixed structs
- **Packed structs** — anything written to flash or sent over MQTT has a predictable byte layout

The blind's position is tracked from time, not from a sensor: each direction has a calibrated travel time, and the motor state machine (`IDLE → MOVING → STOPPING`, with a `WAITING` pause before reversing direction) accumulates the position every loop tick. The relays are interlocked so both directions can never be on at once, and the wiring can be inverted from the preferences without reflashing.

## Hardware

| Device | Chip | Status |
|---|---|---|
| Matismo WIP100 blind controller | TYWE3S · ESP8266 | ✅ Supported |
| BK7231N-based switches | CB3S / T34 · BK7231N | 🚧 In development |

Support for BK7231N chips (newer revisions of the same blind controller, and light switches) is in progress through LibreTiny. The build environments are there, but the drivers aren't finished yet.

## Tech stack

| Layer | Technology |
|---|---|
| **Firmware** | C++17 · Arduino ESP8266 Core · PlatformIO · PubSubClient |
| **API** | FastAPI · Python · SQLModel · SQLite |
| **Messaging** | Mosquitto (MQTT) · custom binary protocol · WebSocket |
| **Frontend** | Vue 3 · Composition API · Pinia · Tailwind CSS 4 |
| **Hosting** | Docker Compose · Nginx · Raspberry Pi · behind the tpcloud gateway |

## How to run

```bash
git clone https://github.com/mtaibo/tphome
cd tphome
cp .env.example .env    # WiFi, MQTT and database values, shared by the API and the firmware
docker compose up --build -d
```

This starts the API, the MQTT broker and the frontend. To reach them from outside the LAN, start [tpcloud](https://github.com/mtaibo/tpcloud) on the same host, since its gateway joins the `tphome-network`.

### Flashing a switch

The firmware runs on the physical switches, not in Docker. The first flash needs a USB-TTL adapter at **3.3V** (never 5V) wired to the chip's TX, RX, GND and VCC, with GPIO 0 pulled to GND on power-up to enter the bootloader.

```bash
cd firmware
pip install -r requirements.txt   # PlatformIO and esptool
./build.sh                        # build, generating the credentials header from .env
./build.sh flash                  # build and flash over serial
```

After that, updates go over the air: upload the binary in the frontend's firmware manager, activate it, and trigger the OTA from each device's settings. The switch downloads it from the Pi and reboots into the new version.
