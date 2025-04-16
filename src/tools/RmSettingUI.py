import pygame, config
from Button import Button
from TextInput import TextInput

class RmSettingUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.maxPLayer = 0
        self.drawTime = 60
        self.maxRounds = 3
        self.wordcount = 3
        self.baseH = 20
        self.customWord = ''

        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.start = Button(5, height - 55, (width // 2) + 150, 50,
                            text='Start', color=config.GREEN)
        self.textArea = TextInput(5, (height//2) - 50, width - 10, (height//2) - 50)

    def handle_event(self, e, game_state):
        if e.type == pygame.MOUSEBUTTONDOWN:
            adj_e = config.relative_pos(self.rect.x, self.rect.y, e)
            if self.start.is_clicked(adj_e):                
                game_state.rmSetting = False
            self.textArea.handle_event(adj_e)
        if e.type == pygame.KEYDOWN:
            self.textArea.handle_event(e)
            if self.textArea.value:
                self.customWord = self.textArea.value

    def display(self, screen, dt):
        self.surface.fill(config.GRAY)
        maxPlayer = self.font.render("Max player", True, config.WHITE)
        drawTime = self.font.render("Draw time", True, config.WHITE)
        maxRounds = self.font.render("Max rounds", True, config.WHITE)
        wordCount = self.font.render("Word count", True, config.WHITE)
        self.start.draw(self.surface)
        self.textArea.draw(self.surface)
        self.textArea.update(dt)
        self.surface.blit(maxPlayer, (30, self.baseH))
        self.surface.blit(drawTime, (30, self.baseH + 40))
        self.surface.blit(maxRounds, (30, self.baseH + 80))
        self.surface.blit(wordCount, (30, self.baseH + 120))
        screen.blit(self.surface, (self.rect.x, self.rect.y))