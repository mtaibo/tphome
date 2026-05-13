<div align="center">

<img src="docs/banner.svg" alt="TPHome" width="100%" />

<br/>
<br/>

**A fully local, self-built home automation system — from chip firmware to web frontend.**

<br/>

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made with](https://img.shields.io/badge/made%20with-C%2B%2B%20%7C%20Python%20%7C%20Vue-lightgrey)

</div>

---

I'm a first-year computer engineering student and this is my biggest project so far — a home automation system I built from scratch during my first year at university to learn embedded systems, networking, and full-stack development by solving a real problem I had at home.

Most smart home devices ship locked to vendor clouds. You install an app per brand, none of them talk to each other, and the day the company shuts down their servers your switches stop working. I wanted something different — a system that runs entirely on my local network, that I understood down to every layer, and that I could shape around how I actually use my home. Things like: the blind going to 20% on the first press instead of closing all the way, or a single interface that shows everything at once.

Every layer of the stack — the C++ firmware running inside the switches, the Python backend orchestrating everything, and the Vue frontend you see here — is designed and written by me.

## Architecture

TPHome is split into three independent repositories, each responsible for one layer of the stack:

```
┌─────────────────────────────────────────────────────┐
│                     tphome (this repo)               │
│              Vue 3 frontend · SVG floor plan         │
│              Tailwind CSS · Pinia · WebSocket        │
└────────────────────────┬────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────┐
│                   tphome-api                         │
│     FastAPI backend · MQTT orchestration · SQLite    │
│         Running on a Raspberry Pi via Docker         │
└────────────────────────┬────────────────────────────┘
                         │ MQTT (binary protocol)
┌────────────────────────▼────────────────────────────┐
│                 tphome-firmware                      │
│   C++ firmware for ESP8266 / BK7231N smart switches  │
│        Replacing factory Tuya / BSEED software       │
└─────────────────────────────────────────────────────┘
```

Each repository is independently versioned and deployable. The firmware runs on the chips inside commercial smart switches. The backend runs on a Raspberry Pi and bridges MQTT with the web layer. This frontend talks to the backend over HTTP and WebSocket.

## Repositories

<table>
<tr>
<td width="33%">

### [tphome-firmware](https://github.com/mtaibo/tphome-firmware)

Custom C++ firmware for ESP8266 and BK7231N chips, built with PlatformIO.

Replaces factory software on commercial blind controllers and light switches with a fully local MQTT-based control layer.

**C++ · PlatformIO · Arduino**

</td>
<td width="33%">

### [tphome-api](https://github.com/mtaibo/tphome-api)

FastAPI backend running on a Raspberry Pi alongside a Mosquitto MQTT broker, orchestrated with Docker.

Handles device management, state persistence, OTA firmware serving and real-time WebSocket events.

**Python · FastAPI · Docker · SQLite**

</td>
<td width="33%">

### tphome (this repo)

Vue 3 frontend served by Nginx behind a Caddy reverse proxy.

Renders an interactive SVG floor plan of my house where I can see and control every light and blind in real time.

**Vue 3 · Tailwind CSS · Pinia · Nginx**

</td>
</tr>
</table>

## What's inside this repo

This repository is the **frontend layer** of TPHome — the single interface for controlling every device in the house:

| What | How |
|---|---|
| **Blueprint view** | Interactive SVG floor plan of the house with rooms, labels, and doors |
| **Lights** | Click any light fixture on the plan to toggle it on/off |
| **Blinds** | Click a blind to open a control panel with position slider, quick buttons, and presets |
| **Live updates** | WebSocket connection receives device state changes and updates the UI in real time |
| **Device management** | Pinia store syncs device configuration and state from the API |
| **API communication** | Axios client for REST calls, WebSocket for real-time events |
| **Docker deployment** | Nginx serves the static build, Caddy handles routing |

## How it works

A typical interaction — pressing "down" on a blind from the frontend:

```
Frontend sends POST /commands/B0101/down
        │
        ▼
API publishes command via MQTT
        │
        ▼
ESP8266 chip receives command, activates relay, starts motor
        │
        ▼
Chip publishes position + motor state every second
        │
        ▼
API receives state, updates database, pushes WebSocket event
        │
        ▼
Frontend updates position in real time
```

No cloud involved at any point. The entire round trip happens on the local network.

## Supported devices

| Device | Chip | Type | Status |
|---|---|---|---|
| Matismo WIP100 | TYWE3S (ESP8266) | Blind controller | Stable |
| Matismo WIP100 | CB3S (BK7231N) | Blind controller | In progress |
| BSeed Melody M1 | T34 (BK7231N) | Light switch | In progress |

## Tech stack

| Layer | Technology |
|---|---|
| **Framework** | Vue 3 with Composition API |
| **Build** | Vite 8 |
| **Styling** | Tailwind CSS 4 |
| **State** | Pinia |
| **Routing** | Vue Router 4 |
| **HTTP** | Axios |
| **Icons** | Lucide |
| **Reverse proxy** | Caddy |
| **Container** | Docker + docker-compose |

## How to run

```bash
# Development
npm install
npm run dev

# Production build
npm run build

# Docker
docker compose up -d
```

The frontend expects `tphome-api` to be available on the same Docker network. See the [Caddyfile](Caddyfile) for routing details.

## License

MIT — see [LICENSE](LICENSE)
