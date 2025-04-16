import config

class GameState:
    def __init__(self): # Default value
        self.state = config.MENU
        self.is_host = False
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva = any
        self.rmSetting = False
        self.round = 1
        self.maxRound = 3
        self.word = ''
        self.word_hint = ''
        self.score = 0
        self.isCustomWord = False
        self.timer = 0
        self.playerList = [] # dashboard
        self.chatLog = [] # chat ui
        self.guessed_correctly = []
        self.currentDrawer = ''
    
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
        self._id = ''
        self.isGuessing = False
        self.isDrawer = True
        self.username = 'anonymous'
        self.avartar = ''
        self.room_id = ''
        self.score = 0
        self.setting = ''
        self.message = ''