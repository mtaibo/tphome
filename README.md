<div align="center">

<img src="docs/banner.svg" alt="TPHome" width="100%" />

<br/>
<br/>

**A home automation system I built from scratch — firmware, backend, and frontend.**

<br/>

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made with](https://img.shields.io/badge/made%20with-C%2B%2B%20%7C%20Python%20%7C%20Vue-lightgrey)

</div>

---

I'm a first-year computer engineering student. I built TPHome because I got tired of needing five different apps to control my apartment. Every smart device wants you on its own cloud, its own account, and none of them talk to each other. And if the company goes under? Your switch is a brick.

So I started building my own system. One that lives on my local network and that I actually understand top to bottom. The C++ code inside the switches, the Python backend on a Raspberry Pi, the Vue frontend — I wrote all of it.

It started as a way to learn embedded systems and backend development by doing something real, but it turned into something I use every day. I wanted the little things to feel right — like the blind stopping at 20% on the first press instead of closing all the way, or a single screen that shows everything at once.

This is my portfolio too. I want it to show that I can build real systems, not just follow tutorials. I'm still learning, but I care about making things well.

---

## Architecture

Three layers, three repos, one system:

```
┌─────────────────────────────────────────────────────┐
│                     tphome                           │
│              Web frontend (Vue)                      │
└────────────────────────┬────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────┐
│                   tphome-api                         │
│     FastAPI backend · MQTT · SQLite                  │
│         Runs on a Raspberry Pi via Docker            │
└────────────────────────┬────────────────────────────┘
                         │ MQTT
┌────────────────────────▼────────────────────────────┐
│                 tphome-firmware                      │
│   C++ firmware for ESP8266 / BK7231N smart switches  │
│     Replaces the factory Tuya / BSEED software       │
└─────────────────────────────────────────────────────┘
```

Each layer is independent and deployable on its own. The firmware replaces the factory software on off-the-shelf smart switches. The backend sits on a Pi, bridging MQTT to the web layer. The frontend is what you see in the browser. No cloud, no vendor lock-in.

---

## Repositories

<table>
<tr>
<td width="33%">

### [tphome-firmware](https://github.com/mtaibo/tphome-firmware)

C++ firmware for ESP8266 and BK7231N chips, built with PlatformIO.

It replaces the factory software on blind controllers and light switches so everything talks over MQTT — no cloud, no vendor app.

**C++ · PlatformIO · Arduino**

</td>
<td width="33%">

### [tphome-api](https://github.com/mtaibo/tphome-api)

FastAPI backend running on a Raspberry Pi with a Mosquitto MQTT broker, all inside Docker.

Handles device management, state persistence, OTA firmware updates, and WebSocket events.

**Python · FastAPI · Docker · SQLite**

</td>
<td width="33%">

### tphome

The web frontend — one interface for every device in the house.

Under development.

</td>
</tr>
</table>

---

## How it works

Here's what happens when you press "down" on a blind:

```
Frontend sends POST /commands/B0101/down
        │
        ▼
API publishes 0xC1 to tp/B0101/c via MQTT
        │
        ▼
ESP8266 chip receives the command, activates the relay, starts the motor
        │
        ▼
Chip sends position + motor state every second to tp/B0101/s
        │
        ▼
API receives the state, updates the database, pushes a WebSocket event
        │
        ▼
Frontend updates the position in real time
```

No cloud, no internet. All on the local network.

---

## License

MIT — see [LICENSE](LICENSE)