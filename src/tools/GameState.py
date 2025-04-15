import config, pygame

class GameState:
    def __init__(self): # Default value
        self.state = config.MENU
        self.is_host = False
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva = any
        self.phase = config.GUESSING
        self.round = 1
        self.maxRound = 10
        self.word = 'KUYYAi'
    
    def SET_DEFAULT(self):
        self.state = config.MENU
        self.is_host = False
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva.fill(config.WHITE)

class PlayerState:
    def __init__(self):
        self.username = 'anonymous'
        self.avartar = ''
        self.room_id = ''
        self.score = 0
        self.setting = ''