from fastapi import APIRouter, Depends

from sqlmodel import Session
from sqlalchemy.orm.attributes import flag_modified

from db.database import get_session
from db.models import Config


router = APIRouter(tags=["Config"], prefix="/config")



@router.get("/devices")
def get_devices(session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    return config.devices if config else {}


@router.get("/map")
def get_map(session: Session = Depends(get_session)):
    config = session.get(Config, 1)
    return config.map if config else {}



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