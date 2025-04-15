import pygame, config
from TextInput import TextInput
class ChatUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.chat_messages = []
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

    def draw(self, screen):
        self.surface.fill(config.WHITE)
        self.chatTextArea.draw(self.surface)
        y = self.padding
        for msg in self.chat_messages:
            msg_surface = self.font.render(f"{self.key}: {msg['anonymous']}", True, config.BLACK)
            self.surface.blit(msg_surface, (self.padding, y))
            y += self.lineHeight
        screen.blit(self.surface, self.rect.topleft)
    
    def update(self, dt):
        self.chatTextArea.update(dt)
    
    def handle_event(self, event, player_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Calculate position relative to surface
            rel_x = event.pos[0] - self.rect.x
            rel_y = event.pos[1] - self.rect.y

            # Create new adjusted event
            adjusted_event = pygame.event.Event(
                event.type,
                {
                    'pos': (rel_x, rel_y),
                    'button': getattr(event, 'button', 0)
                }
            )
            self.chatTextArea.handle_event(adjusted_event)
        if event.type == pygame.KEYDOWN:
            self.chatTextArea.handle_event(event)
            if self.chatTextArea.value:
                self.key = player_state.username
                self.chat_messages.append({self.key : self.chatTextArea.value})
                self.chatTextArea.text = ""   # Clear input text
                self.chatTextArea.value = ""  # Clear stored value
