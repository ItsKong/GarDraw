import config, pygame

class GameState:
    def __init__(self): # Default value
        self.state = config.MENU
        self.user_text = ''
        self.is_host = False
        self.room_id = ''
        self.score = 0
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva = any
    
    def SET_DEFAULT(self):
        self.state = config.MENU
        self.user_text = ''
        self.is_host = False
        self.room_id = ''
        self.score = 0
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva.fill(config.WHITE)
