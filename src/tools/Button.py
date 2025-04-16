import pygame
import config


class Button:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width

        # Optional kwargs with defaults
        self.text = kwargs.get("text", '')
        self.color = kwargs.get("color", config.WHITE)
        self.bd_color = kwargs.get("bd_color", config.BLACK)
        self.bg_color = kwargs.get("bg_color", config.GRAY)
        self.hoverColor = kwargs.get("hoverColor", self.color)
        self.text_color = kwargs.get("text_color", config.WHITE)
        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.border_radius = kwargs.get("radius", 0)
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
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

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

class IconButton(Button):
    def __init__(self, x, y, width, height, icon, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.icon = icon
        self.modeColor = kwargs.get("mode_color", config.GREEN)

    def draw(self, screen):
        color = self.modeColor if self.selected else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.bd_color, self.rect, self.border_width)
        screen.blit(self.icon, (self.rect.x + 2, self.rect.y + 2))

        
class ColorButton(Button):
    def __init__(self, x, y, width, height, color, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.color = color
        self.modeColor = kwargs.get("mode_color", config.GREEN)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        border_col = self.modeColor if self.selected else self.bd_color
        pygame.draw.rect(screen, border_col, self.rect, self.border_width)

class BrushButton(Button):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self.brushDotColor = kwargs.get("dot_color", config.BLACK)
        self.modeColor = kwargs.get("mode_color", config.WHITE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.bd_color, self.rect, 1, border_radius=5)

        if self.selected:
            pygame.draw.rect(screen, self.modeColor, self.rect.inflate(4, 4), 2, border_radius=7)

        dot_size = min(self.brushSize, self.rect.width - 10)
        pygame.draw.circle(screen, self.brushDotColor, self.rect.center, dot_size // 2)
        pygame.draw.circle(screen, config.BLACK, self.rect.center, dot_size // 2, 1)

class TextButton(Button):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, **kwargs)

    def draw(self, screen):
        color = self.hoverColor if self.is_hovered() else self.color

        if any(r > 0 for r in [self.bdRadiusLT, self.bdRadiusRT, self.bdRadiusLB, self.bdRadiusRB]):
            pygame.draw.rect(screen, color, self.rect,
                border_top_left_radius=self.bdRadiusLT,
                border_top_right_radius=self.bdRadiusRT,
                border_bottom_left_radius=self.bdRadiusLB,
                border_bottom_right_radius=self.bdRadiusRB)
        else:
            pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)