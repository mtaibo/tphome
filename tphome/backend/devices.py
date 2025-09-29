# Saving modules
import os
import json

# Device defining modules
from dataclasses import dataclass, asdict
from typing import TypedDict, Literal, NotRequired


DB_PATH = 'database.json'

TYPES = Literal["light", "blind"]
ROOMS = Literal[
    'Entrada', 'Cocina', 'Salón', 'Pasillo',
    'Habitación Secundaria', 'Habitación Invitados', 'Habitación Principal',
    'Baño Medio', 'Baño Habitación Principal'

]


@dataclass
class Device(TypedDict,):
    id: int
    name: str
    room: ROOMS
    is_on: NotRequired[bool]
    position: NotRequired[int]
    type: TYPES

devices: list[Device] = [asdict(
    Device(1, 'Lámpara', 'Salón', is_on=False, type='light'),
    Device(2, 'Persiana', 'Salón', position=75, type='blind'),
)]


class Save():

    def __init__(self, path=DB_PATH):
        self.path = path