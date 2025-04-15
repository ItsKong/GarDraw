import pygame, numpy
import config
config.add_tools
from assets import load_assets
from PaintTool import PenTool, FillTool
from OneTimeCaller import OneTimeCaller
from ChatUI import ChatUI
OTC = OneTimeCaller()

canvas = pygame.Surface((config.CANVA_WIDTH, config.CANVA_HEIGHT))
canvas.fill(config.WHITE)
canva_ui = None

class CanvaUI:
    def __init__(self):
        canvasAssets = load_assets('canvas')
        self.toolbar_bg = canvasAssets['toolbar_bg']
        self.back_button = canvasAssets['back_button']
        self.pen_button = canvasAssets['pen_button']
        self.bucket_button = canvasAssets['bucket_button']
        self.eraser_button = canvasAssets['eraser_button']
        self.color_buttons = canvasAssets['color_buttons']
        self.brush_buttons = canvasAssets['brush_buttons']
        self.topBar = canvasAssets['topBar']
        self.chatSurface = canvasAssets['chatSurface']
        self.canvas_rect = canvas.get_rect(topleft=(config.CANVA_TOPLEFT))
        self.chat_ui = canvasAssets['chat_ui']

pen_tool = PenTool(canvas)
fill_tool = FillTool(canvas)
def init_canva_assets():
    global canva_ui
    if canva_ui == None:
        canva_ui = CanvaUI()

def drawing(pen_tool, game_state, event):
    pen_tool.is_eraser(game_state)
    pen_tool.current_color(game_state)
    pen_tool.current_size(game_state)
    relative_mouse_pos = tuple(numpy.subtract(event.pos, config.CANVA_TOPLEFT))
    pen_tool.current_pos = relative_mouse_pos
    pen_tool.use()
    pen_tool.last_pos = pen_tool.current_pos  # Update for the next motion

def canva_update(screen, game_state, dt):
    OTC.call(lambda: setattr(game_state, 'canva', canvas)) # set canva in game_state once

    screen.blit(game_state.background, (0, 0))
    # pygame.draw.rect(screen, config.BLACK, 
    #                  (config.CANVA_TOPLEFT[0]-5, config.CANVA_TOPLEFT[1]-20, 
    #                   config.CANVA_WIDTH+10, config.CANVA_HEIGHT), border_radius=8)
    screen.blit(canvas, config.CANVA_TOPLEFT)
    screen.blit(canva_ui.toolbar_bg, (config.CANVA_TOPLEFT[0], 
                             config.CANVA_TOPLEFT[1] + config.CANVA_HEIGHT + 10))
    screen.blit(canva_ui.topBar, (config.CANVA_TOPLEFT[0] - 220, 30))
    pygame.draw.rect(screen, config.WHITE, canva_ui.chatSurface, border_radius=8)

    # change color if selected
    canva_ui.pen_button.self_selected(game_state, config.GREEN)
    canva_ui.bucket_button.self_selected(game_state, config.GREEN)
    canva_ui.eraser_button.self_selected(game_state, config.GREEN)

    for btn in canva_ui.color_buttons:
        btn.self_selected(game_state, config.WHITE)

    for i, btn in enumerate(canva_ui.brush_buttons):
        btn.self_selected(game_state, config.WHITE)
        if game_state.tool_mode == config.ERASE_MODE:
            btn.brushDotColor = config.WHITE
        else:
            btn.brushDotColor = config.BLACK

    # tools button
    canva_ui.back_button.draw(screen)
    canva_ui.pen_button.draw(screen)
    canva_ui.bucket_button.draw(screen)
    canva_ui.eraser_button.draw(screen)
    canva_ui.chat_ui.draw(screen)
    canva_ui.chat_ui.update(dt)


    # color button
    for btn in canva_ui.color_buttons:
        btn.button_type = 'color'
        btn.draw(screen)

    # brush button
    for i, btn in enumerate(canva_ui.brush_buttons):
        btn.button_type = 'brush'
        btn.draw(screen)


def canva_event(event, game_state, player_state):
     # button event handle
    # canva_ui.chatTextArea.handle_event(event)
    # canva_ui.chatTextArea.update(pygame.time.Clock().tick(60))
    canva_ui.chat_ui.handle_event(event, player_state)

    if canva_ui.back_button.is_clicked(event):
        # game_state.state = config.MENU
        game_state.SET_DEFAULT()
    if canva_ui.pen_button.is_clicked(event):
        game_state.tool_mode = config.PEN_MODE
    if canva_ui.bucket_button.is_clicked(event):
        game_state.tool_mode = config.FILL_MODE
    if canva_ui.eraser_button.is_clicked(event):
        game_state.tool_mode = config.ERASE_MODE
    
    for btn in canva_ui.color_buttons:
        if btn.is_clicked(event):
            game_state.tool_mode = config.PEN_MODE
            game_state.current_color = btn.color
    
    for btn in canva_ui.brush_buttons:
        if btn.is_clicked(event):
            game_state.brushSize = btn.brushSize

    # mouse draw handle
    if event.type == pygame.MOUSEBUTTONDOWN and canva_ui.canvas_rect.collidepoint(event.pos):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        canvas_x = mouse_x - config.CANVA_TOPLEFT[0]
        canvas_y = mouse_y - config.CANVA_TOPLEFT[1]
        if game_state.tool_mode == config.FILL_MODE: # fill mode
            if fill_tool.is_above_ui(event):
                fill_tool.current_color(game_state)
                fill_tool.span_fill((canvas_x, canvas_y))
        else:
            pen_tool.drawing = True
            pen_tool.last_pos = (canvas_x, canvas_y)
            drawing(pen_tool, game_state, event)

    elif event.type == pygame.MOUSEBUTTONUP:
        pen_tool.drawing = False
        pen_tool.last_pos = None

    elif (event.type == pygame.MOUSEMOTION and pen_tool.drawing and pen_tool.last_pos 
                and game_state.tool_mode != config.FILL_MODE):
        if pen_tool.is_above_ui(event):
            drawing(pen_tool, game_state, event)