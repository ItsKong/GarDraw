import pygame

class TextInput:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        
        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.color = kwargs.get("bg_color", (255, 255, 255))
        self.text = ""
        self.placeholder = kwargs.get("placeholder", "")
        self.text_color = kwargs.get("text_color", (0, 0, 0))
        self.active = kwargs.get("active", False)
        self.border_radius = kwargs.get("radius", 0)
        self.border_color = kwargs.get("border_color", None)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

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
    
    def x(self):
        return self.rect.x
    def y(self):
        return self.rect.y
