from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Device
from pydantic import BaseModel
import struct
import mqtt
import provisioning

router = APIRouter(tags=["Admin"])

# Admin Commands
CMD_OTA       = 0xA0
CMD_REBOOT    = 0xA1
CMD_RESET_MEM = 0xA2
CMD_SET_POS   = 0xA3
CMD_SET_PREFS = 0xA4

class PrefsPayload(BaseModel):
    up_time:         int
    down_time:       int
    down_position:   int
    inverted_relays: bool


def _get_device(id: str, session: Session) -> Device:
    device = session.exec(select(Device).where(Device.id == id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def _cmd(id: str, cmd_byte: int, payload: bytes = b""):
    mqtt.publish(f"tp/{id}/a", bytes([cmd_byte]) + payload)


@router.post("/discover")
async def discover():
    await provisioning.start()
    return {"sent": "DISCOVER"}


@router.post("/admin/{id}/prefs")
def set_prefs(id: str, prefs: PrefsPayload, session: Session = Depends(get_session)):
    _get_device(id, session)
    try:
        payload = struct.pack('<HHH?',
            prefs.up_time, prefs.down_time, prefs.down_position, prefs.inverted_relays)
        _cmd(id, CMD_SET_PREFS, payload)
        return {
            "status": "admin_cmd_sent",
            "device": id,
            "bytes_sent": len(payload),
            "hex_payload": payload.hex().upper()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Packaging error: {str(e)}")


@router.post("/admin/{id}/ota")
def ota(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_OTA)
    return {"sent": "OTA", "device": id}


@router.post("/admin/{id}/reboot")
def reboot(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_REBOOT)
    return {"sent": "REBOOT", "device": id}


@router.post("/admin/{id}/reset")
def reset_mem(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_RESET_MEM)
    return {"sent": "RESET_MEM", "device": id}


@router.post("/admin/{id}/set/{value}")
def set_position(id: str, value: int, session: Session = Depends(get_session)):
    if not (0 <= value <= 10000):
        raise HTTPException(status_code=422, detail="Position must be between 0 and 10000")
    _get_device(id, session)
    _cmd(id, CMD_SET_POS, struct.pack("<H", value))
    return {"sent": "SET_POS", "value": value, "device": id}