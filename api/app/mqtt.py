from sqlmodel import Session, select
from db.database import engine
from db.models import Device, Blind, Config, DeviceLog
from connections import manager

import paho.mqtt.client as mqtt
import update
import threading
import asyncio
import struct
import os

BROKER_HOST = os.getenv("MQTT_BROKER", "mosquitto")
BROKER_PORT = int(os.getenv("MQTT_PORT", 1883))

client = mqtt.Client()
_loop: asyncio.AbstractEventLoop = None


def _push(event: str, data: dict):
    asyncio.run_coroutine_threadsafe(
        manager.broadcast({"event": event, "data": data}),
        _loop
    )


# --- Payload decoders ---

def _decode_state_msg(payload: bytes) -> tuple[str, str]:
    if len(payload) == 1:
        if payload[0] == 0x01: return "PING", ""
        if payload[0] == 0xFF: return "LWT_OFFLINE", ""
    if len(payload) == 2:
        motor_names = {0: "IDLE", 1: "WAITING", 2: "MOVING", 3: "STOPPING"}
        return "STATE", f"pos={payload[0]}% state={motor_names.get(payload[1], payload[1])}"
    if len(payload) >= 15:
        return "DEVICE_INFO", f"{len(payload)}B"
    return "UNKNOWN", ""


def _decode_log_msg(payload: bytes) -> tuple[str, str]:
    if not payload: return "UNKNOWN", ""
    code = payload[0]
    if code == 0x01: return "BOOT", "chip rebooted"
    if code == 0x20: return "MQTT_CONNECTED", "MQTT reconnected"
    if code == 0x30 and len(payload) >= 3:
        total = struct.unpack_from('<H', payload, 1)[0]
        return "FLASH_WRITE", f"total={total}"
    return f"LOG_0x{code:02X}", ""


def _decode_incoming(topic_parts: list, payload: bytes) -> tuple[str, str]:
    suffix = topic_parts[2] if len(topic_parts) > 2 else ""
    if suffix == "s": return _decode_state_msg(payload)
    if suffix == "l": return _decode_log_msg(payload)
    return suffix.upper(), ""


def _decode_outgoing(topic: str, payload: bytes) -> tuple[str, str]:
    parts = topic.split("/")
    suffix = parts[-1] if parts else ""
    if suffix == "c":
        if not payload: return "EMPTY", ""
        cmd = payload[0]
        if cmd <= 100: return "SET_POSITION", f"pos={cmd}%"
        names = {0xC0: "UP", 0xC1: "DOWN", 0xC2: "STOP", 0xC3: "PING", 0xC4: "GET_STATE"}
        return names.get(cmd, f"CMD_0x{cmd:02X}"), ""
    if suffix == "a":
        if not payload: return "EMPTY", ""
        cmd = payload[0]
        names = {
            0xA0: "OTA", 0xA1: "REBOOT", 0xA2: "RESET_MEM",
            0xA3: "GET_INFO", 0xA4: "SET_POS", 0xA5: "SET_PREFS"
        }
        detail = ""
        if cmd == 0xA0 and len(payload) >= 4:
            detail = f"v{payload[1]}.{payload[2]}.{payload[3]}"
        elif cmd == 0xA4 and len(payload) >= 3:
            detail = f"pos={struct.unpack_from('<H', payload, 1)[0]}"
        return names.get(cmd, f"ADMIN_0x{cmd:02X}"), detail
    return suffix.upper(), ""


def _log_message(device_id: str, direction: str, topic: str, payload: bytes, event_label: str, event_detail: str = ""):
    try:
        entry = DeviceLog(
            device_id=device_id,
            direction=direction,
            topic=topic,
            payload_hex=payload.hex().upper() if payload else "",
            event_label=event_label,
            event_detail=event_detail,
        )
        with Session(engine) as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)

        _push("device_log", {
            "id": entry.id,
            "device_id": device_id,
            "timestamp": entry.timestamp.isoformat(),
            "direction": direction,
            "topic": topic,
            "payload_hex": entry.payload_hex,
            "event_label": event_label,
            "event_detail": event_detail,
        })
    except Exception as e:
        print(f"[MQTT] Error saving log entry: {e}")


# --- MQTT handlers ---

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print(f"[MQTT] Connection error. Code: {rc}")
    else:
        print("[MQTT] Connected to broker")
        client.subscribe("tp/#")
        client.subscribe("def/#")


def on_message(client, userdata, message):
    topic = message.topic.split("/")
    payload = message.payload

    if len(topic) < 3: return

    device_id = topic[1]

    # Log all incoming device traffic (skip global tp/a/c)
    if topic[0] in ("tp", "def") and device_id != "a":
        label, detail = _decode_incoming(topic, payload)
        _log_message(device_id, "rx", message.topic, payload, label, detail)

    if topic[2] != "s": return  # Stop here for /l and other non-state topics
    if len(payload) == 0: return

    # DeviceID announcement
    if len(payload) == 1 and payload[0] == 0x01 and update.is_active():
        update.handle_announcement(device_id)
        return

    # LWT — device disconnected unexpectedly
    if len(payload) == 1 and payload[0] == 0xFF:
        _update_online(device_id, online=False)
        _push("device_offline", {"id": device_id})
        return

    # Ping — device is alive
    if len(payload) == 1 and payload[0] == 0x01:
        _update_online(device_id, online=True)
        _push("device_online", {"id": device_id})
        return

    # State update — position + motor state
    if len(payload) == 2:
        _update_state(device_id, position=payload[0], motor_state=payload[1])
        state = {
            "id" : device_id,
            "state" : {
                "position": payload[0],
                "motor_state": payload[1]
            }
        }
        _push("device_state", state)

    if len(payload) >= 15:

        try:

            unpacked = struct.unpack("<BBB3s2sHHH?", payload[:15])

            info = {
                "id": f"{chr(unpacked[0])}{unpacked[1]:02d}{unpacked[2]:02d}",

                "hardware" : {
                    "mac"                  : unpacked[4].hex(':'),
                    "firmware_version"     : unpacked[3].hex('.'),
                },

                "prefs": {
                    "up_time"          : unpacked[5],
                    "down_time"        : unpacked[6],
                    "down_pos"         : unpacked[7],
                    "inverted_relays"  : unpacked[8]
                }
            }

            _update_device_info(device_id, info)
            _push("device_info", info)

        except struct.error as e:
            print(f"Error decodificando payload de {device_id}: {e}")



def _update_online(device_id: str, online: bool):
    from datetime import datetime
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.id == device_id)).first()
        if not device:
            return
        device.online = online
        if online:
            device.last_seen = datetime.now()
        session.add(device)
        session.commit()


def _update_state(id: str, position: int, motor_state: int):
    from datetime import datetime
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.id == id)).first()
        if not device:
            print("LOG: Device to update state was not found")
            return

        device.online = True
        device.last_seen = datetime.now()

        if device.id[0] == "B":
            blind = session.exec(select(Blind).where(Blind.id == id)).first()
            blind.position = position
            blind.motor_state = motor_state
            session.add(blind)

        session.add(device)
        session.commit()


def _update_device_info(device_id: str, info: dict):
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.id == device_id)).first()
        if not device:
            print("LOG: Device to update its info was not found")
            return

        device.firmware_version = info["hardware"]["firmware_version"]
        device.mac = info["hardware"]["mac"]

        if device.id[0] == "B":
            blind        = session.exec(select(Blind).where(Blind.id == device_id)).first()
            device_prefs = info["prefs"]

            config       = session.get(Config, 1)
            config_prefs = (
                config.devices.get("blinds", {}).get(device_id, {}).get("prefs", {})
                if config and config.devices else {}
            )

            if config_prefs and any(config_prefs.get(k) != device_prefs.get(k) for k in config_prefs):
                try:
                    payload = struct.pack('<HHH?',
                        config_prefs['up_time'], config_prefs['down_time'],
                        config_prefs['down_pos'], config_prefs['inverted_relays']
                    )
                    publish(f"tp/{device_id}/a", bytes([0xA5]) + payload)
                except (KeyError, struct.error) as e:
                    print(f"[MQTT] Drift correction failed for {device_id}: {e}")

            blind.up_time        = device_prefs["up_time"]
            blind.down_time      = device_prefs["down_time"]
            blind.down_pos       = device_prefs["down_pos"]
            blind.inverted_relays = device_prefs["inverted_relays"]
            session.add(blind)

        session.add(device)
        session.commit()


def publish(topic: str, payload: bytes):
    parts = topic.split("/")
    if len(parts) == 3 and parts[0] in ("tp", "def") and parts[1] != "a":
        label, detail = _decode_outgoing(topic, payload)
        _log_message(parts[1], "tx", topic, payload, label, detail)
    client.publish(topic, payload)


def setup(loop: asyncio.AbstractEventLoop):
    global _loop
    _loop = loop

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT)

    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True
    thread.start()
