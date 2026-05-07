from sqlmodel import Session, select
from db.database import engine
from db.models import Device, Blind
from connections import manager

import paho.mqtt.client as mqtt
import provisioning
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

    if topic[2] != "s": return # Ignore anything that is not a state message
    if len(payload) == 0: return

    device_id = topic[1]

    # DeviceID announcement
    if len(payload) == 1 and payload[0] == 0x01 and provisioning.is_active():
        provisioning.handle_announcement(device_id)
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

        if device.type == "B":
            blind = session.exec(select(Blind).where(Blind.id == id)).first()
            blind.position = position
            blind.motor_state = motor_state
            session.add(blind)
            _push("device_state", {
                "id": id,
                "position": position,
                "motor_state": motor_state
            })

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

        if device.type == "B":
            blind = session.exec(select(Blind).where(Blind.id == device_id)).first()
            blind.up_time = info["prefs"]["up_time"]
            blind.down_time = info["prefs"]["down_time"]
            blind.down_pos = info["prefs"]["down_pos"]
            blind.inverted_relays = info["prefs"]["inverted_relays"]
            session.add(blind)
        
        session.add(device)
        session.commit()


def publish(topic: str, payload: bytes):
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