from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from sqlalchemy.orm.attributes import flag_modified

from db.database import get_session
from db.models import Config


router = APIRouter(tags=["Config"], prefix="/config")


METADATA = {
    "blinds": {
        "prefs": {
            "up_time":         { "label": "Tiempo de subida",   "type": "time" },
            "down_time":       { "label": "Tiempo de bajada",   "type": "time" },
            "down_pos":        { "label": "Posición de bajada", "type": "percent" },
            "inverted_relays": { "label": "Invertir relés",     "type": "boolean" },
        },
        "map": {
            "x":      { "label": "X" },
            "y":      { "label": "Y" },
            "width":  { "label": "Ancho" },
            "height": { "label": "Alto" },
        }
    }
}


@router.get("/metadata")
def get_metadata():
    return METADATA


@router.get("/devices")
def get_devices(session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    return config.devices if config else {}


@router.get("/map")
def get_map(session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    return config.map if config else {}


@router.patch("/devices/{device_id}/prefs")
def patch_device_prefs(device_id: str, data: dict, session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    for category in config.devices.values():
        if device_id in category:
            category[device_id]["prefs"] = data
            flag_modified(config, "devices")
            session.add(config)
            session.commit()
            return {"updated": device_id, "prefs": data}
    raise HTTPException(status_code=404, detail=f"Device {device_id} not found in config")


@router.patch("/devices/{device_id}/map")
def patch_device_map(device_id: str, data: dict, session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    for category in config.devices.values():
        if device_id in category:
            category[device_id]["map"] = data
            flag_modified(config, "devices")
            session.add(config)
            session.commit()
            return {"updated": device_id, "map": data}
    raise HTTPException(status_code=404, detail=f"Device {device_id} not found in config")


@router.put("/devices")
def update_devices(data: dict, session: Session = Depends(get_session)):
    config = session.get(Config, 1)

    if not config: config = Config(id=1, devices=data, map={})
    else:
        config.devices = data
        flag_modified(config, "devices")

    session.add(config)
    session.commit()
    session.refresh(config)
    return config.devices


@router.put("/map")
def update_map(data: dict, session: Session = Depends(get_session)):
    config = session.get(Config, 1)

    if not config: config = Config(id=1, devices={}, map=data)
    else:
        config.map = data
        flag_modified(config, "map")

    session.add(config)
    session.commit()
    session.refresh(config)
    return config.map