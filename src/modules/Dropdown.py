import pygame
import config
from Button import Button, TextButton

class Dropdown(Button):
    def __init__(self, x, y, width, height, choices, **kwargs):
        super().__init__(x, y, width, height, text=choices[0], **kwargs)
        self.choices = choices[:]
        self._dropped = False
        self.__choices = []
        self.kwargs = kwargs
        self.__build_choices()

        values = choices[:] 

    def __build_choices(self):
        self.__choices = []
        total = len(self.choices[1:])
        for i, choice  in enumerate(self.choices[1:]):
            y_offset = self.rect.y + (i + 1) * self.rect.height
            # Copy kwargs so we can safely modify it per-button
            button_kwargs = self.kwargs.copy()
            button_kwargs.pop('radius', None)

            if i == total - 1:
                button_kwargs["bdRadiusLB"] = 8
                button_kwargs["bdRadiusRB"] = 8
                button_kwargs.pop("radius", None)

            btn = TextButton(
                self.rect.x,
                y_offset,
                self.rect.width,
                self.rect.height,
                text=choice,
                **button_kwargs
            )
            self.__choices.append(btn)

    def draw(self, screen):
        is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        # Draw main (default) button
        if self._dropped:
            # Custom top-only radius when opened
            pygame.draw.rect(
                screen,
                self.hoverColor if is_hovered else self.color,
                self.rect,
                border_top_left_radius=8,
                border_top_right_radius=8,
                border_bottom_left_radius=0,
                border_bottom_right_radius=0
            )
        else:
            # Normal full border radius when not dropped
            pygame.draw.rect(
                screen,
                self.hoverColor if is_hovered else self.color,
                self.rect,
                border_radius=self.border_radius
            )

        # Draw main text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        if self._dropped:
            for btn in self.__choices:
                btn.draw(screen)

    def handle_event(self, event):
        if self.is_clicked(event):
            self._dropped = not self._dropped
        if self._dropped:
            for i, btn in enumerate(self.__choices):
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    not self.is_clicked(event) and not btn.is_clicked(event)):
                    self._dropped = False
                else:
                    if btn.is_clicked(event):
                        clicked_text = btn.text
                        self.choices[0], self.choices[i + 1] = self.choices[i + 1], self.choices[0]
                        self.text = self.choices[0]  # update main button text
                        self._dropped = False
                        self.__build_choices()
                        break


        
