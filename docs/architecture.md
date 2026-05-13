# TPHome Architecture

## Overview

TPHome is a three-layer home automation system designed to run entirely on the local network with no cloud dependency. Each layer is a separate repository, independently versioned and deployable.

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (tphome)                  │
│   Vue 3 SPA · SVG floor plan · Pinia state · Nginx  │
│   Communicates via HTTP REST + WebSocket             │
└────────────────────────┬────────────────────────────┘
                         │ :80  Caddy reverse proxy
                         │ /api/* → tphome-api:8000
                         │ /ws/*  → tphome-api:8000
                         │ /*     → tphome-frontend:80
┌────────────────────────▼────────────────────────────┐
│                  Backend (tphome-api)                 │
│   FastAPI · Mosquitto MQTT · SQLite · Docker         │
│   Running on Raspberry Pi 4                          │
│   Manages devices, state persistence, OTA updates    │
└────────────────────────┬────────────────────────────┘
                         │ MQTT over WiFi (local network)
                         │ Topics: tp/<device_id>/c (commands)
                         │         tp/<device_id>/s (state)
┌────────────────────────▼────────────────────────────┐
│                 Firmware (tphome-firmware)            │
│   C++ on ESP8266 / BK7231N · PlatformIO · Arduino    │
│   Runs inside commercial smart switches              │
│   Replaces factory Tuya / BSEED firmware             │
└─────────────────────────────────────────────────────┘
```

## Frontend architecture (this repo)

### Component tree

```
App.vue
  └── <RouterView>
       ├── Dashboard.vue
       │    ├── Sidebar.vue        (collapsible navigation)
       │    ├── Topbar.vue         (API status, active count)
       │    └── Blueprint.vue      (SVG floor plan container)
       │         ├── svg
       │         │    ├── HouseLayer.vue   (rooms, labels, doors)
       │         │    ├── BlindsLayer.vue  (blind rectangles)
       │         │    └── LightsLayer.vue  (light circles)
       │         └── BlindsControl.vue     (control panel sidebar)
       └── Settings.vue           (placeholder)
```

### State management (Pinia)

Two stores are defined, both initialized in `App.vue` on mount:

**`useDevices` store** (`src/config/devices.js`)
- `storage` — reactive object `{ lights: {}, blinds: {}, switches: {} }`
- `blinds` — computed, filters out devices with null state
- `lights` — computed, filters out devices with null state
- `active` — computed, count of online blind devices
- `setup()` — fetches device config from API, populates storage, then calls `update()`
- `update()` — fetches current device states from API, syncs preferences

**`useMap` store** (`src/config/map.js`)
- `storage` — reactive object with `viewBox`, `rooms[]`, `labels[]`, `doors[]`
- `setup()` — fetches map config from API

### Real-time communication

The WebSocket client (`src/config/socket.js`) connects on app mount and handles these events:

| Event type | Action |
|---|---|
| `device_state` | Updates device position/motor_state in store |
| `device_online` | Marks device as online |
| `device_offline` | Marks device as offline |
| `device_info` | Updates device preferences |

The client auto-reconnects every 3 seconds on disconnect.

### Device configuration

Devices are configured via JSON files stored at `src/db/` and served by the API:

**`devices.json`** — Lists every device with:
- `id` — unique identifier (`L0101`, `B0101`, etc.)
- `name` — human-readable name
- `map` — SVG coordinates (position for lights, position+dimensions for blinds)
- `prefs` — device-specific preferences (motor timings, relay config)

**`map.json`** — Defines the floor plan:
- `viewBox` — SVG viewBox dimensions
- `rooms[]` — rectangles with id, x, y, w, h
- `labels[]` — text elements with x, y coordinates
- `doors[]` — line segments with x1, y1, x2, y2

### Communication flow

#### User toggles a light
```
User clicks light circle on SVG
  → LightsLayer.vue emits 'toggle' event
  → api.sendCommand('L0101', 'toggle')
  → POST /api/commands/L0101/toggle
  → API publishes to MQTT topic tp/L0101/c
  → Firmware receives and toggles relay
  → Firmware publishes new state to tp/L0101/s
  → API receives, stores in DB, broadcasts via WebSocket
  → Frontend WebSocket handler updates store
  → Vue reactivity updates the light circle UI
```

#### User adjusts a blind
```
User clicks blind on SVG
  → Blueprint.vue sets selectedId
  → BlindsControl.vue panel opens
  → User drags slider or clicks preset
  → api.sendCommand('B0101', 'set', 50)
  → POST /api/commands/B0101/set/50
  → API publishes to MQTT
  → Firmware runs motor for calculated time
  → Firmware publishes position every second
  → Real-time UI updates via WebSocket
```

### Deployment

The frontend is dockerized with a multi-stage build:

1. **Build stage**: `node:20-alpine`, installs deps, runs `vite build`
2. **Production stage**: `nginx:stable-alpine`, serves `dist/` from `/usr/share/nginx/html`

`docker-compose.yml` runs two services:
- `caddy` — reverse proxy (port 80), routes API calls to backend
- `tphome-frontend` — nginx serving static files

Both connect to an external Docker network `tphome-network` where `tphome-api` lives.

### File reference

| File | Purpose |
|---|---|
| `src/App.vue` | Root component, initializes all stores |
| `src/main.js` | Vue app creation, plugin registration |
| `src/main.css` | Tailwind imports, theme tokens, component classes |
| `src/router.js` | Route definitions (/, /settings) |
| `src/config/api.js` | Axios HTTP client |
| `src/config/socket.js` | WebSocket client |
| `src/config/devices.js` | Pinia device store |
| `src/config/map.js` | Pinia map store |
| `src/views/Dashboard.vue` | Main dashboard layout |
| `src/layout/Sidebar.vue` | Left navigation sidebar |
| `src/layout/Topbar.vue` | Top status bar |
| `src/layout/BlindsControl.vue` | Blind control panel |
| `src/components/Blueprint.vue` | SVG blueprint container |
| `src/components/blueprint-layers/HouseLayer.vue` | Rooms/labels/doors SVG |
| `src/components/blueprint-layers/BlindsLayer.vue` | Blinds SVG layer |
| `src/components/blueprint-layers/LightsLayer.vue` | Lights SVG layer |
| `src/db/devices.json` | Device configuration data |
| `src/db/map.json` | Floor plan configuration data |
| `Caddyfile` | Reverse proxy routing rules |
| `nginx.conf` | Static file serving config |
| `Dockerfile` | Multi-stage build |
| `docker-compose.yml` | Service orchestration |
| `vite.config.js` | Vite build configuration |
