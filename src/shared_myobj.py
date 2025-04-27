import time
from GameState import GameState, PlayerState
from GameSystem import ChatSystem, RoundManager
from client import manager
from db import DB

# share all obj on memory
db = DB()
game_state = GameState()
player_state = PlayerState()
roundManager = RoundManager(game_state, player_state, db)
roundManager.get_manager(manager)
chatSys = ChatSystem(game_state, player_state, db)
last_sync = time.time()
# network = WebSocketManager(game_state=game_state)