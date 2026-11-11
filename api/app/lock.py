from fastapi import HTTPException
from sqlmodel import Session, select
from db.models import Blind

CMD_SET_LOCK = 0xA6

# First firmware that understands SET_LOCK, older ones would silently ignore it
MIN_FIRMWARE = (2, 3, 0)


def supports_lock(firmware_version: str | None) -> bool:
    # Stored as the hex of each version byte, "02.03.00"
    try: return tuple(int(part, 16) for part in firmware_version.split(".")) >= MIN_FIRMWARE
    except (AttributeError, ValueError): return False


def is_locked(id: str, session: Session) -> bool:
    blind = session.exec(select(Blind).where(Blind.id == id)).first()
    return bool(blind and blind.locked)


def ensure_unlocked(id: str, session: Session):
    if is_locked(id, session):
        raise HTTPException(status_code=423, detail="Device locked by an admin")
