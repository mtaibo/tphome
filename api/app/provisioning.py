import asyncio
from datetime import datetime
from sqlmodel import Session, select
from db.database import engine
from db.models import Device, PendingDevice
from connections import manager
import mqtt

DISCOVERY_TIMEOUT = 5

_responses: set[str] = set()
_active = False


def handle_announcement(id: str):
    if _active: _responses.add(id)


def is_active():
    return _active


async def start():
    global _active, _responses

    # Restart variables to start new discovery
    _responses = set()
    _active = True

    # Send the MQTT message and wait for the responses
    mqtt.publish("tp/a/c", b"\x01")
    await asyncio.sleep(DISCOVERY_TIMEOUT)

    # Set discovery state to inactive and process responses
    _active = False
    await _process()


async def _process():
    online = []
    offline = []
    pending = []

    with Session(engine) as session:

        known_devices = session.exec(select(Device)).all()
        known_macs = {device.mac for device in known_devices}

        # Known devices
        for device in known_devices:

            if device.id in _responses: # ID on db
                online.append(device.id)
                _responses.discard(device.id)

                device.online = True
                device.last_seen = datetime.now()
                session.add(device)

            elif device.mac in _responses: # MAC on db, device was unconfigured
                pending.append(device.mac)
                _responses.discard(device.mac)

                # Delete device from db to then add it as pending
                session.delete(device)
                session.add(PendingDevice(mac=device.mac))

            else: # ID on db without response, set to offline
                offline.append(device.id)

                device.online = False
                session.add(device)

        # Unknown responses
        for mac in _responses:

            if len(mac) > 4:
                mqtt.publish(f"tp/{mac}/a", bytes([0xA2]) + b"")
                continue

            # Unknown id, move to pending
            pending_device = session.exec(select(PendingDevice).where(PendingDevice.mac == mac)).first()
            if not pending_device: 
                pending.append(mac)
                session.add(PendingDevice(mac=mac))

        session.commit()

    await manager.broadcast({
        "event": "discovery_complete",
        "data": {
            "online": online,
            "offline": offline,
            "pending": pending
        }
    })