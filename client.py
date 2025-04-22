# client.py
import asyncio
import websockets



async def connect():
    uri = "ws://192.168.1.3:8000/ws"  # use host's LAN IP
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client!")
        while True:
            msg = await websocket.recv()
            print("Received:", msg)

asyncio.run(connect())
