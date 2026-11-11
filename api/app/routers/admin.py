from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Device, Blind
from pydantic import BaseModel
from auth import require_admin
from lock import CMD_SET_LOCK, MIN_FIRMWARE, supports_lock, is_locked, ensure_unlocked
import struct
import mqtt
import update

router = APIRouter(tags=["Admin"])

# Admin Commands
CMD_OTA       = 0xA0
CMD_REBOOT    = 0xA1
CMD_RESET_MEM = 0xA2
CMD_GET_INFO  = 0xA3
CMD_SET_POS   = 0xA4
CMD_SET_PREFS = 0xA5

class PrefsPayload(BaseModel):
    up_time:         int
    down_time:       int
    down_pos:   int
    inverted_relays: bool


def _get_device(id: str, session: Session) -> Device:
    device = session.exec(select(Device).where(Device.id == id)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


def _cmd(id: str, cmd_byte: int, payload: bytes = b""):
    mqtt.publish(f"tp/{id}/a", bytes([cmd_byte]) + payload)


@router.post("/update")
async def start_update():
    await update.start()
    return {"sent": "UPDATE"}


@router.post("/admin/{id}/prefs")
def set_prefs(id: str, prefs: PrefsPayload, session: Session = Depends(get_session)):
    _get_device(id, session)
    try:
        payload = struct.pack('<HHH?',
            prefs.up_time, prefs.down_time, prefs.down_pos, prefs.inverted_relays)
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
def ota(id: str, version: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    
    # Validate format of the version code
    parts = version.split(".")
    if len(parts) != 3: raise HTTPException(status_code=422, detail=f"Invalid version format: major.minor.patch (1.2.12)")
    major, minor, patch = [int(p) for p in parts]

    # Validate each part of the version code
    for name, value in [("major", major), ("minor", minor), ("patch", patch)]:
        if not (0 <= value <= 255): raise HTTPException(status_code=422, detail=f"Version {name} must be between 0 and 255")

    # Older firmware ignores the lock, a locked switch would come back unlocked
    if (major, minor, patch) < MIN_FIRMWARE and is_locked(id, session):
        raise HTTPException(status_code=423, detail="Device locked by an admin, older firmware can't keep the lock")

    # Pack every part of the version code as three unsigned int bytes
    payload = struct.pack("BBB", major, minor, patch)
    _cmd(id, CMD_OTA, payload)
    
    return {"sent": "OTA", "device": id, "version": f"{major}.{minor}.{patch}"}


@router.post("/admin/{id}/info")
def info(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_GET_INFO)
    return {"sent": "INFO", "device": id}


@router.post("/admin/{id}/reboot")
def reboot(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    _cmd(id, CMD_REBOOT)
    return {"sent": "REBOOT", "device": id}


@router.post("/admin/{id}/reset")
def reset_mem(id: str, session: Session = Depends(get_session)):
    _get_device(id, session)
    ensure_unlocked(id, session) # Wiping the switch would also clear its lock
    _cmd(id, CMD_RESET_MEM)
    return {"sent": "RESET_MEM", "device": id}


@router.post("/admin/{id}/set/{value}")
def set_position(id: str, value: int, session: Session = Depends(get_session)):
    if not (0 <= value <= 10000):
        raise HTTPException(status_code=422, detail="Position must be between 0 and 10000")
    _get_device(id, session)
    _cmd(id, CMD_SET_POS, struct.pack("<H", value))
    return {"sent": "SET_POS", "value": value, "device": id}


def _set_lock(id: str, locked: bool, session: Session):
    device = _get_device(id, session)
    blind = session.exec(select(Blind).where(Blind.id == id)).first()
    if not blind:
        raise HTTPException(status_code=422, detail="Only blinds can be locked")
    if not supports_lock(device.firmware_version):
        raise HTTPException(status_code=409, detail=f"Firmware {device.firmware_version} doesn't support the lock, update it to 2.3.0 or later and refresh its info")

    blind.locked = locked
    session.add(blind)
    session.commit()

    # The switch answers with its info, which confirms the lock (see mqtt._update_device_info)
    _cmd(id, CMD_SET_LOCK, bytes([1 if locked else 0]))
    mqtt.push_lock(id, locked, confirmed=False)
    return {"sent": "LOCK" if locked else "UNLOCK", "device": id, "online": device.online}


@router.post("/admin/{id}/lock")
def lock(id: str, session: Session = Depends(get_session), admin: dict = Depends(require_admin)):
    return _set_lock(id, True, session)


@router.post("/admin/{id}/unlock")
def unlock(id: str, session: Session = Depends(get_session), admin: dict = Depends(require_admin)):
    return _set_lock(id, False, session)
