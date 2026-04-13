import asyncio
from datetime import datetime
from sqlmodel import Session, select
from db.database import engine
from db.models import Device, PendingDevice
from connections import manager
import mqtt

DISCOVERY_TIMEOUT = 5

_responses: set[str] = set()
_discovery_active = False


def handle_announcement(device_id: str):
    if _discovery_active:
        _responses.add(device_id)


async def start():
    global _discovery_active, _responses

    _responses = set()
    _discovery_active = True

    mqtt.publish("tp/a/c", b"\x01")
    await asyncio.sleep(DISCOVERY_TIMEOUT)

    _discovery_active = False
    await _process()


async def _process():
    online = []
    offline = []
    pending = []

    with Session(engine) as session:

        all_devices = session.exec(select(Device)).all()
        known_macs = {d.mac for d in all_devices}

        # Known devices
        for device in all_devices:

            if device.id in _responses:
                # Correct ID, set device online
                device.online = True
                device.last_seen = datetime.now()
                online.append(device.id)
                session.add(device)

            elif device.mac in _responses:
                # Device responded with its MAC, was reset, move to pending
                session.delete(device)
                existing = session.exec(
                    select(PendingDevice).where(PendingDevice.mac == device.mac)
                ).first()
                if not existing:
                    session.add(PendingDevice(mac=device.mac))
                pending.append(device.mac)

            else:
                # No response, set device offline
                device.online = False
                offline.append(device.id)
                session.add(device)

        # Unknown responses
        for device_id in _responses:
            if device_id in {d.id for d in all_devices}:
                continue
            if device_id in known_macs:
                continue

            if len(device_id) == 5:
                # Configured device not in database, add it
                session.add(Device(
                    id=device_id,
                    online=True,
                    last_seen=datetime.now()
                ))
                online.append(device_id)

            else:
                # Unknown MAC, move to pending
                existing = session.exec(
                    select(PendingDevice).where(PendingDevice.mac == device_id)
                ).first()
                if not existing:
                    session.add(PendingDevice(mac=device_id))
                pending.append(device_id)

        session.commit()

    await manager.broadcast({
        "event": "discovery_complete",
        "data": {
            "online": online,
            "offline": offline,
            "pending": pending
        }
    })