import pygame, numpy
import config
from assets import load_assets
from PaintTool import PenTool, FillTool
from OneTimeCaller import OneTimeCaller
OTC = OneTimeCaller()

canvas = pygame.Surface((config.CANVA_WIDTH, config.CANVA_HEIGHT))
canvas.fill(config.WHITE)
ui = None

class CanvaUI:
    def __init__(self):
        canvasAssets = load_assets(config.DRAWING)
        self.toolbar_bg = canvasAssets['toolbar_bg']
        self.back_button = canvasAssets['back_button']
        self.pen_button = canvasAssets['pen_button']
        self.bucket_button = canvasAssets['bucket_button']
        self.eraser_button = canvasAssets['eraser_button']
        self.color_buttons = canvasAssets['color_buttons']
        self.brush_buttons = canvasAssets['brush_buttons']
        self.topBarSurface = canvasAssets['topBar']
        self.chatSurface = canvasAssets['chatSurface']
        self.canvas_rect = canvas.get_rect(topleft=(config.CANVA_TOPLEFT))
        self.chat_ui = canvasAssets['chat_ui']
        self.topbarUI = canvasAssets['topbarUI']
        self.dashboardSurface = canvasAssets['dashboardSurface']
        self.dashboardUI = canvasAssets['dashboardUI']
        self.rmSetting = canvasAssets['rmSetting']

pen_tool = PenTool(canvas)
fill_tool = FillTool(canvas)
def init_canva_assets():
    global ui
    if ui == None:
        ui = CanvaUI()

def drawing(pen_tool, game_state, event):
    pen_tool.is_eraser(game_state)
    pen_tool.current_color(game_state)
    pen_tool.current_size(game_state)
    relative_mouse_pos = tuple(numpy.subtract(event.pos, config.CANVA_TOPLEFT))
    pen_tool.current_pos = relative_mouse_pos
    pen_tool.use()
    pen_tool.last_pos = pen_tool.current_pos  # Update for the next motion

def canva_update(screen, game_state, dt, player_state):
    OTC.call(lambda: setattr(game_state, 'canva', canvas)) # set canva in game_state once

    screen.blit(game_state.background, (0, 0))
    pygame.draw.rect(screen, config.BLACK, 
                     (config.CANVA_TOPLEFT[0]-5, config.CANVA_TOPLEFT[1]-20, 
                      config.CANVA_WIDTH+10, config.CANVA_HEIGHT+30), border_radius=8)
    screen.blit(canvas, config.CANVA_TOPLEFT)
    screen.blit(ui.toolbar_bg, (config.CANVA_TOPLEFT[0], 
                             config.CANVA_TOPLEFT[1] + config.CANVA_HEIGHT + 10))
    pygame.draw.rect(screen, config.WHITE, ui.topBarSurface, border_radius=8)
    pygame.draw.rect(screen, config.WHITE, ui.chatSurface, border_radius=8)
    ui.topbarUI.display(screen, game_state)
    ui.topbarUI.update(player_state)
    ui.dashboardUI.display(screen)
    

    # change color if selected
    ui.pen_button.self_selected(game_state, config.GREEN)
    ui.bucket_button.self_selected(game_state, config.GREEN)
    ui.eraser_button.self_selected(game_state, config.GREEN)

    for btn in ui.color_buttons:
        btn.self_selected(game_state, config.WHITE)

    for i, btn in enumerate(ui.brush_buttons):
        btn.self_selected(game_state, config.WHITE)
        if game_state.tool_mode == config.ERASE_MODE:
            btn.brushDotColor = config.WHITE
        else:
            btn.brushDotColor = config.BLACK

    # tools button
    ui.back_button.draw(screen)
    ui.pen_button.draw(screen)
    ui.bucket_button.draw(screen)
    ui.eraser_button.draw(screen)
    ui.chat_ui.draw(screen, game_state)
    ui.chat_ui.update(dt)


    # color button
    for btn in ui.color_buttons:
        btn.button_type = 'color'
        btn.draw(screen)

    # brush button
    for i, btn in enumerate(ui.brush_buttons):
        btn.button_type = 'brush'
        btn.draw(screen)
    
    if game_state.rmSetting:
        ui.rmSetting.display(screen, dt)
        return



def canva_event(event, game_state, player_state, roundManager, chatSys, db):
    if ui.back_button.is_clicked(event):
        roundManager.SET_DEFAULT()
        player_state.SET_DEFAULT()
        game_state.SET_DEFAULT()
        ui.rmSetting.set_text_default()
        db.delete_to(game_state)
        return
    ui.dashboardUI.handle_event(event, game_state, player_state)
    if game_state.rmSetting: # room setting
        ui.rmSetting.handle_event(event, game_state, player_state, db)
        return
    elif not roundManager.round_active and not game_state.rmSetting: # start round
        print(game_state.timer)
        roundManager.start_round()
        player_state.sync_player_local(game_state)
        return
    ui.chat_ui.handle_event(event, game_state, player_state, chatSys)
    
    if player_state.isDrawer:
        if ui.pen_button.is_clicked(event):
            game_state.tool_mode = config.PEN_MODE
        if ui.bucket_button.is_clicked(event):
            game_state.tool_mode = config.FILL_MODE
        if ui.eraser_button.is_clicked(event):
            game_state.tool_mode = config.ERASE_MODE
        
        for btn in ui.color_buttons:
            if btn.is_clicked(event):
                game_state.tool_mode = config.PEN_MODE
                game_state.current_color = btn.color
        
        for btn in ui.brush_buttons:
            if btn.is_clicked(event):
                game_state.brushSize = btn.brushSize

        # mouse draw handle
        if event.type == pygame.MOUSEBUTTONDOWN and ui.canvas_rect.collidepoint(event.pos):
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