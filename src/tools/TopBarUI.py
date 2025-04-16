import pygame, config
from Button import IconButton

class TopBarUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 20))

        self.icon = kwargs.get('icon', {})

        self.setting_btn = IconButton(x + config.CANVA_WIDTH + 275 + 220 - config.TOOLBAR_HEIGHT, 
                            y,
                            config.TOOLBAR_HEIGHT,
                            config.TOOLBAR_HEIGHT,
                            text='setting',
                            color=config.WHITE,
                            icon=self.icon['setting_icon'],
                            mode=config.SETTING)
    def handle_event(self, e):
        pass

    def display(self, screen, game_state):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.icon['clock_icon'], (0, 0))
        phase = game_state.phase
        phaseSurface = self.font.render(phase, True, config.BLACK)
        if phase == config.WAITING:
            self.surface.blit(phaseSurface, ((self.rect.width - self.rect.x)//2, 
                                            self.rect.y // 2))
        elif phase == config.GUESSING:
            word = game_state.word
            word = self.font.render(word, True, config.BLACK)
            self.surface.blit(phaseSurface, ((self.rect.width - self.rect.x)//2, 
                                            2))
            self.surface.blit(word, ((self.rect.width - self.rect.x)//2,
                                            self.rect.y - 2))
        roundnn = f"Round {game_state.round} of {game_state.maxRound}"
        roundSurface = self.font.render(roundnn, True, config.BLACK)
        self.surface.blit(roundSurface, (100, self.rect.y //2))
        screen.blit(self.surface, self.rect.topleft)
        self.setting_btn.draw(screen)
