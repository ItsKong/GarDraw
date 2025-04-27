import pygame, config

class DashboardUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.boxHeight = 50
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.players= []


        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))

    def handle_event(self, e, game_state, player_state):
        self.players = game_state.playerList
        

    def display(self, screen):
        self.surface.fill((0, 0, 0, 0))
        visible_rows = self.surface.get_height() // self.boxHeight
        for i, ply in enumerate(self.players[:visible_rows]):
            y = i * self.boxHeight 
            if ply.isDrawer:
                bgColor = config.ORANGE
            else:
                bgColor = config.WHITE if i % 2 == 0 else config.GRAY

            if i == 0:
                pygame.draw.rect(self.surface, bgColor, (0, y, 
                                                     self.surface.get_width(), self.boxHeight),
                                                     border_top_left_radius=8,
                                                     border_top_right_radius=8)
            elif i == len(self.players) - 1:
                pygame.draw.rect(self.surface, bgColor, (0, y, 
                                                     self.surface.get_width(), self.boxHeight),
                                                     border_bottom_left_radius=8,
                                                     border_bottom_right_radius=8)
            else:
                pygame.draw.rect(self.surface, bgColor, (0, y, 
                                                     self.surface.get_width(),
                                                     self.boxHeight))
                
            name = self.font.render(ply.username, True, config.BLACK)
            score = self.font.render(f"{str(ply.score)} points", True, config.BLACK)
            index = self.font.render(f"#{str(i + 1)}", True, config.BLACK)
            self.surface.blit(name, ((self.surface.get_width() - name.get_width()) // 2, y))
            self.surface.blit(score, ((self.surface.get_width() - name.get_width()) // 2, y + 20))
            self.surface.blit(index, ((5, y)))
        screen.blit(self.surface, self.rect.topleft)