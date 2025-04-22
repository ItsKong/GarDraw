import pygame, pygame.scrap, time
import config
config.add_path()
from GameState import GameState, PlayerState
from OneTimeCaller import OneTimeCaller
from menu import menu_update, init_menu_assets, menu_event
from canvas import init_canva_assets, canva_update, canva_event
from GameSystem import RoundManager, ChatSystem
from db import DB

pygame.init()
pygame.font.init()


OTC_MENU = OneTimeCaller()
OTC_CANVA = OneTimeCaller()
OTC_DB = OneTimeCaller()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Drawing Game")
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

db = DB()
game_state = GameState()
player_state = PlayerState()
roundManager = RoundManager(game_state, player_state, db)
chatSys = ChatSystem(game_state, player_state, db)
last_sync = time.time()

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(config.FPS) #delta time (in ms) // FPS

    init_menu_assets()
    init_canva_assets()

    if game_state.state == config.MENU:
        menu_update(screen, game_state, dt)
    if game_state.state == config.DRAWING:
        canva_update(screen, game_state, dt, player_state)
        roundManager.update()
        if time.time() - last_sync > 0.5:  # sync every 0.5 sec
            game_state.sync_gameState_local(db)
            last_sync = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.state == config.MENU:
            menu_event(event, game_state, player_state, db)
        elif game_state.state == config.DRAWING:
            canva_event(event, game_state, player_state, roundManager, chatSys, db)

    pygame.display.update()

pygame.quit()
