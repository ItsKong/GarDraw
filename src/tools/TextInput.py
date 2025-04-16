import pygame

class TextInput:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.value = ''
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_position = len(self.text)
        self.cursor_interval = 500  # milliseconds
        self.backspace_held = False
        self.backspace_timer = 0
        self.backspace_delay = 400   # initial delay before repeat (ms)
        self.backspace_repeat = 50   # speed of repeat (ms)

        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.color = kwargs.get("bg_color", (255, 255, 255))
        self.placeholder = kwargs.get("placeholder", "")
        self.text_color = kwargs.get("text_color", (0, 0, 0))
        self.active = kwargs.get("active", False)
        self.border_radius = kwargs.get("radius", 0)
        self.border_color = kwargs.get("border_color", None)

    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        # Handle backspace hold
        if self.backspace_held:
            self.backspace_timer += dt
            if self.backspace_timer >= self.backspace_delay:
                # Repeat delete every backspace_repeat interval
                self.backspace_timer -= self.backspace_repeat
                self.text = self.text[:-1]


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                self.value = self.text
                # self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.backspace_held = True
                self.backspace_timer = 0  # reset repeat timer
            else:
                self.text += event.unicode
        else:
            self.backspace_held = False


    def draw(self, surface):
        # Draw box
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
        if self.border_color != None:
            pygame.draw.rect(surface, self.border_color, self.rect, 2, self.border_radius)

        # Determine what to display
        display_text = self.text if self.text or self.active else self.placeholder
        color = self.text_color if self.text or self.active else (150, 150, 150)

        # Render and draw text
        text_surf = self.font.render(display_text, True, color)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))
         # Draw cursor
        if self.active and self.cursor_visible:
            text_width = text_surf.get_width()
            cursor_x = self.rect.x + 10 + text_width
            cursor_y = self.rect.y + 10
            cursor_height = text_surf.get_height()
            pygame.draw.line(surface, self.text_color, 
                             (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
    
    def x(self):
        return self.rect.x
    def y(self):
        return self.rect.y
