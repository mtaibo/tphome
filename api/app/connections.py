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


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):

    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({
                "client": client_id,
                "data": data
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"info": f"Client #{client_id} disconnected"})