import pygame
import config

config.add_tools()
from assets import load_assets
from GameState import GameState

pygame.init()
pygame.font.init()
config.add_pages()
from menu import menu_page
from canvas import canvas_page

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
# screenTool = Screen()
# screen = screenTool.return_RES()
pygame.display.set_caption("Drawing Game")
game_state = GameState()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.VIDEORESIZE:
        #     width, height = event.w, event.h
            # config.WIDTH = width
            # config.HEIGHT = height
            # screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
        if game_state.state == 'menu':
            menu_page(screen, event, game_state)
        elif game_state.state == 'canvas':
            canvas_page(screen, event, game_state)

    pygame.display.update()

pygame.quit()
