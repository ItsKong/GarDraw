# host create room
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
config.add_path()
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
from GameState import GameState
from shared_myobj import roundManager
import uvicorn, json, uuid, asyncio

app = FastAPI()

class ServerManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, dict] = {}
        self.active_GameRoom: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text("Connected!")

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            print(f"{self.active_connections[websocket]['username']} left.")
            del self.active_connections[websocket]
    
    async def send_gameState(self, gameState: GameState, websocket: WebSocket):
        await websocket.send_text(json.dumps(gameState.to_dict()))
    
    async def syncGameState(self):
        # updata game state
        print("=================syncGameState===================")
        for connection, playerData in self.active_connections.items():
            try:
                room_id = playerData.get('room_id', None)
                if room_id and room_id in self.active_GameRoom:
                    parsed = {
                        'room_id': room_id,
                        'game_state': self.active_GameRoom[room_id],
                        'player_state': playerData,
                    }
                    await connection.send_text(json.dumps(parsed))
                else:
                    print(f"Player {playerData.get('username', 'unknown')} not in a valid room.")
            except Exception as e:
                print("Parsed error:", str(e))
                await self.disconnect(connection)
            
    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            await connection.send_text(message)

    async def add_player(self, websocket: WebSocket, player_dict: dict):
        self.active_connections[websocket] = player_dict

    async def get_player(self):
        return list(self.active_connections.values())
    
    async def update_player(self, websocket, player_dict):
        if websocket in self.active_connections:
            self.active_connections[websocket] = player_dict
    
    async def update_gameState(self, websocket, gameState):
        if websocket in self.active_connections:
            self.active_GameRoom[gameState['_id']] = gameState
        await self.syncGameState()

    async def joining(self, websocket, player_dict):
        if websocket in self.active_connections:
            if player_dict['room_id'] not in self.active_GameRoom:
                self.active_GameRoom[player_dict['room_id']] = {'playerList': []}  # Just in case
            player_dict['isGuessing'] = True
            self.active_GameRoom[player_dict['room_id']]['playerList'].append(player_dict)
            await self.syncGameState()  # <== after update, sync it!
    
    async def createRoom(self, client_game: dict = None):
        for player in list(self.active_connections.values()):    
            if (player['isHost'] and player['_id'] not in list(self.active_GameRoom)):
                if client_game:
                    client_game['_id'] = str(uuid.uuid4())
                    player['room_id'] = client_game['_id'] 
                    self.active_GameRoom[client_game['_id'] ] = client_game
                else: # mostly debuggy
                    game = GameState() # server mem
                    game._id = str(uuid.uuid4())
                    player['room_id'] = game._id
                    game.currentHost = player['_id']
                    game.playerList.append(player)
                    game_dict = game.to_dict()
                    self.active_GameRoom[game._id] = game_dict
                # print("Room create! => ", client_game)

                # return game_dict['_id']

manager = ServerManager()

# print(type(game))
# print(game.to_dict())

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        # Step 1: Receive initial player info
        playerStr = await websocket.receive_text()
        playerDict = json.loads(playerStr)
        print("Server 1st get: ", playerDict)
        await manager.add_player(websocket, playerDict['player'])

        while True:
            data = await websocket.receive_text()
            try:
                data_dict = json.loads(data)
                print("Server get: ", data)
                # Optionally parse/update game state here
                await manager.update_player(websocket, data_dict['player'])
                if data_dict['action'] == 'create_room':
                    print("Creating room")
                    await manager.createRoom(data_dict['game'])

                elif data_dict['action'] == 'join_room':
                    print("Joining")
                    await manager.joining(websocket, data_dict['player'])
                
                elif data_dict['action'] == 'update':
                    print('update')
                    await manager.update_gameState(websocket, data_dict['game'])
                
                elif data_dict['action'] == 'sync':
                    print('syncimg')
                    await manager.syncGameState()
                
                # elif data_dict['action'] == 'update':
                await manager.syncGameState()

            except Exception as e:
                print("Client receive error:", str(e))
                break
            await asyncio.sleep(0.01)  # prevent tight loop

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
    # uvicorn server:app --host 0.0.0.0 --port 8000 --reload
