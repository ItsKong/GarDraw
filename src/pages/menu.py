import config
import pygame, pygame_widgets
config.add_tools()
from assets import load_assets

menuAsset = None
def init_menu_assets(screen):
    global menuAsset
    if menuAsset is None:
        menuAsset = load_assets(config.MENU)

def menu_update(screen, game_state, dt):
    background = menuAsset['bg']
    logo = menuAsset['logo']
    create_room_button = menuAsset['create_room_button']
    join_room_button = menuAsset['join_room_button']
    # quit_button = menuAsset['quit_button']
    menu_background = menuAsset['menu_bg']
    name_input = menuAsset['name_input']
    language_btn = menuAsset['language_btn']
    game_state.background = background

    # background logo menu_bg
    screen.blit(background, (0, 0))
    screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 50))
    screen.blit(menu_background,  (screen.get_width() // 2 - logo.get_width() // 2, 160))
    pygame.draw.rect(menu_background, config.RED, menu_background.get_rect(), border_radius=8)

    # draw input box
    pygame.draw.rect(screen, config.WHITE, name_input, border_radius=10)
    pygame.draw.rect(screen, config.BLACK, name_input, 2, border_radius=10)

    # draw input area v2
    name_input.draw(screen)
    language_btn.draw(screen)

    # draw v.2
    create_room_button.draw(screen)
    join_room_button.draw(screen)

    name_input.update(dt)
    

def menu_event(event, game_state):
    menu_background = menuAsset['menu_bg']
    name_input = menuAsset['name_input']
    language_btn = menuAsset['language_btn']
    create_room_button = menuAsset['create_room_button']
    join_room_button = menuAsset['join_room_button']

    language_btn.handle_event(event)
    name_input.handle_event(event)
    if join_room_button.is_clicked(event):
        game_state.state = 'canvas'
        
