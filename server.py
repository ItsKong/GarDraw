# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
# from shared import GameState
import uvicorn
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

clients: List[WebSocket] = []
game_state = GameState()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("🔌 Client connected")

    # Send full game state
    await websocket.send_text(json.dumps(game_state.to_dict()))

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg["type"] == "join":
                player = msg["player"]
                game_state.players.append(player)
            elif msg["type"] == "guess":
                print(f"Guess: {msg['text']} from {msg['player']}")

            # Broadcast updated state
            for client in clients:
                await client.send_text(json.dumps(game_state.to_dict()))

    except WebSocketDisconnect:
        clients.remove(websocket)
        print("🔌 Client disconnected")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
