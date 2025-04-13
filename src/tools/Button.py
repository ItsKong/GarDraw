import pygame
import config


class Button:
    def __init__(self, x, y, width, height, text, color, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.text = text
        self.color = color

        # Optional kwargs with defaults
        self.bd_color = kwargs.get("bd_color", config.BLACK)
        self.bg_color = kwargs.get("bg_color", config.GRAY)
        self.hoverColor = kwargs.get("hoverColor", color)
        self.text_color = kwargs.get("text_color", config.WHITE)
        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.border_radius = kwargs.get("border_radius", -1)
        self.bdRadiusLT = kwargs.get("bdRadiusLT", -1)
        self.bdRadiusRT = kwargs.get("bdRadiusRT", -1)
        self.bdRadiusLB = kwargs.get("bdRadiusLB", -1)
        self.bdRadiusRB = kwargs.get("bdRadiusRB", -1)
        self.border_width = kwargs.get("border_width", -1)
        self.icon = kwargs.get("icon", None)
        self.button_type = kwargs.get("button_type", None)
        self.brushSize = kwargs.get("brushSize", None)
        self.mode = kwargs.get("mode", None)
        self.modeColor = kwargs.get("modeColor", None)

        self.selected = False
        self.brushDotColor = config.BLACK
        self.brushSelectedColor = config.WHITE

    def draw(self, screen):
        # Button color changes on hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        if self.icon:
            pygame.draw.rect(screen, self.modeColor if self.selected else self.bg_color, self.rect)
            pygame.draw.rect(screen, self.bd_color, self.rect, self.border_width) # border
            screen.blit(self.icon, (self.x() + 2, self.y() + 2))

        elif self.button_type == 'color':
            # for color butt
            pygame.draw.rect(screen, self.color, self.rect) # inside
            pygame.draw.rect(screen, self.modeColor if self.selected else self.bd_color, self.rect, self.border_width)

        elif self.button_type == 'brush':
            # for brush size butt
            pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
            pygame.draw.rect(screen, self.bd_color, self.rect, 1, border_radius=5)
            if self.selected:
                pygame.draw.rect(screen, self.modeColor, self.rect.inflate(4, 4), 2, border_radius=7)
            dot_color = self.brushDotColor 
            dot_size = (
                    self.brushSize
                    if self.brushSize < self.width - 10
                    else self.width  - 10
                )
            pygame.draw.circle(screen, dot_color, self.rect.center, dot_size // 2)
            pygame.draw.circle(screen, config.BLACK, self.rect.center, dot_size // 2, 1)

        else:
            # Draw text
            pygame.draw.rect(screen, self.hoverColor if is_hovered else self.color, self.rect, border_radius= self.border_radius)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def self_selected(self, game_state, color):
        if game_state.tool_mode == self.mode:
            self.modeColor = color
            self.selected = True

        elif game_state.current_color == self.mode:
            self.modeColor = color
            self.selected = True

        elif game_state.brushSize == self.brushSize:
            self.modeColor = color
            self.selected = True
        else:
            self.selected = False
    
    def x(self):
        return self.rect.x
    def y(self):
        return self.rect.y
