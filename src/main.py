import pygame
import config
import uuid
config.add_path()
from GameState import GameState, PlayerState
from OneTimeCaller import OneTimeCaller
from menu import menu_update, init_menu_assets, menu_event
from canvas import init_canva_assets, canva_update, canva_event
from GameSystem import RandomWord, RoundManager, ChatSystem

pygame.init()
pygame.font.init()

OTC_MENU = OneTimeCaller()
OTC_CANVA = OneTimeCaller()


screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Drawing Game")

game_state = GameState()
player_state = PlayerState()
randword = RandomWord(game_state)
roundManager = RoundManager(game_state, randword)
chatSys = ChatSystem(game_state, player_state)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(config.FPS) #delta time (in ms) // FPS

    OTC_MENU.call(lambda: init_menu_assets())
    OTC_CANVA.call(lambda: init_canva_assets())
    if game_state.state == config.MENU:
        menu_update(screen, game_state, dt)
    if game_state.state == config.DRAWING:
        canva_update(screen, game_state, dt)
        roundManager.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.state == config.MENU:
            menu_event(event, game_state, player_state)
        elif game_state.state == config.DRAWING:
            canva_event(event, game_state, player_state, roundManager, chatSys, randword)

    pygame.display.update()

pygame.quit()
