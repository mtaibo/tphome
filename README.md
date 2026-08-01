<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/banner/dark.svg">
  <img src="images/banner/light.svg" alt="TPHome" width="100%" />
</picture>

<br/>
<br/>

**Home automation system — from the chip to the browser.**

<br/>

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made with](https://img.shields.io/badge/made%20with-C%2B%2B%20%7C%20Python%20%7C%20Vue-lightgrey)

</div>

---

I'm a first-year computer engineering student and this is a home automation system I built from scratch — every layer of it. The C++ firmware runs on the chips inside commercial switches, the Python backend runs on a Raspberry Pi, and the Vue frontend serves as the single control panel for every device in the house.

## How it started

I got tired of needing different apps to control my house. Every brand has its own cloud and its own account, they hardly talk to each other, and if you want a specific device behaviour — like closing a blind to 20% on first press instead of fully closed — there was no way to do it. So I built my own system, one that lives entirely on my local network.

Everything here is:
- **Local** — no cloud needed, everything runs on my home network
- **Understandable** — no black boxes, I designed and built each piece, all fully documented
- **Customizable** — for example, the blind stops at 20% on first press instead of 0%
- **Unified** — one screen shows every device in the house

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  frontend/                          │
│           Vue 3 frontend · Tailwind CSS             │
│         Hosted via Docker on Raspberry Pi           │
└────────────────────────┬────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────┐
│                     api/                            │
│    FastAPI backend · MQTT orchestration · SQLite    │
│          Hosted via Docker on Raspberry Pi          │
└────────────────────────┬────────────────────────────┘
                         │ MQTT (binary protocol)
┌────────────────────────▼────────────────────────────┐
│                  firmware/                          │
│   C++ firmware for ESP8266 / BK7231N smart switches │
│           Flashing over factory firmware            │
└─────────────────────────────────────────────────────┘
```

## Modules

<table>
<tr>
<td width="33%">

### [firmware/](firmware/)

Custom C++ firmware for proprietary chips, built with PlatformIO.

Replaces factory software on commercial blind controllers and light switches with a fully local MQTT-based control layer.

**C++ · PlatformIO · Arduino**

</td>
<td width="33%">

### [api/](api/)

FastAPI backend running on a Raspberry Pi alongside a Mosquitto MQTT broker, managed with Docker.

Handles device management, state persistence, OTA firmware serving and real-time WebSocket events.

**Python · FastAPI · Docker · SQLite**

</td>
<td width="33%">

### [frontend/](frontend/)

Vue 3 frontend served by Nginx behind a Caddy reverse proxy, also hosted on the Raspberry Pi.

Renders an interactive SVG floor plan where you can see and control every light and blind in real time.

**Vue 3 · Tailwind CSS · Nginx**

</td>
</tr>
</table>

## How it works

A typical interaction — pressing "down" on a blind from the frontend:

```
Frontend sends POST /commands/B0101/down
        │
        ▼
API publishes 0xC1 to tp/B0101/c via MQTT
        │
        ▼
ESP8266 chip receives command, activates relay, starts motor
        │
        ▼
Chip publishes 2-byte state (position + motor_state) every second
        │
        ▼
API parses binary payload, updates SQLite, pushes WebSocket event
        │
        ▼
Frontend updates position in real time
```

No cloud involved at any point. The entire system works on the local network.

## Tech stack

| Layer | Technology |
|---|---|
| **Firmware language** | C++17 |
| **Firmware framework** | Arduino (ESP8266 Core / LibreTiny) |
| **Firmware build** | PlatformIO |
| **API framework** | FastAPI · Python 3.11 |
| **API database** | SQLite via SQLModel |
| **API broker** | Mosquitto (MQTT) |
| **Frontend framework** | Vue 3 · Composition API |
| **Frontend styling** | Tailwind CSS 4 |
| **Frontend state** | Pinia |
| **Hosting** | Docker + Nginx + Caddy · Raspberry Pi |

## How to run

```bash
git clone https://github.com/mtaibo/tphome
cd tphome
cp .env.example .env   # fill in WiFi, MQTT and API values
docker compose up --build -d
```

That's it. Caddy, Nginx, the API, and the MQTT broker all start together.

**Firmware** is flashed separately — it runs on the physical chips, not in Docker:

```bash
cd firmware
./build.sh              # compile blind_esp8266 (default)
./build.sh all          # compile all environments
./build.sh flash        # compile and flash
```

See [firmware/README.md](firmware/README.md) for wiring and first-flash instructions.

## License

MIT — see [LICENSE](LICENSE)
