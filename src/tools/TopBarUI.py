import pygame, config
from Button import IconButton
from GameSystem import RandomWord

class TopBarUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.guessWordSize = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 50))
        self.roomStatus = ''
        self.hintWord = ''
        self.icon = kwargs.get('icon', {})
        self.isGuessing = True

        self.setting_btn = IconButton(x + config.CANVA_WIDTH + 275 + 220 - config.TOOLBAR_HEIGHT, 
                            y,
                            config.TOOLBAR_HEIGHT,
                            config.TOOLBAR_HEIGHT,
                            text='setting',
                            color=config.WHITE,
                            icon=self.icon['setting_icon'],
                            mode=config.SETTING)
    
    def update(self, player_state):
        self.isGuessing = player_state.isGuessing

    def display(self, screen, game_state):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.icon['clock_icon'], (0, 0))
        if game_state.rmSetting:
            waiting = self.font.render("WAITING", True, config.BLACK)
            self.surface.blit(waiting, ((self.rect.width - self.rect.x)//2, 
                                            (self.rect.y ) // 2))
            screen.blit(self.surface, self.rect.topleft)
            return
        else:
            if self.isGuessing:
                hintWord = game_state.word_hint
                hintWords = self.guessWordSize.render(hintWord, True, config.BLACK)
                self.surface.blit( hintWords, ((self.rect.width - self.rect.x)//2,
                                                (self.rect.y)//2))
            else:
                hintWord2 = game_state.word
                hintWord2s = self.guessWordSize.render(hintWord2, True, config.BLACK)
                self.surface.blit(hintWord2s, ((self.rect.width - self.rect.x)//2,
                                                (self.rect.y)//2))
        roundnn = f"Round {game_state.round} of {game_state.maxRound}"
        timer = f"Timer: {game_state.timer}"
        timerSur = self.font.render(timer, True, config.BLACK)
        roundSurface = self.font.render(roundnn, True, config.BLACK)
        self.surface.blit(roundSurface, (100, self.rect.y //2))
        self.surface.blit(timerSur, (300, self.rect.y // 2))
        screen.blit(self.surface, self.rect.topleft)
        self.setting_btn.draw(screen)
