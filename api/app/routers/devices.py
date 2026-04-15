from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Device, Blind, Light, PendingDevice
from pydantic import BaseModel
import mqtt

router = APIRouter(tags=["Devices"])


# Models

class DeviceResponse(BaseModel):
    id: str
    mac: str
    name: str
    type: str
    zone: str
    online: bool
    last_seen: str | None
    firmware: str | None
    state: dict | None = None


class DeviceUpdate(BaseModel):
    name: str
    zone: str


class ConfigureDevice(BaseModel):
    mac: str
    name: str
    zone: str
    type: str


# Aux functions

def _get_device(id: str, session: Session) -> Device:
    device = session.exec(select(Device).where(Device.id == id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def _build_response(device: Device, session: Session) -> DeviceResponse:
    state = None

    if device.type == "B":
        blind = session.exec(select(Blind).where(Blind.device_id == device.id)).first()
        if blind:
            state = {"position": blind.position, "motor_state": blind.motor_state}

    elif device.type == "L":
        light = session.exec(select(Light).where(Light.device_id == device.id)).first()
        if light:
            state = {"on": light.on}

    return DeviceResponse(
        id=device.id,
        mac=device.mac,
        name=device.name,
        type=device.type,
        zone=device.zone,
        online=device.online,
        last_seen=str(device.last_seen) if device.last_seen else None,
        firmware=device.firmware,
        state=state
    )


def _next_device_id(type: str, zone: str, session: Session) -> str:
    existing = session.exec(
        select(Device).where(Device.type == type, Device.zone == zone)
    ).all()
    number = len(existing) + 1
    return f"{type}{zone}{number:02d}"


# Routes

@router.get("/devices", response_model=list[DeviceResponse])
def get_devices(session: Session = Depends(get_session)):
    devices = session.exec(select(Device)).all()
    return [_build_response(d, session) for d in devices]


@router.get("/devices/pending", response_model=list[str])
def get_pending(session: Session = Depends(get_session)):
    pending = session.exec(select(PendingDevice)).all()
    return [p.id for p in pending]


@router.post("/devices/pending/configure")
def configure_device(data: ConfigureDevice, session: Session = Depends(get_session)):

    pending = session.exec(
        select(PendingDevice).where(PendingDevice.mac == data.mac)
    ).first()
    if not pending:
        raise HTTPException(status_code=404, detail="Pending device not found")

    # Build new device ID
    new_id = _next_device_id(data.type, data.zone, session)

    # Send new ID to device via MQTT
    mqtt.publish(f"def/{data.mac}/a", new_id.encode())

    # Create Device
    device = Device(
        id=new_id,
        mac=data.mac,
        name=data.name,
        type=data.type,
        zone=data.zone,
        online=False
    )
    session.add(device)

    if data.type == "B":
        session.add(Blind(device_id=new_id))
    elif data.type == "L":
        session.add(Light(device_id=new_id))

    # Remove from pending
    session.delete(pending)
    session.commit()

    return {"configured": new_id}


@router.get("/devices/{id}", response_model=DeviceResponse)
def get_device(id: str, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    return _build_response(device, session)


@router.put("/devices/{id}")
def update_device(id: str, data: DeviceUpdate, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    device.name = data.name
    device.zone = data.zone
    session.add(device)
    session.commit()
    session.refresh(device)
    return _build_response(device, session)


@router.delete("/devices/{id}")
def delete_device(id: str, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    session.delete(device)
    session.commit()
    return {"deleted": id}