import pygame
import config
from Button import Button

class Dropdown(Button):
    def __init__(self, x, y, width, height, text, color, choices, **kwargs):
        super().__init__(x, y, width, height, text, color, **kwargs)
        self.choices = choices

        self._dropped = False
        self.__chosen = None

        values = choices[:] 
        self.__choices = []
        for i, txt in enumerate(choices):
            y_offset = y + (i + 1) * height # drop down
            choice = Button(x, y_offset, width, height, txt, color, **kwargs)
            self.__choices.append(choice)
    
    def draw(self, screen):
        super().draw(screen)
        # Draw the downward arrow
        arrow_color = (0, 0, 0)  # Black color for the arrow
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),  # Left point
            (self.rect.right - 10, self.rect.centery - 5),  # Right point
            (self.rect.right - 15, self.rect.centery + 5)   # Bottom center
        ]
        pygame.draw.polygon(screen, arrow_color, arrow_points)

        if self._dropped:
            for btn in self.__choices:
                btn.draw(screen)

    def handle_event(self, event):
        if self.is_clicked(event):
            self._dropped = not self._dropped
        if self._dropped:
            for btn in self.__choices:
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    not self.is_clicked(event) and not btn.is_clicked(event)):
                    self._dropped = False
                else:
                    if btn.is_clicked(event):
                        self.__chosen = btn.text
                        self.text = btn.text
                        self._dropped = False


        
