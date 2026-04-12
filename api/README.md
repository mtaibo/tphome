# TPHome API

**TPHome** is a personal home automation project built from the ground up — hardware flashing, custom firmware, local MQTT backend, and a web frontend — with the goal of replacing proprietary smart home apps with a fully self-hosted, local-first stack.

This repository contains the **API layer**: a FastAPI backend running on a Raspberry Pi that acts as the bridge between the MQTT network of devices and the web frontend.

> **Note:** This project is under active development. Architecture and endpoints are subject to change.

---

## The TPHome Ecosystem

| Repository | Description | Status |
|---|---|---|
| [`tphome-firmware`](https://github.com/mtaibo/tphome-firmware) | Firmware for ESP8266 / BK7231N chips | Active |
| `tphome-api` | FastAPI + MQTT backend on Raspberry Pi | In progress |
| `tphome` | Frontend + full system orchestration | Planned |

---

## Responsibilities

- **Device management** — register, configure and monitor all TPHome devices on the network
- **MQTT orchestration** — bridge between the REST frontend and the MQTT device layer
- **OTA serving** — host compiled firmware binaries for wireless device updates
- **Home automation services** — schedules, automations and state persistence

---

## Stack

- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [Paho MQTT](https://eclipse.dev/paho/) — MQTT client
- [Docker](https://www.docker.com/) — containerised deployment on Raspberry Pi

---

## Deployment

> Full deployment guide coming once the initial architecture is stable.

The project is designed to run via Docker on a Raspberry Pi alongside an MQTT broker (Mosquitto). A `docker-compose.yml` will orchestrate both services.

```bash
# Coming soon
docker compose up -d
```

---

## Related

- [tphome-firmware](https://github.com/mtaibo/tphome-firmware) — device firmware and protocol documentation

---

## License

MIT — see [LICENSE](LICENSE)
