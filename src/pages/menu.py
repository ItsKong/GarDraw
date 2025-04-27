import config
import pygame, uuid, asyncio
config.add_path()
from client import connect
from assets import load_assets
from shared_myobj import manager
ui = None

class MenuUI:
    def __init__(self):
        menuAsset = load_assets(config.MENU)
        self.background = menuAsset['bg']
        self.logo = menuAsset['logo']
        self.create_room_button = menuAsset['create_room_button']
        self.join_room_button = menuAsset['join_room_button']
        # quit_button = menuAsset['quit_button']
        self.menu_background = menuAsset['menu_bg']
        self.name_input = menuAsset['name_input']
        self.language_btn = menuAsset['language_btn']
        self.room_id_input = menuAsset['room_id_input']
        
def init_menu_assets():
    global ui
    if ui is None:
        ui = MenuUI()

def menu_update(screen, game_state, dt):
    game_state.background = ui.background

    # background logo menu_bg
    screen.blit(ui.background, (0, 0))
    screen.blit(ui.logo, (screen.get_width() // 2 - ui.logo.get_width() // 2, 50))
    screen.blit(ui.menu_background, (screen.get_width() // 2 - ui.logo.get_width() // 2, 160))
    pygame.draw.rect(ui.menu_background, config.RED, ui.menu_background.get_rect(), border_radius=8)

    # draw input box
    pygame.draw.rect(screen, config.WHITE, ui.name_input, border_radius=10)
    pygame.draw.rect(screen, config.BLACK, ui.name_input, 2, border_radius=10)

    # draw input area v2
    ui.name_input.draw(screen)
    # ui.language_btn.draw(screen)
    ui.room_id_input.draw(screen)

    # draw v.2
    ui.create_room_button.draw(screen)
    ui.join_room_button.draw(screen)

    ui.name_input.update(dt)
    ui.room_id_input.update(dt)

def SET_player_data (username, player_state):
    if username == '':
        player_state.username = 'anonymous'
        player_state._id = str(uuid.uuid4())
    else:
        player_state.username = username
        player_state._id = str(uuid.uuid4())
    

def menu_event(event, game_state, player_state, db):
    # ui.language_btn.handle_event(event)
    ui.name_input.handle_event(event)
    ui.room_id_input.handle_event(event)
    username = ui.name_input.value

    if ui.join_room_button.is_clicked(event):
        # get room id and add player to room game state in db
        # gameState => host 
        # get random _id gameState then pull by _id
        # append local player => game_state.update_to()
        SET_player_data(username, player_state)
        rmid = ui.room_id_input.value if ui.room_id_input.value != '' else None
        manager.set_action('join_room', custom=rmid)
        # joined = game_state.join_game(player_state, db, rmid)
        # if joined:
        #     print(game_state.playerList)
        #     game_state.state = config.DRAWING
        # else:
        #     return

    if ui.create_room_button.is_clicked(event):
        SET_player_data(username, player_state)
        # manager.SET_PLAYER(player_state)
        player_state.isHost = True
        game_state.playerList.append(player_state)
        game_state.currentDrawer = player_state._id # shoulde be _id
        game_state.currentHost = player_state._id
        game_state.rmSetting = True
        game_state.state = config.DRAWING
        # print(id(player_state))
        # print(id(manager.player_state))
        manager.set_action('create_room')
        # db.insert_to(game_state)  
        # asyncio.create_task(connect(player_state, 'localhost'))
        
