from sqlmodel import Session, select
from db.database import engine
from db.models import Device, Blind
from connections import manager

import paho.mqtt.client as mqtt
import asyncio
import threading
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

    if topic[0] == "def":
        return  # Handled by provisioning router

    if topic[0] != "tp" or topic[2] != "s":
        return  # Ignore anything that is not a state message

    device_id = topic[1]

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
    if len(payload) >= 2:
        _update_state(device_id, position=payload[0], motor_state=payload[1])


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


def _update_state(device_id: str, position: int, motor_state: int):
    from datetime import datetime
    with Session(engine) as session:
        device = session.exec(select(Device).where(Device.id == device_id)).first()
        if not device:
            return

        device.online = True
        device.last_seen = datetime.now()

        if device.type == "blind":
            blind = session.exec(select(Blind).where(Blind.device_id == device_id)).first()
            if not blind:
                return
            blind.position = position
            blind.motor_state = motor_state
            session.add(blind)
            _push("device_state", {
                "id": device_id,
                "position": position,
                "motor_state": motor_state
            })

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