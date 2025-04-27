import config, random

class GameState:
    def __init__(self): # Default value
        self.state = config.MENU
        self.currentHost = ''
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
        self.version = 0
        self.drawPos = ()

    def to_dict(self):
        temp_dict = self.__dict__.copy()
        temp_dict.pop('canva')
        temp_dict.pop('background')
        if 'playerList' in temp_dict:
            temp_dict['playerList'] = [player.to_dict() for player in self.playerList if hasattr(player, 'to_dict')] 
        if isinstance(temp_dict.get('guessed_correctly'), set):
            temp_dict['guessed_correctly'] = list(temp_dict['guessed_correctly'])

        return temp_dict
    
    def to_obj(self, data):
        try:
            self._id = ''
            for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
            self.playerList =  [PlayerState(**p) for p in self.playerList] 
            print("Object Synchronized! => ", str(self))
        except Exception as e:
            print("Failed to synchronized:", str(e))
    
    # def sync_gameState_local(self, db):
    #     # sync with mongoDB game state
    #     try:
    #         db.sync_from_db(self)
    #         self.playerList = [PlayerState(**p) for p in self.playerList] 
    #     except Exception as e:
    #         print("Syncing Fail error: ", str(e))
    
    # def join_game(self, obj, db, id=None):
    #     # pull => sync local => append player local => update db
    #     try:
    #         if id:
    #             db.pull_from_db(self, id)
    #         else:
    #             lists = db.get_all_id()
    #             randID = random.choice(lists)
    #             db.pull_from_db(self, randID)
    #         self.playerList = [PlayerState(**p) for p in self.playerList] 
    #         print(type(self.playerList[0]))
    #         # print(type(self.playerList[0]))
    #         self.playerList.append(obj)
    #         db.update_to(self)
    #         return True
    #     except Exception as e:
    #         print("Joining Fail error:", str(e))
    #         return False

    
    def SET_DEFAULT(self):
        self.state = config.MENU
        self.currentHost = ''
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
        self.version = 0

class PlayerState:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id', '')
        self.isGuessing = kwargs.get('isGuessing', False)
        self.isDrawer = kwargs.get('isDrawer', False)
        self.isHost = kwargs.get('isHost', False)
        self.username = kwargs.get('username', 'anonymous')
        self.avartar = kwargs.get('avartar', '')
        self.room_id = kwargs.get('room_id', '')
        self.score = kwargs.get('score', 0)
        self.setting = kwargs.get('setting', '')
        self.message = kwargs.get('message', '')
    
    def to_dict(self):
        tmp_dict = self.__dict__.copy()
        return tmp_dict
    
    def SET_DEFAULT(self):
        self._id = '' # python gen
        self.isGuessing = False
        self.isDrawer = False
        self.isHost = False
        self.username = 'anonymous'
        self.avartar = ''
        self.room_id = ''
        self.score = 0
        self.setting = ''
        self.message = ''
    
    # def sync_player_local(self, obj):
    #     # sync with local game state
    #     try:
    #         for p in obj.playerList:
    #             if p._id == self._id:
    #                 p_dict = obj.__dict__
    #                 self.__dict__.update({
    #                     key: value for key, value in p_dict.items() if key in ['isGuessing', 'isDrawer',
    #                                                                              'isHost']
    #                 }) 
    #                 break
    #     except Exception as e:
    #         print("Error syncing player", e)  