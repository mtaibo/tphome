from pathlib import Path


class Config:

    def __init__(self):
        self.app_name = "tphome"
        self.debug = True
        self.ROOT_PATH = Path(__file__).resolve().parents[1]
        self.DB_PATH = self.ROOT_PATH / 'data' / 'database.json'


config = Config()