# host create room
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
config.add_path()
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from GameState import GameState
import uvicorn, json

app = FastAPI()

class ServerManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_gameState(self, gameState: GameState, websocket: WebSocket):
        await websocket.send_text(json.dumps(gameState.to_dict()))
    
    async def broadcast(self, gameState: GameState):
        # updata game state
        for connection in self.active_connections:
            await connection.send_text(json.dumps(gameState.to_dict()))

manager = ServerManager()
game = GameState()

print(type(game))
print(game.to_dict())
@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    username = await websocket.receive_text()
    print(f"{username} joined!")
    
    await manager.send_gameState(game, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Clinet {username}, GET: {data}")
            await manager.broadcast(game)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left!")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
    # uvicorn server:app --host 0.0.0.0 --port 8000 --reload
