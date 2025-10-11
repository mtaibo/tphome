import json
from typing import TypedDict, Literal
from dataclasses import dataclass


from data.config import config


@dataclass
class Device(TypedDict):
    id : int
    name : str
    type : Literal['Light', 'Blind']




class Storage():

    def load(self):
       with open(config.DB_PATH, 'r') as db_file:
            self.db = json.load(db_file) 

    def save(self):
        with open(config.DB_PATH, 'w') as db_file:
            json.dump(self.db, db_file)



storage = Storage()