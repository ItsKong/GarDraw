import config
import pygame
config.add_tools()
from assets import load_assets

menu_ui = None

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
    global menu_ui
    if menu_ui is None:
        menu_ui = MenuUI()

def menu_update(screen, game_state, dt):
    game_state.background = menu_ui.background

    # background logo menu_bg
    screen.blit(menu_ui.background, (0, 0))
    screen.blit(menu_ui.logo, (screen.get_width() // 2 - menu_ui.logo.get_width() // 2, 50))
    screen.blit(menu_ui.menu_background, (screen.get_width() // 2 - menu_ui.logo.get_width() // 2, 160))
    pygame.draw.rect(menu_ui.menu_background, config.RED, menu_ui.menu_background.get_rect(), border_radius=8)

    # draw input box
    pygame.draw.rect(screen, config.WHITE, menu_ui.name_input, border_radius=10)
    pygame.draw.rect(screen, config.BLACK, menu_ui.name_input, 2, border_radius=10)

    # draw input area v2
    menu_ui.name_input.draw(screen)
    menu_ui.language_btn.draw(screen)

    # draw v.2
    menu_ui.create_room_button.draw(screen)
    menu_ui.join_room_button.draw(screen)

    menu_ui.name_input.update(dt)
    

def menu_event(event, game_state, player_state):
    menu_ui.language_btn.handle_event(event)
    menu_ui.name_input.handle_event(event)
    username = menu_ui.name_input.value
    
    if username == '':
        player_state.username = 'anonymous'
    else:
        player_state.username = username

    if menu_ui.join_room_button.is_clicked(event):
        game_state.state = 'canvas'
        
