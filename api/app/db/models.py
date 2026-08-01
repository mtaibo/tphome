from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
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


class Config(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True) # Just 1 row

    devices: dict = Field(sa_column=Column(JSON))
    map: dict = Field(sa_column=Column(JSON))


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


class FirmwareInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    chip: str
    target: str
    version: str
    notes: str = ""
    uploaded_at: str
    active: bool = False