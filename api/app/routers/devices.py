from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Device, Blind, Light, PendingDevice
from pydantic import BaseModel
from admin import reset_mem
import mqtt

router = APIRouter(tags=["Devices"])


# MODELS


class Response(BaseModel):
    id: str
    hardware: dict
    connection: dict
    prefs: dict
    state: dict


class Update(BaseModel):
    prefs: dict


class ConfigureDevice(BaseModel):
    mac: str
    name: str
    zone: str
    type: str


# AUX FUNCTIONS


def _get_device(id: str, session: Session) -> Device:
    device = session.exec(select(Device).where(Device.id == id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def _build_response(device: Device, session: Session) -> Response:

    if device.id[0] == "B":
        blind = session.exec(select(Blind).where(Blind.id == device.id)).first()
        if blind:
            state = {"position": blind.position, "motor_state": blind.motor_state}
            prefs = {"up_time": blind.up_time, "down_time": blind.down_time,
                     "down_pos": blind.down_pos, "inverted_relays": blind.inverted_relays}
        else: return f"Device {device.id} not found on blinds database table"

    elif device.id[0] == "L":
        light = session.exec(select(Light).where(Light.id == device.id)).first()
        if light:
            state = {"on": light.on}

    return Response(
        id=device.id,
        hardware={
            "mac" : device.mac,
            "firmware_version" : device.firmware_version
        },
        connection={
            "online" : device.online,
            "last_seen" : str(device.last_seen)
        },
        prefs=prefs,
        state=state
    )


def _encode_device_id(id: str) -> bytes:
    type = id[0]
    zone = int(id[1:3])
    device = int(id[3:5])
    return bytes([ord(type), zone, device])


# DB DEVICES ROUTES


@router.get("/devices", response_model=list[Response])
def get_devices(session: Session = Depends(get_session)):
    devices = session.exec(select(Device)).all()
    return [_build_response(device, session) for device in devices]


@router.get("/devices/{id}", response_model=Response)
def get_device(id: str, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    return _build_response(device, session)


@router.put("/devices/{id}")
def update_device(id: str, data: Update, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    device.prefs = data.prefs
    session.add(device)
    session.commit()
    session.refresh(device)
    return _build_response(device, session)


@router.delete("/devices/{id}")
def delete_device(id: str, session: Session = Depends(get_session)):
    device = _get_device(id, session)
    reset_mem(id, session)
    session.delete(device)
    session.commit()
    return {"deleted": id}


# DB PROVISIONING DEVICES ROUTES


@router.get("/devices/pending", response_model=list[str])
def get_pending(session: Session = Depends(get_session)):
    pending = session.exec(select(PendingDevice)).all()
    return [pending_device.mac for pending_device in pending]


@router.post("/devices/pending/configure")
def configure_device(data: ConfigureDevice, session: Session = Depends(get_session)):

    pending = session.exec(
        select(PendingDevice).where(PendingDevice.mac == data.mac)
    ).first()
    if not pending:
        raise HTTPException(status_code=404, detail="Pending device not found")

    # Build new device ID
    new_id = None

    # Send new ID to device via MQTT
    mqtt.publish(f"def/{data.mac}/a", _encode_device_id(new_id))

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
        session.add(Blind(id=new_id))
    elif data.type == "L":
        session.add(Light(id=new_id))

    # Remove from pending
    session.delete(pending)
    session.commit()

    return {"configured": new_id}