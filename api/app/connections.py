from fastapi.websockets import WebSocket
from typing import List

class ConnectionManager:

    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active:
            await connection.send_json(message)

manager = ConnectionManager()