import pygame, numpy, time
import config
config.add_tools
from assets import load_assets
from PaintTool import PenTool, FillTool
from OneTimeCaller import OneTimeCaller
canvas = pygame.Surface((config.CANVA_WIDTH, config.CANVA_HEIGHT))
canvas.fill(config.WHITE)

otc = OneTimeCaller()

canvasAsset = load_assets('canvas')
toolbar_bg = canvasAsset['toolbar_bg']
back_button = canvasAsset['back_button']
pen_button = canvasAsset['pen_button']
bucket_button = canvasAsset['bucket_button']
eraser_button = canvasAsset['eraser_button']
color_buttons = canvasAsset['color_buttons']
brush_buttons = canvasAsset['brush_buttons']
topBar = canvasAsset['topBar']
chatSurface = canvasAsset['chatSurface']
chatTextArea = canvasAsset['chatTextArea']

pen_button.mode = config.PEN_MODE
bucket_button.mode = config.FILL_MODE
eraser_button.mode = config.ERASE_MODE

pen_tool = PenTool(canvas)
fill_tool = FillTool(canvas)

def drawing(pen_tool, game_state, event):
    pen_tool.is_eraser(game_state)
    pen_tool.current_color(game_state)
    pen_tool.current_size(game_state)
    relative_mouse_pos = tuple(numpy.subtract(event.pos, config.CANVA_TOPLEFT))
    pen_tool.current_pos = relative_mouse_pos
    pen_tool.use()
    pen_tool.last_pos = pen_tool.current_pos  # Update for the next motion

def button_seleted_checker(game_state):
    pen_button.self_selected(game_state, config.GREEN)
    bucket_button.self_selected(game_state, config.GREEN)
    eraser_button.self_selected(game_state, config.GREEN)
    # color butt
    for btn in color_buttons:
        btn.self_selected(game_state, config.WHITE)

    # brush butt
    for i, btn in enumerate(brush_buttons):
        btn.self_selected(game_state, config.WHITE)
        if game_state.tool_mode == config.ERASE_MODE:
            btn.brushDotColor = config.WHITE
        else:
            btn.brushDotColor = config.BLACK

def canvas_page(screen, event, game_state):
    otc.call(lambda: setattr(game_state, 'canva', canvas)) # set canva in game_state once
    # screen.fill(config.WHITE)
    screen.blit(game_state.background, (0, 0))
    canvas_rect = canvas.get_rect(topleft=(config.CANVA_TOPLEFT))
    screen.blit(canvas, config.CANVA_TOPLEFT)
    screen.blit(toolbar_bg, (config.CANVA_TOPLEFT[0], 
                             config.CANVA_TOPLEFT[1] + config.CANVA_HEIGHT + 10))
    screen.blit(topBar, (config.CANVA_TOPLEFT[0] - 220, 30))
    screen.blit(chatSurface, (config.CANVA_TOPLEFT[0]*3 + 205, config.CANVA_TOPLEFT[1]))
    # change color if selected
    button_seleted_checker(game_state)

    # tools button
    back_button.draw(screen)
    pen_button.draw(screen)
    bucket_button.draw(screen)
    eraser_button.draw(screen)
    chatTextArea.draw(screen)

    # color button
    for btn in color_buttons:
        btn.button_type = 'color'
        btn.draw(screen)

    # brush button
    for i, btn in enumerate(brush_buttons):
        btn.button_type = 'brush'
        btn.draw(screen)

    # button event handle
    chatTextArea.handle_event(event)
    chatTextArea.update(pygame.time.Clock().tick(60))

    if back_button.is_clicked(event):
        # game_state.state = config.MENU
        game_state.SET_DEFAULT()
    if pen_button.is_clicked(event):
        game_state.tool_mode = config.PEN_MODE
    if bucket_button.is_clicked(event):
        game_state.tool_mode = config.FILL_MODE
    if eraser_button.is_clicked(event):
        game_state.tool_mode = config.ERASE_MODE
    
    for btn in color_buttons:
        if btn.is_clicked(event):
            game_state.tool_mode = config.PEN_MODE
            game_state.current_color = btn.color
    
    for btn in brush_buttons:
        if btn.is_clicked(event):
            game_state.brushSize = btn.brushSize

    # mouse draw handle
    if event.type == pygame.MOUSEBUTTONDOWN and canvas_rect.collidepoint(event.pos):
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