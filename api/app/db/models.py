from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Device(SQLModel, table=True):
    id: str = Field(primary_key=True)

    # Hardware
    mac: str
    firmware_version: Optional[str] = None

    # Connection
    online: bool = False
    last_seen: Optional[datetime] = None


class PendingDevice(SQLModel, table=True):
    mac: str = Field(primary_key=True)


class Blind(SQLModel, table=True):
    id: str = Field(foreign_key="device.id", primary_key=True)

    # Prefs
    up_time: int = 0
    down_time: int = 0
    down_pos: int = 0
    inverted_relays: bool = False

    # State
    position: int = 0
    motor_state: int = 0


class Light(SQLModel, table=True):
    id: str = Field(foreign_key="device.id", primary_key=True)
    on: bool = False