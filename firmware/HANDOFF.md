# Firmware handoff — power, reconnect and refactor (Nov 2026)

Temporary working notes for the next Claude session. **Delete this file once everything below is verified**, and update `~/workspace/agents/repos/tphome.md`.

## Why this work happened

Reported by Miguel on 2026-11-10:

- Power problems with the blind switches (Matismo WIP100, TYWE3S / ESP8266). **One switch burned out.** Power use is the top priority.
- **One blind has been offline for about a week (since ~2026-11-03) and never reconnected.** Unknown whether it is drawing extra power or at risk.
- The firmware was almost all headers with logic in them, and very few `.cpp` files.

## What was changed (all on `main`)

| Commit | What |
|---|---|
| `9f5a036` | `fix: cut power use while offline and reboot devices stuck without network` |
| `807b888` | `fix: keep the loop non-blocking and relays off during reboots, OTA and AP mode` |
| `f2d1418` | `refactor: split firmware modules into declaration headers and source files` |
| `d2510e8` | `docs:` README firmware section updated to match |

The last commit before this work is `d5a04d3` (use it to compare builds, sizes and behaviour).

### 9f5a036 — power and offline recovery

- `src/main.cpp`: `delay(10)` at the end of `loop()`. Before, the loop spun with no idle time at all, so the CPU ran at 100 % and the WiFi modem sleep worked poorly. 10 ms matches the centisecond resolution every timer already uses (buttons, LEDs, motor).
- TX power **10 → 16 dBm** (`TX_POWER` in `driver_wifi`). History: 18.5 → 14 (`39d2f5a`) → 16 (`809e9de`, raised *because of drops*) → 10 (`9769645`). The radio transmits a tiny fraction of the time, so TX power barely changes average consumption but costs range. 16 was the last value without drops.
- WiFi reconnect is now a 3-phase state machine (`src/network/wifi.cpp`): `Online`, `Joining` (each attempt gets 15 s), and `Asleep` (radio **fully off** via `WiFi.forceSleepBegin()`, backoff 5 → 10 → 20 → 40 → 60 s). Before, an offline device kept its radio on nonstop (~70 mA, against ~15–20 mA connected with modem sleep). That is probably what the week-long offline blind has been doing.
- `Hardware::Wifi::wake()` re-applies mode, hostname, sleep mode and TX power after waking the radio (`configure()`).
- `Network::update(busy)`: **reboots after 15 min without WiFi + MQTT**, only if the blind is idle and the switch is in NORMAL mode. The ESP8266 WiFi stack sometimes wedges after many `disconnect`/`begin` cycles, and only a restart fixes it.
- `Mqtt::drop()`: when WiFi goes down, the MQTT socket is closed at once instead of waiting about 90 s for keepalive.
- The BOOT log (`tp/{ID}/l`, code `0x01`) now carries **1 extra byte: the reset reason** (`ESP.getResetInfoPtr()->reason`). The API (`api/app/mqtt.py`, `RESET_REASONS`) decodes it as power on / hardware watchdog / exception / software watchdog / software restart / deep sleep wake / external reset. A run of "power on" or watchdog boots before a switch disappears points to a failing power supply.

### 807b888 — never block with a relay on

- MQTT `connect()` used to block for up to about 15 s (WiFiClient connect timeout plus `setSocketTimeout(10)`). Now `_wifiClient.setTimeout(2000)` and `setSocketTimeout(2)`, and **no reconnect attempts while the blind is moving** (`Mqtt::update(busy)`).
- The global ping (`tp/a/c` `0x01`) used `delay(random(50,1000))` inside the MQTT callback. It is now scheduled through `_pendingPing` and sent from `Commands::update()`.
- `Settings::reboot()` turns both relays off first (`Hardware::relaysOff()`). Before, it waited 3 s with a relay possibly still on.
- `Blinds::stop()` is called before every reboot, reset, provisioning reboot and AP start, and when entering connection mode (long press on the top button). This saves the position correctly.
- OTA is **rejected while the motor runs**. `ESPhttpUpdate.rebootOnUpdate(false)`: the firmware version is stored **only if the update succeeded**. Before, a failed OTA still saved the new version number. On failure the backlight is restored and the old firmware keeps running.
- AP mode used to be `while(true)`. It now closes after **10 min** and reboots, with `delay(5)` per iteration. A forgotten AP had the radio transmitting nonstop.
- `SET_POS` (`0xA4`) is ignored while moving, because the motor overwrites the position every loop.
- **LWT bug:** PubSubClient sends the will message with `strlen()`, and the old `&offlineByte` had no terminator. The offline message went out with stack garbage after `0xFF`, and the API (which expects exactly 1 byte) could miss it. It is now `{0xFF, '\0'}`.
- LED blink: the `uint16_t` subtraction promoted to `int`, so after the 655 s wrap blinking froze forever (connection mode). It is now cast back to `uint16_t`.
- The MQTT "wait 3 s on boot" hack (`lastTime = now + 3000`) underflowed and never waited. It is replaced by an `attempted` flag (first attempt runs immediately).
- `Motor` no longer reads `Settings::state` during static init (it read 0 before settings were loaded, which was misleading).

### f2d1418 — headers vs sources

The rule now:

- **`include/` headers only declare**: enums, structs, constants and function prototypes.
- **`src/` mirrors the layout and holds every definition**. Private state and helpers are `static` inside their `.cpp`.
- Exceptions kept in headers on purpose: the `InputPin`/`OutputPin` templates (`driver_input.h`, `driver_output.h`) and three one-line `inline` helpers in `hardware.h` (`relaysOff`, `enableLight`, `disableLight`).
- `include/hardware/board.h` is the single place that picks the board (`hardware/esp8266/hardware.h` or `hardware/bk7231n/hardware.h`). Everything else includes `hardware/board.h`.
- `hardware/esp8266/hardware.h` also pulls in `driver_wifi.h`.
- Hardware-specific `.cpp` files (`src/hardware/esp8266/*`) are wrapped in `#if defined(DEVICE_HARDWARE_ESP8266)`. `src/logic/blinds.cpp` is wrapped in `#if defined(DEVICE_TYPE_BLIND)`.
- The circular include between blinds and commands, and the `Commands::publishState` forward declaration, are gone. `Blinds::state()` replaces direct access to `Blinds::_motor`. `Mqtt::publish()` replaces `Mqtt::_client`. `Hardware::Wifi::macAddress()` replaces `WiFi.macAddress()` in settings and commands.
- `Diagnostics::flashWrites` is `extern` and defined in `src/diagnostics.cpp`.

```
src/main.cpp
src/diagnostics.cpp
src/hardware/esp8266/{hardware,driver_wifi}.cpp
src/settings/{settings,mode}.cpp
src/logic/{leds,buttons,blinds,actions}.cpp
src/network/{wifi,mqtt,commands,network,ota,ap}.cpp
```

## Verification status: builds, not yet tested on a device

Built on the Mac on 2026-11-10 (Rosetta installed) with the Arduino ESP8266 core **3.1.2** (`framework-arduinoespressif8266 3.30102.0`). `blind_esp8266` builds with no warnings from the project sources.

| Build | RAM | Flash |
|---|---|---|
| `d5a04d3` (before) | 30188 B (36.9 %) | 354627 B (46.5 %) |
| `0729ee1` (after) | 30120 B (36.8 %) | 355479 B (46.7 %) |

The sketch area is 761840 B, so an OTA image of about 355 KB still fits in the free space.

Spots that were checked against the core source, so no need to recheck them:

- `WiFiClient::setTimeout()` is passed to `ClientContext` and limits `connect()`. The 2 s cap works.
- The radio sleep sequence works on 3.1.2: `forceSleepBegin()` stores the current mode (already `WIFI_OFF` after `disconnect(true)`). Then `forceSleepWake()` wakes the modem, and `configure()` → `WiFi.mode(WIFI_STA)` turns station mode back on, with hostname and TX power applied again. `forceSleepBegin()` already waits 10 ms internally, so the extra `delay(1)` is harmless.
- `user_interface.h` and the reset reason, the function-pointer callback and `min()` all compile.

## On-device test, B0101 (2026-11-10)

Firmware **2.2.0** (API firmware id 3, now the *active* one) was flashed to **B0101** by OTA, run from the Pi over SSH (`ssh tphome`).

How the tests were done:

- **Commands:** published straight to the broker with `docker exec tphome-broker mosquitto_pub` (binary payloads via `printf`).
- **Traffic:** recorded with `mosquitto_sub -F "%I %t %x"`.
- **API calls:** made from inside the container with `docker exec tphome-api python -c "urllib…"`. The container has no `curl` or `requests`, so uploads use a hand-built multipart body.

Results:

- **OTA:** works. The BOOT log came back as `01 04` (software restart). GET_INFO returns 15 bytes: `B 01 01`, version `2.2.0` (saved only after a successful OTA), the real MAC `06:28`, and the real prefs (32 s up / 30 s down / 20 % / not inverted).
- **Ping, state and global ping:** they answer. The global ping answer is delayed without blocking.
- **Movement:**
  - 100 → 90 % lands exactly.
  - An OTA sent mid-move is ignored.
  - UP followed by 80 % reverses after the 1 s pause.
  - Back to 100 % includes the 2 s end-of-travel run.
  - One FLASH_WRITE log per stop.
- **Remote reboot (`0xA1`):** the LWT is now exactly 1 byte, `FF`. Then `01 04`, then online again (after the API fix below).
- **Broker restart:** B0101 reconnects within 6 s and logs `MQTT_CONNECTED`. The old-firmware switches came back too.

**Not tested** (needs physical access or the router):

- WiFi loss: radio off between attempts, reconnect after a radio sleep, and the 15 min offline reboot;
- AP mode timeout;
- LED blink after 11 min;
- buttons;
- current draw.

### Things fixed or found during the test

- **OTA had been broken since the tphome Caddy was dropped.** Nothing listened on `192.168.1.160:80`, and the tpcloud gateway only matches hostnames. Fixed in tpcloud `181994f`: a gateway listener on `:8081` that only serves `/firmware`, published as host port 80. It is LAN-only (no router port forward), every other path returns 404 even with a spoofed Host, and the public sites are unaffected.
- **API `fd4a014`** (deployed on the Pi, `docker compose up -d --build api` in `~/tphome`), which fixes two things:
  - Now that the LWT works, a rebooted device stayed "offline" because nothing marked it online again. BOOT (`0x01`) and MQTT_CONNECTED (`0x20`) logs now mark it online.
  - Any state payload starting with `0xFF` is treated as LWT. Firmware before 2.2.0 sent `FF` plus stack garbage (20 bytes), which the API parsed as DEVICE_INFO. That is why every device had version `3f.98.ae`, MAC `20:40`, junk prefs, and never went offline, and why the API kept re-sending SET_PREFS.
- **Live devices** (global ping): B0101, B0102, B0201. **B0301 does not answer** (last seen by the API 2026-11-07), so it is the likely "offline for a week" blind, not B0101. **B0401** appears in the broker log until 2026-08-28 but isn't in the API.
- The broker's Docker log (json-file) has NUL bytes from around 2026-10-30/31. The broker restarted 2026-10-31 07:38 UTC, which looks like an unclean shutdown. `docker logs` stops reading there, and the raw file needs sudo, which the SSH session doesn't have.

## Next steps

1. **Build** (done on the Mac, repeat wherever you flash from): `cd firmware && ./build.sh`. This generates `include/settings/credentials.h` from the root `.env` and builds `blind_esp8266`.
   - The binary is at `.pio/build/blind_esp8266/firmware.bin`.
   - Only `blind_esp8266` builds. The `blind_bk7231n` and `light_bk7231` drivers are empty files, so those envs were already broken.
2. **First switch (B0101)** — see the test above:
   - [x] Boots and connects. The BOOT log shows "software restart" after an OTA.
   - [x] Up / stop / set position by MQTT, and position tracking is right. *Buttons and the down-twice behaviour not tried.*
   - [x] Reversing while moving waits 1 s before the other relay closes.
   - [x] The global ping is answered.
   - [x] The LWT is 1 byte (`FF`). The API marks the device offline, then online again on BOOT.
   - [x] Broker restart → MQTT reconnects on its own. *Button responsiveness during the outage not checked.*
   - [ ] WiFi loss → the radio goes off between attempts, it reconnects when WiFi returns, and it reboots after 15 min offline. **Most important open item.**
   - [x] OTA while moving is ignored. *A failed OTA was not tried.*
   - [ ] Connection mode LED after 11 min, and the AP timeout after 10 min.
3. **Measure current** if possible (bench unit on 3.3 V with a meter): connected idle, offline, and moving, before (`d5a04d3`) vs after. The expectation is a lower idle draw and a much lower offline draw.
4. Then roll out to the rest by OTA, one at a time. 2.2.0 is already the active firmware, so it's just `POST /admin/{id}/ota?version=2.2.0` (or the frontend button) for B0102 and B0201. B0301 needs the checks below first.

## The blind that's been offline for a week (probably B0301)

The firmware can't tell what happened. Ask Miguel:

- **Do its buttons still move the blind?**
  - Yes → the MCU is alive and the problem is network: a wedged WiFi stack, or a weak link at 10 dBm. Power-cycling it from the breaker for 10 s should bring it back, then flash the new firmware.
  - No, with LEDs off → hardware or power supply. Same model as the one that burned, so open it.
- **Look at its logs** (frontend → device logs, `tp/{ID}/l`) from before it went dark. Many BOOT entries in a row point to brownouts from a failing power supply.
- Until checked, it has been running a week at its worst sustained load (radio always on plus the green LED), in a wall box. Suggest cutting its power until it's inspected.

## Not changed / ideas for later (ask Miguel first)

- **Light sleep** (`WIFI_LIGHT_SLEEP`) would cut idle power a lot more. But buttons are polled, so presses could be missed during sleep unless GPIO wake-up is set up. Measure after this round first.
- The **green LED stays solid while offline** (a few mA). A short blink would save power, but Miguel removed the connection blink on purpose in `90e8527`.
- The relay interlock was reviewed and is correct: both relays are always off before either turns on, there is a 1 s dead time on reversal, and the run time is capped at travel time + 2 s. The burned switch is most likely hardware (relay arcing with no snubber, an undersized supply, heat in the wall box), not firmware.
- Unused defaults `Defaults::ID`, `IS_MOVING` and `IS_WAITING` can go.
