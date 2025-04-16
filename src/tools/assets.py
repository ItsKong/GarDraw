import pygame
import config
config.add_tools()
from Button import Button, BrushButton, TextButton, IconButton, ColorButton
from TextInput import TextInput
from Dropdown import Dropdown
from ChatUI import ChatUI
from TopBarUI import TopBarUI
from DashboardUI import DashboardUI
from RmSettingUI import RmSettingUI

def load_assets(page):
    if page == config.MENU:
        # load background 
        try:
            background_image = pygame.image.load("./picture/background.png")
            background_image = pygame.transform.scale(background_image, (config.WIDTH, config.HEIGHT))
        except:
            background_image = pygame.Surface((config.WIDTH, config.HEIGHT))
            background_image.fill(config.WHITE)

        # load logo
        try:
            logo = pygame.image.load("./picture/logo.png")
            logo_width, logo_height = logo.get_size()
            new_width = 400
            new_height = int((new_width / logo_width) * logo_height)
            logo = pygame.transform.scale(logo, (new_width, new_height))
        except:
            logo = pygame.Surface((400, 200))
            logo.fill(config.BLUE)

        # menu componet
        menu_background = pygame.Surface((config.MENU_WIDTH, config.MENU_HEIGHT), pygame.SRCALPHA)
        # avatar select
        # avatarSelect = 

        # button v.2
        join_room_button = TextButton(config.WIDTH*0.3649, 
                                    config.HEIGHT*0.43, 
                                    config.MENU_WIDTH - 20, 
                                    50, 
                                    text="PLAY", color=config.GREEN,
                                    radius=8,
                                    hoverColor=config.SEL_GREEN)
        create_room_button = TextButton(config.WIDTH*0.3649, 
                                  config.HEIGHT*0.5, 
                                  config.MENU_WIDTH - 20, 
                                  40, 
                                  text="CREATE PRIVATE ROOM", color=config.ORANGE,
                                  radius=8,
                                  hoverColor=config.SEL_ORANGE)
        # quit_button = Button((config.WIDTH - button_width) // 2, 300, 
        #                      button_width, button_height, "quit", config.PINK)
        
        # language button
        language_btn = Dropdown(config.WIDTH*0.55,
                                config.HEIGHT*0.22,
                                config.MENU_WIDTH*0.2, 
                                40, 
                                text_color=config.RED,
                                fontSize=25,
                                border_radius=-1,
                                radius=8,
                                hoverColor=config.GRAY,
                                color=config.WHITE,
                                choices=[
                                    'English',
                                    'Thai'
                                ])

        # Name input box position updated to be above the first button
        input_box_width, input_box_height = 250, 40
        name_input = TextInput(config.WIDTH*0.3649,  
                                config.HEIGHT*0.22,           
                                config.MENU_WIDTH*0.6,                        
                                input_box_height,                       
                                placeholder="Enter your name",
                                radius=8)
        
        
        menuAsset = {
            'bg': background_image,
            'menu_bg': menu_background,
            'logo': logo,
            'create_room_button': create_room_button,
            'join_room_button' : join_room_button,
            #'quit_button' : quit_button,
            'name_input' : name_input,
            'language_btn': language_btn
        }
        return menuAsset
    

    # =========================================================================================================
    # ====================================  SECTION CANVA =====================================================
    # =========================================================================================================
    
    if page == config.DRAWING:
        # Load tool icons
        try:
            eraser_icon = pygame.image.load("./picture/eraser.png")
            eraser_icon = pygame.transform.scale(eraser_icon, (30, 30))
        except pygame.error:
            eraser_icon = None

        try:
            pen_icon = pygame.image.load("./picture/pen.png")
            pen_icon = pygame.transform.scale(pen_icon, (30, 30))
        except pygame.error:
            pen_icon = None

        try:
            bucket_icon = pygame.image.load("./picture/color.png")
            bucket_icon = pygame.transform.scale(bucket_icon, (30, 30))
        except pygame.error:
            bucket_icon = None
        
        try:
            clock_icon = pygame.image.load('./picture/icon/timer.png')
            clock_icon = pygame.transform.scale(clock_icon, (config.TOOLBAR_HEIGHT, config.TOOLBAR_HEIGHT))
        except pygame.error:
            clock_icon = None

        try:
            setting_icon = pygame.image.load('./picture/icon/settings.png')
            setting_icon = pygame.transform.scale(setting_icon, (config.TOOLBAR_HEIGHT, config.TOOLBAR_HEIGHT))
        except pygame.error:
            setting_icon = None

        # UI element =>
        # surface 
        topBar = pygame.Rect((config.CANVA_TOPLEFT[0] - 220, 25,config.CANVA_WIDTH + 500, config.TOOLBAR_HEIGHT))
        chatSurface = pygame.Rect((config.CANVA_TOPLEFT[0]*3 + 210, config.CANVA_TOPLEFT[1], 275, config.CANVA_HEIGHT))
        toolbar_bg = pygame.Surface((config.CANVA_WIDTH, config.TOOLBAR_HEIGHT), pygame.SRCALPHA)
        toolbar_bg.fill((0, 0, 0, 0)) #(0, 0, 0, 128))
        dashboardSurface = pygame.Rect((config.CANVA_TOPLEFT[0] - 225,
                                        config.CANVA_TOPLEFT[1],
                                        215,
                                        config.CANVA_HEIGHT))

        chat_ui = ChatUI(chatSurface.x + 5,
                         chatSurface.y + 5,
                         chatSurface.width - 10,
                         chatSurface.height - 10)
        topbarUI = TopBarUI(topBar.x, topBar.y, 
                            topBar.width, topBar.height,
                            icon={
                                'clock_icon': clock_icon,
                                'setting_icon': setting_icon
                            })
        dashboardUI = DashboardUI(dashboardSurface.x,
                                  dashboardSurface.y,
                                  dashboardSurface.width,
                                  dashboardSurface.height)
        rmSetting = RmSettingUI(config.CANVA_TOPLEFT[0], config.CANVA_TOPLEFT[1],
                                config.CANVA_WIDTH, config.CANVA_HEIGHT)

        # button
        tool_btn_size = 40
        back_button = TextButton(10, config.HEIGHT - 45, 100, 30 , text='Back', color=config.RED, border_radius=0)
        pen_button = IconButton(config.CANVA_WIDTH, 
                                ((config.HEIGHT + config.CANVA_HEIGHT + config.TOOLBAR_HEIGHT) // 2) - 5 , 
                                tool_btn_size, tool_btn_size , 
                                text='Pen', 
                                color=config.BLACK, 
                                border_width=3,
                                radius=0, 
                                icon=pen_icon,
                                mode=config.PEN_MODE)
        bucket_button = IconButton(config.CANVA_WIDTH + 40, 
                                ((config.HEIGHT + config.CANVA_HEIGHT + config.TOOLBAR_HEIGHT) // 2) - 5 , 
                                tool_btn_size, tool_btn_size , 
                                text='Bucked', 
                                color=config.BLACK, 
                                border_width=3,
                                radius=0, 
                                icon=bucket_icon,
                                mode=config.FILL_MODE)
        eraser_button = IconButton(config.CANVA_WIDTH + 80, 
                                ((config.HEIGHT + config.CANVA_HEIGHT + config.TOOLBAR_HEIGHT) // 2) - 5 , 
                                tool_btn_size, tool_btn_size , 
                                text='eraser', 
                                color=config.BLACK, 
                                border_width=3,
                                radius=0, 
                                icon=eraser_icon,
                                mode=config.ERASE_MODE)
        
        # Color palette for drawing
        color_palette = [
            {"color": config.BLACK, "name": "Black"},
            {"color": config.WHITE, "name": "White"},
            {"color": config.BROWN, "name": "Brown"},
            {"color": config.RED, "name": "Red"},
            {"color": config.BLUE, "name": "Blue"},
            {"color": config.CYAN, "name": "Cyan"},
            {"color": config.GREEN, "name": "Green"},
            {"color": config.YELLOW, "name": "Yellow"},
            {"color": config.ORANGE, "name": "Orange"},
            {"color": config.PINK, "name": "Pink"},
            {"color": config.PURPLE, "name": "Purple"},
        ]
        # Color picker buttons - positioned at the bottom
        color_button_size = 30
        color_buttons = []
        color_palette_x = (config.WIDTH - config.CANVA_WIDTH + 10) // 2 # 120
        color_palette_y = (config.HEIGHT + config.CANVA_HEIGHT + config.TOOLBAR_HEIGHT) // 2 #config.HEIGHT - config.TOOLBAR_HEIGHT + 10
        color_palette_spacing = 1
        # Initialize color picker buttons
        for i, color_data in enumerate(color_palette):
            x_pos = color_palette_x + i * (color_button_size + color_palette_spacing)
            color_buttons.append(ColorButton(x_pos, color_palette_y, color_button_size, color_button_size, 
                                text=color_data['name'], 
                                color= color_data["color"],
                                mode=color_data['color'],
                                border_width=3))
        brush_buttons = []
        brush_button_spacing = 5
        brush_button_size = 40
        brush_pos_x = config.CANVA_WIDTH + 150 # WIDTH + 190
        # Brush butt
        for i, size in enumerate(config.BRUSH_SIZES):
            x_pos = brush_pos_x + i * (brush_button_size + brush_button_spacing)
            brush_buttons.append(BrushButton(x_pos, 
                                        (config.HEIGHT + config.CANVA_HEIGHT + config.TOOLBAR_HEIGHT - 20)//2,
                                        brush_button_size, brush_button_size, color=config.BLACK,
                                        brushSize=size, mode=size))
        
        canvasAsset = {
            'back_button' : back_button,
            'toolbar_bg': toolbar_bg,
            'pen_button': pen_button,
            'bucket_button': bucket_button,
            'eraser_button': eraser_button,
            'color_buttons': color_buttons,
            'brush_buttons': brush_buttons,
            'topBar': topBar,
            'chatSurface': chatSurface,
            'chat_ui': chat_ui,
            'topbarUI': topbarUI,
            'dashboardSurface': dashboardSurface,
            'dashboardUI': dashboardUI,
            'rmSetting': rmSetting
        }
        return canvasAsset
