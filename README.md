<div align="center">

<!-- Replace with your banner -->
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

Most smart home devices ship locked to vendor clouds. You install an app per brand, none of them talk to each other, and the day the company shuts down their servers your switches stop working.

I wanted something different — a system that runs entirely on my local network, that I understood down to every layer, and that I could shape around how I actually use my home. Things like: the blind going to 20% on the first press instead of closing all the way, or a single interface that shows everything at once.

I built TPHome during my first year at university, as a personal project to learn embedded systems, networking and backend development by solving a real problem I had at home. Every layer — the chip firmware, the backend, the frontend — is designed and written from scratch.

---

## Architecture

TPHome is split into three independent repositories, each responsible for one layer of the stack:

```
┌─────────────────────────────────────────────────────┐
│                     tphome                          │
│              Web frontend (planned)                 │
└────────────────────────┬────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────┐
│                   tphome-api                        │
│     FastAPI backend · MQTT orchestration · SQLite   │
│         Running on a Raspberry Pi via Docker        │
└────────────────────────┬────────────────────────────┘
                         │ MQTT (binary protocol)
┌────────────────────────▼────────────────────────────┐
│                 tphome-firmware                     │
│   C++ firmware for ESP8266 / BK7231N smart switches │
│        Replacing factory Tuya / BSEED software      │
└─────────────────────────────────────────────────────┘
```

Each layer is independently versioned and deployable. The firmware runs on the chips inside commercial smart switches. The backend runs on a Raspberry Pi and bridges MQTT with the web layer. The frontend talks to the backend over HTTP and WebSocket.

---

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

### tphome

Web frontend — the single interface for controlling every device in the house.

Under development.

</td>
</tr>
</table>

---

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
Chip publishes position + motor state every second to tp/B0101/s
        │
        ▼
API receives state, updates database, pushes WebSocket event
        │
        ▼
Frontend updates position in real time
```

No cloud involved at any point. The entire round trip happens on the local network.

---

## Supported devices

| Device | Chip | Type | Status |
|---|---|---|---|
| Matismo WIP100 | TYWE3S (ESP8266) | Blind controller | Stable |
| Matismo WIP100 | CB3S (BK7231N) | Blind controller | In progress |
| BSeed Melody M1 | T34 (BK7231N) | Light switch | In progress |

---

## License

MIT — see [LICENSE](LICENSE)
