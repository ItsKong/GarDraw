import pygame, pygame.scrap, time, asyncio
import config
config.add_path()
from OneTimeCaller import OneTimeCaller # type: ignore
from menu import menu_update, init_menu_assets, menu_event
from canvas import init_canva_assets, canva_update, canva_event
from shared_myobj import *
from client import connect



async def main():
    pygame.init()
    pygame.font.init()


    OTC_MENU = OneTimeCaller()
    OTC_CANVA = OneTimeCaller()
    OTC_DB = OneTimeCaller()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Drawing Game")
    pygame.scrap.init()
    pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    clock = pygame.time.Clock()
    running = True
    connect_task = asyncio.create_task(connect(player=player_state))
    manager.SET_GAME(game_state)
    while running:
        dt = clock.tick(config.FPS) #delta time (in ms) // FPS
        
        init_menu_assets()
        init_canva_assets()

        if game_state.state == config.MENU:
            menu_update(screen, game_state, dt)
        if game_state.state == config.DRAWING:
            canva_update(screen, game_state, dt, player_state)
            roundManager.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state.state == config.MENU:
                menu_event(event, game_state, player_state, db)
            elif game_state.state == config.DRAWING:
                canva_event(event, game_state, player_state, roundManager, chatSys, db, dt)

        pygame.display.update()
        await asyncio.sleep(0.01)
    connect_task.cancel()
    try:
        await connect_task
    except asyncio.CancelledError:
        print("Connect task canceled gracefully.")

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())