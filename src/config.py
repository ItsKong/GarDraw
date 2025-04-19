import sys, os, pygame
# from screeninfo import get_monitors
def add_path():
    tools_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tools'))
    pages_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pages'))
    sys.path.append(tools_folder_path)
    sys.path.append(pages_folder_path)


def relative_pos(x, y, e):
    # Calculate position relative to surface
    rel_x = e.pos[0] - x
    rel_y = e.pos[1] - y

    # Create new adjusted event
    adjusted_event = pygame.event.Event(
        e.type,
        {
            'pos': (rel_x, rel_y),
            'button': getattr(e, 'button', 0)
        }
    )
    return adjusted_event

FPS = 144

# WIDTH, HEIGHT = get_resulution()
WIDTH, HEIGHT = 1400, 800
# WIDTH, HEIGHT = 1600, 900
CANVA_WIDTH, CANVA_HEIGHT = 800, 600
CANVA_TOPLEFT = ((WIDTH - CANVA_WIDTH) // 2, (HEIGHT - CANVA_HEIGHT) // 2) # 300
# CANVA_TOPLEFT = (0,0)
MENU_WIDTH, MENU_HEIGHT = 400, 306
MENU_TOPLEFT = ((WIDTH - MENU_WIDTH) // 2, HEIGHT*0.195)

## note CANVA == SCREEN Topleft 0,0 => normal
## CANVA == 800, 600 Topleft 0,0 => tool bar grey to black in 2 frame,  brush button grey fade in 2 frame 
## CANVA_WIDTH, CANVA_HEIGHT = 800 Topleft = ((WIDTH - CANVA_WIDTH) // 2, (HEIGHT - CANVA_HEIGHT) // 2)
## => tool bar grey to black in 2 frame,  brush button grey fade in 2 frame 
## screen.blit(toolbar_bg, (0, config.WIDTH - 50)) => brush button border bug

## ALL CONSTANST
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (193, 9, 48, 230)  # RGBA color with 90% opacity
GREEN = (64, 255, 47)
SEL_GREEN = (48, 194, 35)
YELLOW = (255, 208, 64)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
SEL_ORANGE =(204, 132, 0)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (220, 220, 22)
TEST = (220, 220, 22, 0)

# Game states
MENU = "menu"
DRAWING = "drawing"
GUESSING = "guessing"
WAITING = 'waiting'

# Drawing mode
PEN_MODE = "pen"
ERASE_MODE = "erase"
FILL_MODE = "fill"
SETTING = 'setting'

# Fixed brush size options
BRUSH_SIZES = [6, 15, 50]
TOOLBAR_HEIGHT = 50