from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter 
from typing import List

router = APIRouter(tags=["WebSocket"])

class ConnectionManager:

    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active[:]:
            try: await connection.send_json(message)
            except Exception: self.disconnect(connection)

manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)