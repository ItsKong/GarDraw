import pygame, config

class DashboardUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.boxHeight = 50
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        ghost = [
    {"_id": "1", "username": "anonymous", "score": 12},
    {"_id": "2", "username": "player_1", "score": 27},
    {"_id": "3", "username": "gamerX", "score": 15},
    {"_id": "4", "username": "champion_42", "score": 32},
    {"_id": "5", "username": "shadowKnight", "score": 21},
    {"_id": "5", "username": "shadowKnight", "score": 21}
]
        self.players = ghost


        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))

    def handle_event(self, e, game_state, player_state):
        # if player_state._id not in self.players:
        #     self.players.append({
        #         '_id': player_state._id,
        #         'username': player_state.username,
        #         'score': game_state.score
        #     })
        pass

    def display(self, screen):
        self.surface.fill((0, 0, 0, 0))
        visible_rows = self.surface.get_height() // self.boxHeight
        for i, ply in enumerate(self.players[:visible_rows]):
            y = i * self.boxHeight 
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
                
            name = self.font.render(ply['username'], True, config.BLACK)
            score = self.font.render(f"{str(ply['score'])} points", True, config.BLACK)
            index = self.font.render(f"#{str(i + 1)}", True, config.BLACK)
            self.surface.blit(name, ((self.surface.get_width() - name.get_width()) // 2, y))
            self.surface.blit(score, ((self.surface.get_width() - name.get_width()) // 2, y + 20))
            self.surface.blit(index, ((5, y)))
        screen.blit(self.surface, self.rect.topleft)