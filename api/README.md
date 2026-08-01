<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../images/banner/dark.svg">
  <img src="../images/banner/light.svg" alt="TPHome" width="100%" />
</picture>

<br/>
<br/>

**The brain of the home automation system — bridging MQTT devices to the web.**

<br/>

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made with](https://img.shields.io/badge/made%20with-Python%20%7C%20FastAPI%20%7C%20Docker-lightgrey)

</div>

---

I'm a first-year computer engineering student and this is the backend layer of a home automation system I built from scratch. The full system lives in this monorepo: firmware (C++ for ESP8266/BK7231N switches), this API (FastAPI on Raspberry Pi), and the frontend (Vue 3, also on the Pi).

This module contains the **backend layer** that sits between the physical devices and the web interface. It's a FastAPI server that handles MQTT orchestration, device management, state persistence, real-time WebSocket events, OTA firmware updates, and device discovery — all running on a Raspberry Pi on my home network.

## Monorepo structure

<table>
<tr>
<td width="33%">

### [firmware/](../firmware/)

Custom C++ firmware for proprietary chips, built with PlatformIO.

Replaces factory software on commercial blind controllers and light switches with a fully local MQTT-based control layer.

**C++ · PlatformIO · Arduino**

</td>
<td width="33%">

### api/ (this module)

FastAPI backend running on a Raspberry Pi alongside a Mosquitto MQTT broker, managed with Docker.

Handles device management, state persistence, OTA firmware serving and real-time WebSocket events.

**Python · FastAPI · Docker · SQLite**

</td>
<td width="33%">

### [frontend/](../frontend/)

Vue 3 frontend served by Nginx behind a Caddy reverse proxy, also hosted on the Raspberry Pi.

Renders an interactive SVG floor plan where you can see and control every light and blind in real time.

**Vue 3 · Tailwind CSS · Nginx**

</td>
</tr>
</table>

## API architecture

```
┌───────────────────────────────────────────────────────┐
│                     tphome-api                        │
│                                                       │
│  ┌───────── HTTP ──────────┐  ┌─── WebSocket ────┐    │
│  │    REST routers         │  │ connections.py   │    │
│  │  ┌──────────────────┐   │  │  broadcast()     │    │
│  │  │ commands.py      │   │  └────────┬─────────┘    │
│  │  │ devices.py       │   │           │              │
│  │  │ config.py        │   │           │              │
│  │  │ admin.py         │   │           │              │
│  │  └───────┬──────────┘   │           │              │
│  └──────────┼──────────────┘           │              │
│             │                          │              │
│  ┌──────────▼──────────────────────────▼───────────┐  │
│  │                   mqtt.py                       │  │
│  │  publish() · binary message parsing · loop      │  │
│  └──────────┬──────────────────────────┬───────────┘  │
│             │                          │              │
│  ┌──────────▼───────┐    ┌─────────────▼───────────┐  │
│  │    Mosquitto     │    │  SQLite (SQLModel)      │  │
│  │   MQTT Broker    │    │  Device · Blind · Light │  │
│  │                  │    │  Config · PendingDevice │  │
│  │  tp/{id}/{c,s,a} │    └─────────────────────────┘  │
│  │  def/{mac}/a     │                                 │
│  └──────────────────┘                                 │
│                                                       │
│  ┌───────────────────────────────────────────────┐    │
│  │           provisioning.py                     │    │
│  │  Device discovery via MQTT broadcast          │    │
│  └───────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

The API is structured around five routers, each with a single responsibility. The MQTT module is the core — it subscribes to device topics, parses incoming binary messages, updates the database, and broadcasts state changes to all connected WebSocket clients. The provisioning module handles device discovery when new hardware appears on the network.

## What's managed here

| What | How |
|---|---|
| **MQTT orchestration** | Bridges REST commands to the MQTT device layer and parses incoming state updates |
| **REST API** | Full CRUD for devices, configuration, and commands over HTTP |
| **Real-time updates** | WebSocket endpoint pushes device state, online status, and discovery events to the frontend |
| **State persistence** | SQLite database with SQLModel keeps device positions, preferences, and config across reboots |
| **Device discovery** | MQTT broadcast protocol identifies new hardware and prepares it for configuration |
| **OTA updates** | Serves firmware binaries and triggers wireless updates for supported chips |
| **Device provisioning** | Manages the lifecycle from announcement → pending → configured device |

## Endpoints & data flow

The API communicates with devices over MQTT using a custom binary protocol. Each device publishes state updates to `tp/{id}/s` and receives commands on `tp/{id}/c`.

**Database models** — four SQLModel tables handle persistence:

| Table | Purpose |
|---|---|
| `Device` | Hardware info (MAC, firmware version, online status, last seen) |
| `Blind` | Position (0–100), motor state (up/down/stopped), timing preferences |
| `Light` | On/off state |
| `Config` | Devices and map JSON blobs served to the frontend |
| `PendingDevice` | Unconfigured devices discovered on the network |

A typical command flow looks like this:

```
Frontend sends POST /commands/B0101/down
        │
        ▼
commands.py publishes 0xC1 to tp/B0101/c via MQTT
        │
        ▼
ESP8266 receives command, activates relay, starts motor
        │
        ▼
Chip publishes 2-byte state (position + motor_state) to tp/B0101/s
        │
        ▼
mqtt.py parses binary payload, updates Blind row in SQLite
        │
        ▼
connections.py broadcasts device_state event to all WebSocket clients
```

The binary protocol keeps messages compact — state updates are 2 bytes, device info is 15 bytes packed with `struct`, and commands are single-byte opcodes. This matters on a local network where dozens of devices report every second.

## Tech stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI |
| **Language** | Python 3.11 |
| **ORM** | SQLModel (SQLAlchemy + Pydantic) |
| **MQTT client** | Paho-MQTT |
| **MQTT broker** | Mosquitto (Docker) |
| **WebSocket** | Native FastAPI WebSockets |
| **Database** | SQLite |
| **Container** | Docker + docker-compose |

## How to run

The API is designed to run alongside a Mosquitto MQTT broker, both managed by Docker on a shared network.

```bash
# Clone the monorepo
git clone https://github.com/mtaibo/tphome
cd tphome/api

# Set up environment
cp .env.example .env

# Start services
docker compose up --build -d
```

The `.env` file configures the MQTT broker address and database path:

```
MQTT_BROKER=mosquitto
MQTT_PORT=1883
DATABASE_URL=sqlite:////app/storage/tphome.db
```

The API exposes port `8000` internally and expects to be reached through the `tphome-network` Docker network (shared with the frontend).

## License

MIT — see [LICENSE](LICENSE)
