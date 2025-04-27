# client.py
import asyncio
import websockets
import json, sys, os, uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
config.add_path()
from GameState import GameState, PlayerState

class ClientManager:
    def __init__(self, player_state: PlayerState = PlayerState()):
        self.action = 'create_room'
        self.player_state = player_state
        self.game = None
        # self.player_state.isHost = False
        # self.player_state._id = str(uuid.uuid4())
    
    def SET_PLAYER(self, obj):
        self.player_state = obj
    
    def SET_GAME(self, obj):
        self.game = obj

    def to_parsed(self):
        if self.player_state.isHost:
            parsed = {
                'action': self.get_action(),
                'player': self.player_state.to_dict(),
                'game': self.game.to_dict()
            }
        else:
            parsed = {
                'action': self.get_action(),
                'player': self.player_state.to_dict(),
            }
        print(parsed)
        return parsed
    
    def set_action(self, action: str):
        """Call this when player does something."""
        self.action = action

    def has_action(self) -> bool:
        """Check if there is any action to send."""
        return self.action is not None

    def get_action(self) -> dict:
        """Return and clear the action (after sending)."""
        action = self.action
        self.action = None
        return action

manager = ClientManager()

async def connect(player: PlayerState, ip="localhost"):
    uri = f"ws://{ip}:8000/ws"
    manager.SET_PLAYER(player)
    async with websockets.connect(uri) as websocket:
        print(await websocket.recv())
        await websocket.send(json.dumps(manager.to_parsed()))

        # Create task to listen
        listen_task = asyncio.create_task(listen_server(websocket))

        # Main sending loop
        while True:
            if manager.has_action():  # If user did something
                print("Client Sent: ", manager.player_state)
                await websocket.send(json.dumps(manager.to_parsed()))
            
            await asyncio.sleep(1)  # Very fast loop

async def listen_server(websocket):
    while True:
        try:
            state = await websocket.recv()
            game_data = json.loads(state)
            print("Client Get:", game_data)
            manager.game.to_obj(game_data['game_state'])
        except Exception as e:
            print("Listen error:", str(e))
            break


if __name__ == "__main__":
    asyncio.run(connect(player=PlayerState(), ip="localhost"))  # Change to host's IP for LAN
