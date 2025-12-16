from csv import unregister_dialect
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


ws_router = APIRouter(
    prefix='/ws/table',
    tags=['WS']
)


class ConnectionManager:
    def __init__(self):
        self.access_connections = {}
    
    async def connect(self, websocket: WebSocket, user_id):
        await websocket.accept()

        self.access_connections[user_id] = websocket
    
    def disconnect(self, user_id):
        if user_id in self.access_connections:
            del self.access_connections[user_id]
    
    async def broadcast(self, message: str, sender_id: int):
        for user_id, ws in self.access_connections.items():
            mes = {
                'message': message,
                'is_self': sender_id == user_id
            }
            await ws.send_json(mes)


manager = ConnectionManager()


@ws_router.websocket('/{user_id}')
async def ws_endpoint(websocket: WebSocket, user_id: int, username: str):
    await manager.connect(websocket, user_id)
    await manager.broadcast(f'User({username})) {user_id} has joined', user_id)

    while True:
        try:
            data = await websocket.receive_text()
            await manager.broadcast(f'User {user_id}: {data}', user_id)
        except WebSocketDisconnect:
            manager.disconnect(user_id)
            await manager.broadcast(f'User {user_id} has left', user_id)