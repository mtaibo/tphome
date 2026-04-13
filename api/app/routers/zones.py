from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_session
from db.models import Zone
from pydantic import BaseModel

router = APIRouter(tags=["Zones"])


class ZoneCreate(BaseModel):
    code: str
    name: str


@router.get("/zones", response_model=list[Zone])
def get_zones(session: Session = Depends(get_session)):
    return session.exec(select(Zone)).all()


@router.post("/zones")
def create_zone(data: ZoneCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Zone).where(Zone.code == data.code)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Zone already exists")
    zone = Zone(code=data.code, name=data.name)
    session.add(zone)
    session.commit()
    session.refresh(zone)
    return zone


@router.put("/zones/{code}")
def update_zone(code: str, data: ZoneCreate, session: Session = Depends(get_session)):
    zone = session.exec(select(Zone).where(Zone.code == code)).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    zone.name = data.name
    session.add(zone)
    session.commit()
    session.refresh(zone)
    return zone


@router.delete("/zones/{code}")
def delete_zone(code: str, session: Session = Depends(get_session)):
    zone = session.exec(select(Zone).where(Zone.code == code)).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    session.delete(zone)
    session.commit()
    return {"deleted": code}