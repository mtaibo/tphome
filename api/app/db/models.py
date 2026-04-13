from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Zone(SQLModel, table=True):
    code: str = Field(primary_key=True)
    name: str


class Device(SQLModel, table=True):
    id: str = Field(primary_key=True)
    mac: str
    name: str
    type: str
    zone: str = Field(foreign_key="zone.code")

    online: bool = False
    last_seen: Optional[datetime] = None
    firmware: Optional[str] = None


class Blind(SQLModel, table=True):
    device_id: str = Field(foreign_key="device.id", primary_key=True)
    position: int = 0       # 0-100
    motor_state: int = 0    # 0=IDLE 1=WAITING 2=MOVING 3=STOPPING


class Light(SQLModel, table=True):
    device_id: str = Field(foreign_key="device.id", primary_key=True)
    on: bool = False