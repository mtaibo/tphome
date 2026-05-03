from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


'''
{
    "id": "B0101",

    "hardware": {
        "mac": "20:40",
        "firmware_version": "3f.68.af"
    },

    "connection": {
        "online": true,
        "last_seen": "2026-04-29T16:40:11.675639Z"
    },

    "prefs": {
        "up_time": 5242,
        "down_time": 42926,
        "down_pos": 61008,
        "inverted_relays": true
    },

    "state": {
        "position": 100,
        "motor_state": 0
    }
}
'''

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
    up_time: int = Field(default=0)
    down_time: int = Field(default=0)
    down_pos: int = Field(default=0)
    inverted_relays: bool = Field(default=False)

    # State
    position: int = 0
    motor_state: int = 0


class Light(SQLModel, table=True):
    id: str = Field(foreign_key="device.id", primary_key=True)
    on: bool = False