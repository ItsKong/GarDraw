import config
import pygame
config.add_tools()
from assets import load_assets

ui = None

class MenuUI:
    def __init__(self):
        self.menuAsset = load_assets(config.MENU)
        self.background = self.menuAsset['bg']
        self.logo = self.menuAsset['logo']
        self.create_room_button = self.menuAsset['create_room_button']
        self.join_room_button = self.menuAsset['join_room_button']
        # quit_button = menuAsset['quit_button']
        self.menu_background = self.menuAsset['menu_bg']
        self.name_input = self.menuAsset['name_input']
        self.language_btn = self.menuAsset['language_btn']
        
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
    ui.language_btn.draw(screen)

    # draw v.2
    ui.create_room_button.draw(screen)
    ui.join_room_button.draw(screen)

    ui.name_input.update(dt)
    

def menu_event(event, game_state, player_state):
    ui.language_btn.handle_event(event)
    ui.name_input.handle_event(event)
    username = ui.name_input.value
    
    if username == '':
        player_state.username = 'anonymous'
    else:
        player_state.username = username

    if ui.join_room_button.is_clicked(event):
        game_state.state = config.DRAWING
    if ui.create_room_button.is_clicked(event):
        game_state.rmSetting = True
        game_state.state = config.DRAWING
        
