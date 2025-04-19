import config

class GameState:
    def __init__(self): # Default value
        self.state = config.MENU
        self.is_host = False
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None # can't insert db
        self.canva = any # can't db
        self.rmSetting = False
        self.round = 1
        self.maxPlayer = 8
        self.maxRound = 3
        self.word = ''
        self.word_hint = ''
        self.score = 0
        self.isCustomWord = False
        self.timer = 0
        self.playerList = [] # dashboard
        self.chatLog = [] # chat ui
        self.guessed_correctly = None
        self.currentDrawer = ''

    def to_dict(self):
        temp_dict = self.__dict__.copy()
        temp_dict.pop('canva')
        temp_dict.pop('background')
        if 'playerList' in temp_dict:
            temp_dict['playerList'] = [player.to_dict() for player in self.playerList]
        if isinstance(temp_dict.get('guessed_correctly'), set):
            temp_dict['guessed_correctly'] = list(temp_dict['guessed_correctly'])

        return temp_dict
    
    def SET_DEFAULT(self):
        self.state = config.MENU
        self.is_host = False
        self.tool_mode = config.PEN_MODE
        self.current_color = config.BLACK
        self.brushSize = config.BRUSH_SIZES[0]
        self.background = None
        self.canva.fill(config.WHITE)
        self.rmSetting = False
        self.round = 1
        self.maxPlayer = 8
        self.maxRound = 3
        self.word = ''
        self.word_hint = ''
        self.score = 0
        self.isCustomWord = False
        self.timer = 0
        self.playerList = [] # dashboard
        self.chatLog = [] # chat ui
        self.guessed_correctly = None
        self.currentDrawer = ''

class PlayerState:
    def __init__(self):
        self._id = '' # python gen
        self.isGuessing = False
        self.isDrawer = True
        self.isHost = None
        self.username = 'anonymous'
        self.avartar = ''
        self.room_id = ''
        self.score = 0
        self.setting = ''
        self.message = ''
    
    def to_dict(self):
        tmp_dict = self.__dict__.copy()
        return tmp_dict
    
    def SET_DEFAULT(self):
        self._id = '' # python gen
        self.isGuessing = False
        self.isDrawer = True
        self.isHost = None
        self.username = 'anonymous'
        self.avartar = ''
        self.room_id = ''
        self.score = 0
        self.setting = ''
        self.message = ''
    
    def sync_player_local(self, obj):
        try:
            for p in obj.playerList:
                if p._id == self._id:
                    p_dict = obj.__dict__
                    self.__dict__.update({
                        key: value for key, value in p_dict.items() if key in ['isGuessing', 'isDrawer',
                                                                                 'isHost']
                    }) 
                    break
        except Exception as e:
            print("Error syncing player", e)  