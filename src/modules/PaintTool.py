import pygame
import config

class PenTool():
    def __init__(self, surface, color=config.BLACK, size=config.BRUSH_SIZES[0]):
        self.color = color
        self.colorTemp = self.color
        self.size = size
        self.surface = surface
        self.drawing = False
        self.current_pos = None
        self.last_pos = None
        self.eraser = False
    
    def use(self):
        if self.eraser:
            self.color = config.WHITE
        else:
            self.color = self.colorTemp

        dx = self.last_pos[0] - self.current_pos[0]
        dy = self.last_pos[1] - self.current_pos[1]
        distance = max(1, int((dx**2 + dy**2) ** 0.5))
        steps = max(1, distance // (self.size // 3))
        for i in range(steps + 1):
            t = i / steps
            x = int(self.current_pos[0] + dx * t)
            y = int(self.current_pos[1] + dy * t)
            pygame.draw.circle(self.surface, self.color, (x, y), self.size)
    
    def is_eraser(self, game_state):
        if game_state.tool_mode == config.ERASE_MODE:
            self.eraser = True
        else:
            self.eraser = False
    
    def current_color(self, game_state):
        self.colorTemp = game_state.current_color
    
    def current_size(self, game_state):
        self.size = game_state.brushSize

    def is_above_ui(self, event):
        # return event.pos[1] < config.CANVA_HEIGHT - config.TOOLBAR_HEIGHT
        return True


class FillTool():
    def __init__(self, surface, color=config.BLACK, size=config.BRUSH_SIZES[0]):
        self.color = color
        self.colorTemp = self.color
        self.size = size
        self.surface = surface
        self.drawing = False
        self.current_pos = None
        self.last_pos = None
        self.eraser = False

    def current_color(self, game_state):
        self.color = game_state.current_color

    def is_above_ui(self, event):
        # return event.pos[1] < config.CANVA_HEIGHT - config.TOOLBAR_HEIGHT
        return True

    def span_fill(self, position, threshold=0):
        x, y = int(position[0]), int(position[1])
        width, height = self.surface.get_size()

        if not (0 <= x < width and 0 <= y < height):
            print("Click out of bounds")
            return
        target_color = self.surface.get_at((x, y))
        print("Clicked color:", target_color)
        print("Fill color:", self.color)

        if target_color == self.color:
            print("Already filled, returning.")
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()
            # move to leftmost pixel in span (line)
            while x >= 0 and self.surface.get_at((x, y)) == target_color:
                x -= 1
            x += 1
            # fill span and check adjacent rows
            span_above = span_below = False
            # Fill the horizontal span and queue the lines above and below
            while x < width and self.surface.get_at((x, y)) == target_color:
                self.surface.set_at((x, y), self.color)
                
                # Check the pixel above
                if y > 0:
                    if self.surface.get_at((x, y - 1)) == target_color and not span_above:
                        stack.append((x, y - 1))
                        span_above = True
                    elif self.surface.get_at((x, y - 1)) != target_color:
                        span_above = False
                
                # Check the pixel below
                if y < height - 1:
                    if self.surface.get_at((x, y + 1)) == target_color and not span_below:
                        stack.append((x, y + 1))
                        span_below = True
                    elif self.surface.get_at((x, y + 1)) != target_color:
                        span_below = False
                
                x += 1

                    
