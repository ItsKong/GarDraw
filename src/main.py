import pygame
import config

pygame.init()
pygame.font.init()

config.add_tools()
from GameState import GameState
from OneTimeCaller import OneTimeCaller
OTC = OneTimeCaller()

config.add_pages()
from menu import menu_update, init_menu_assets, menu_event
from canvas import canvas_page

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
# screenTool = Screen()
# screen = screenTool.return_RES()
pygame.display.set_caption("Drawing Game")
game_state = GameState()


running = True
while running:
    dt = pygame.time.Clock().tick(60) #delta time (in ms)

    OTC.call(lambda: init_menu_assets(screen))
    if game_state.state == config.MENU:
        menu_update(screen, game_state, dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.state == config.MENU:
            menu_event(event, game_state)
        elif game_state.state == 'canvas':
            canvas_page(screen, event, game_state)

    pygame.display.update()

pygame.quit()
