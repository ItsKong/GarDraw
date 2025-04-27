# random word, timer, chat interactive, round count
import random, pygame, config

class RoundManager:
    # manage time round and word handle game progression 
    # timer each round and choose new player, word next round
    # endround when someone guess the right word or timer runnint out

    def __init__(self, game_state, player_state, db):
        self.game_state = game_state
        self.player_state = player_state
        self.randword = []
        self.db = db
        self.words =  [] #word or ["apple", "car", "pizza", "bicycle"]
        self.last_tick = pygame.time.get_ticks()
        self.round_active = False
        self.areadyDraw = []
        self.manager = None
    
    def choose_word(self):
        defaultWord = ["apple", "banana", "car", "dog", "elephant", "flower", "guitar", "house", "island", 
                       "jungle","kite", "lion", "mountain", "notebook", "ocean", "pencil", "queen", "robot", 
                       "sun", "tree"]
        if self.game_state.isCustomWord:
            # return random.choice(custom_wrod)
            pass
        return random.choice(defaultWord)


    def get_manager(self, manager):
        self.manager = manager
    
    def SET_DEFAULT(self):
        self.words =  [] #word or ["apple", "car", "pizza", "bicycle"]
        self.last_tick = pygame.time.get_ticks()
        self.round_active = False
        self.areadyDraw = []
        # self.game_state.guessed_correctly.clear()
    
    def start_round(self):
        # set game state
        # for player in self.game_state.playerList:
        #     if self.player_state._id == player._id:
        #         self.player_state = player
        # if self.game_state.currentDrawer == self.player_state._id:
        #     self.player_state.isDrawer = True
        #     self.player_state.isGuessing = False
        # else:
        #     self.player_state.isDrawer = False
        #     self.player_state.isGuessing = True
        self.words = self.choose_word()
        self.game_state.timer = self.game_state.timer if self.game_state.timer > 0 else 10
        self.game_state.maxRound = self.game_state.maxRound if ( self.game_state.maxRound > 0 and
                                                        self.game_state.maxRound < self.game_state.maxPlayer) else 3
        self.game_state.word = self.words
        self.game_state.word_hint = ("_" + " ") * len(self.words)
        self.game_state.guessed_correctly = set()
        self.round_active = True

        # rotate drawer each round
        for p in self.game_state.playerList:
            if p._id in self.areadyDraw:
                p.isGuessing = True
                p.isDrawer = False
                if p._id == self.player_state._id:
                    self.player_state.isGuessing = True
                    self.player_state.isDrawer = False
            else:
                p.isGuessing = False
                p.isDrawer = True
                if p._id == self.player_state._id:
                    self.player_state.isGuessing = False
                    self.player_state.isDrawer = True
                print('hi', self.game_state.currentDrawer)
                print(f"{p.username} is drawer")
                break
        if self.player_state.isHost:
            self.game_state.version += 1
            # self.db.update_to(self.game_state)
            self.manager.set_action('update')

    def update(self):
        # print(self.game_state.timer)
        now = pygame.time.get_ticks()
        if self.round_active and now - self.last_tick >= 1000:
            self.game_state.timer -= 1
            self.last_tick = now
            if self.player_state.isHost:
                # self.game_state.version += 1
                # self.db.update_to(self.game_state)
                self.manager.set_action('update')

            if self.game_state.timer <= 0:
                self.end_round()
    
    def end_round(self):
        print("Round ended.")
        self.round_active = False
        self.game_state.round += 1

        if self.game_state.round > self.game_state.maxRound:
            self.game_state.state = "result"
        else:
            self.areadyDraw.append(self.game_state.currentDrawer)
            self.game_state.word = ''
            self.game_state.word_hint = ''
            self.game_state.canva.fill(config.WHITE)
            self.game_state.chatLog = []
            self.start_round()

        

class ChatSystem:
    def __init__(self, game_state, player_state, db):
        self.game_state = game_state
        self.player_state = player_state
        self.db = db

    def check_guess(self, player_name, message):
        if message.strip().lower() == self.game_state.word.lower():
            if player_name not in self.game_state.guessed_correctly:
                print("HI")
                self.game_state.guessed_correctly.add(player_name)
                print(f"{player_name} guessed the word correctly!")
                self.award_points(player_name)
                self.player_state.isGuessing = False
                self.db.update_to(self.game_state)
                return f"{player_name} guessed the word correctly!"
        else:
            return ''

    def award_points(self, player_name):
        for player in self.game_state.playerList:
            if player.username == player_name:
                player.score += 100