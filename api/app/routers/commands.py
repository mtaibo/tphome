from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Device
import mqtt

router = APIRouter(prefix="/commands/{id}", tags=["Commands"])

CMD_UP    = 0xC0
CMD_DOWN  = 0xC1
CMD_STOP  = 0xC2
CMD_PING  = 0xC3
CMD_STATE = 0xC4


def _get_device(id: str, session: Session) -> Device:
    device = session.exec(select(Device).where(Device.id == id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def _cmd(id: str, byte: int):
    mqtt.publish(f"tp/{id}/c", bytes([byte]))


@router.post("/up")
def up(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_UP)
    return {"sent": "UP", "device": id}


@router.post("/down")
def down(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_DOWN)
    return {"sent": "DOWN", "device": id}


@router.post("/stop")
def stop(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_STOP)
    return {"sent": "STOP", "device": id}


@router.post("/ping")
def ping(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_PING)
    return {"sent": "PING", "device": id}


@router.post("/state")
def state(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_STATE)
    return {"sent": "STATE", "device": id}


@router.post("/set/{value}")
def set_pos(id: str, value: int, session: Session = Depends(get_session)):
    if not (0 <= value <= 100):
        raise HTTPException(status_code=422, detail="Position must be between 0 and 100")
    _get_device(id, session)
    _cmd(id, value)
    return {"sent": "SET", "value": value, "device": id}