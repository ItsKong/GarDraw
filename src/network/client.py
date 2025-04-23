# client.py
import asyncio
import websockets
import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
config.add_path()
from GameState import GameState

async def connect(username, ip="localhost"):
    uri = f"ws://{ip}:8000/ws/123"
    async with websockets.connect(uri) as websocket:
        # Send join event
        await websocket.send(username)

        while True:
            state = await websocket.recv()
            try:
                game_data = json.loads(state)
                print(f"Client: {username}, GET: {game_data}")
                await websocket.send(json.dumps(game_data))
            except json.JSONDecodeError:
                print("Not JSON:", state)
            await asyncio.sleep(1)

if __name__ == "__main__":
    name = input("Enter your name: ")
    asyncio.run(connect(name, "localhost"))  # Change to host's IP for LAN
