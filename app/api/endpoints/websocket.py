from fastapi import APIRouter, WebSocket, WebSocketDisconnect


ws_router = APIRouter(
    prefix='/ws/table',
    tags=['WS']
)


class ConnectionManager:
    def __init__(self):
        self.access_connections = {}
    
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()

        self.access_connections[username] = websocket
    
    def disconnect(self, username: str):
        if username in self.access_connections:
            del self.access_connections[username]
    
    async def broadcast(self, data: dict):
        for ws in self.access_connections.values():
            await ws.send_json(data)


manager = ConnectionManager()


@ws_router.websocket('/')
async def ws_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(username)
