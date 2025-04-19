import pygame, config
from TextInput import TextInput
class ChatUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.padding = 5
        self.input_height = 40
        self.max_lines = 100  # trim old messages
        self.lineHeight = 20
        self.key = ''

        self.font = pygame.font.Font(kwargs.get('font', None), kwargs.get('fontSize', 25))
        self.chatTextArea = TextInput(self.padding ,
                                height - 55,
                                width - 10,
                                40,
                                placeholder="Enter your name",
                                radius=8,
                                border_color = config.GRAY
                                )

    def draw(self, screen, game_state):
        self.surface.fill(config.WHITE)
        self.chatTextArea.draw(self.surface)
        y = self.padding
        for name, msg in game_state.chatLog:
            if name == '':
                msg_surface = self.font.render(f"{msg}", True, config.BLACK)
            else:
                msg_surface = self.font.render(f"{name}: {msg}", True, config.BLACK)
            self.surface.blit(msg_surface, (self.padding, y))
            y += self.lineHeight
        screen.blit(self.surface, self.rect.topleft)
    
    def update(self, dt):
        self.chatTextArea.update(dt)
    
    def handle_event(self, event, game_state, player_state, chatSys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            adj_e = config.relative_pos(self.rect.x, self.rect.y, event)
            self.chatTextArea.handle_event(adj_e)
        if event.type == pygame.KEYDOWN:
            self.chatTextArea.handle_event(event)
            if self.chatTextArea.value:
                msg = self.chatTextArea.value
                if player_state.isGuessing:
                    winner = chatSys.check_guess(player_state.username, msg)
                    if winner != '':
                        game_state.chatLog.append(('', winner))
                    self.chatTextArea.text = ''
                    self.chatTextArea.value = ''
                else:
                    game_state.chatLog.append((player_state.username, msg))
                    self.chatTextArea.text = ''
                    self.chatTextArea.value = ''
        elif event.type == pygame.KEYUP:
            self.chatTextArea.handle_event(event)
                    
