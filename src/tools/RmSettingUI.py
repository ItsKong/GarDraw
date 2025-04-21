import pygame, config
from Button import TextButton
from TextInput import TextInput
from Dropdown import Dropdown

class RmSettingUI:
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.maxPLayer = 0
        self.drawTime = 60
        self.maxRounds = 3
        self.wordcount = 3
        self.baseH = 20
        self.customWord = ''

        self.font = pygame.font.Font(kwargs.get("font", None), kwargs.get("fontSize", 30))
        self.start = TextButton(5, height - 55, (width // 2) + 150, 50,
                            text='Start', color=config.GREEN, radius=8)
        self.invite = TextButton((width//2) + 160, height - 55, (width//4) + 30, 50,
                                text='Invite', color=config.ORANGE, radius=8)
        self.textArea = TextInput(5, (height//2) - 50, width - 10, (height//2) - 50, radius=8,
                                  placeholder='Custom word. Separate by , (comma)')
        self.maxplyBtn = TextInput(200, self.baseH-10, self.rect.width//2, self.baseH+10, radius=8,
                                    placeholder='Min 3 player, Max 8 player')
        self.drawTimeBtn = TextInput(200, self.baseH+30, self.rect.width//2, self.baseH+10, radius=8,
                                    placeholder='Time per Round')
        self.maxRndBtn = TextInput(200, self.baseH+70, self.rect.width//2, self.baseH+10, radius=8,
                                    placeholder='Total rounds')
    def set_text_default(self):
        self.textArea.text = ''
        self.maxplyBtn.text = ''
        self.drawTimeBtn.text = ''
        self.maxRndBtn.text = ''

        self.textArea.value = ''
        self.maxplyBtn.value = ''
        self.drawTimeBtn.value = ''
        self.maxRndBtn.value = ''

        self.textArea.active = False
        self.maxplyBtn.active = False
        self.drawTimeBtn.active = False
        self.maxRndBtn.active = False

    def handle_event(self, e, game_state, player_state, db):
        adj_e = config.relative_pos(self.rect.x, self.rect.y, e)
        self.textArea.handle_event(adj_e)
        self.maxplyBtn.handle_event(adj_e)
        self.drawTimeBtn.handle_event(adj_e)
        self.maxRndBtn.handle_event(adj_e)
        if self.textArea.value:
            game_state.isCustomWord = True
            self.customWord = self.textArea.value
        if self.maxplyBtn.value.isdigit():
            game_state.maxPlayer = int(self.maxplyBtn.value)
        if self.drawTimeBtn.value.isdigit():
            game_state.timer = int(self.drawTimeBtn.value)
        if self.maxRndBtn.value.isdigit():
            game_state.maxRound = int(self.maxRndBtn.value)

        if self.start.is_clicked(adj_e):   
            game_state.currentDrawer = player_state._id # shoulde be _id
            game_state.rmSetting = False 
        if self.invite.is_clicked(adj_e):
            txt = str(game_state._id)
            pygame.scrap.put(pygame.SCRAP_TEXT, txt.encode('utf-8'))
            

    def display(self, screen, dt):
        # print(self.drawTimeBtn.value)
        self.surface.fill(config.DARK_GRAY)
        maxPlayer = self.font.render("Max player:", True, config.WHITE)
        drawTime = self.font.render("Draw time:", True, config.WHITE)
        maxRounds = self.font.render("Max rounds: ", True, config.WHITE)
        # wordCount = self.font.render("Word count", True, config.WHITE)
        self.start.draw(self.surface)
        self.textArea.draw(self.surface)
        self.maxplyBtn.draw(self.surface)
        self.drawTimeBtn.draw(self.surface)
        self.maxRndBtn.draw(self.surface)
        self.invite.draw(self.surface)

        self.textArea.update(dt)
        self.maxplyBtn.update(dt)
        self.drawTimeBtn.update(dt)
        self.maxRndBtn.update(dt)

        self.surface.blit(maxPlayer, (30, self.baseH))
        self.surface.blit(drawTime, (30, self.baseH + 40))
        self.surface.blit(maxRounds, (30, self.baseH + 80))
        # self.surface.blit(wordCount, (30, self.baseH + 120))
        screen.blit(self.surface, (self.rect.x, self.rect.y))