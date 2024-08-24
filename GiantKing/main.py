import pyxel
import random
from building_manager import BuildingManager
from choice_manager import ChoiceManager
from buildings import Building,Tower
from resource_manager import ResourceManager, ResourcesIndex, resource_names, resource_sprites, resource_mini_icons
from placer_manager import PlacerManager
from tile_manager import TileManager, TileIndex, tile_sprites
from descriptions_manager import DescriptionsManager
from buildings import Building
from particles_manager import ParticleManager
from event_manager import EventManager, Event
from wave_manager import WaveManager
from game_manager import GameManager, GameState
from animation_handler import AnimationHandler

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

TILE_WIDTH = 16
TILE_HEIGHT = 16
TILE_MAP_WIDTH = 12
TILE_MAP_HEIGHT = 12

RESOURCES_BASE_X = 192
RESOURCE_BASE_Y = 0

CHOICE_PANE_BASE_X = 0
CHOICE_PANE_BASE_Y = 192

CHOICE_BAR_SIZE = 4

PLAY_BUTTON = (16*6,16*4,16*4,16*2)
QUIT_BUTTON = (16*6, 16*10, 16*4,16*2)
HOW_TO_PLAY_BUTTON = (16*6, 16*7,16*4,16*2)

PLAY_AGAIN_BUTTON = (4*16,4*16,16*4,16*2)
GO_TO_MENU_BUTTON = (4*16, 7*16, 16*4,16*2)

RESUME_BUTTON = (4*16,4*16,16*4,16*2)

NEXT_BUTTON = (0,0,16*4,16*2)

class TileMap:
    def __init__(self):
        pass
    

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Bubbles", capture_scale=1)
        pyxel.mouse(True)

        self.game_manager = GameManager()
        self.game_reset()

        # load tilemap images:
        pyxel.load("tiles.pyxres")
        self.load_buttons_sprites()
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def load_buttons_sprites(self):
        pyxel.images[2].load(0,0,"assets_buttons_resized/PlayButton.png")
        pyxel.images[2].load(0,16*2,"assets_buttons_resized/QuitButton.png")
        pyxel.images[2].load(0,16*4,"assets_buttons_resized/PlayAgain.png")
        pyxel.images[2].load(0,16*6,"assets_buttons_resized/Menu.png")
        pyxel.images[2].load(0,16*8,"assets_buttons_resized/Unpause.png")
        pyxel.images[2].load(0,16*10,"assets_buttons_resized/HowToPlay.png")
        pyxel.images[2].load(0,16*12,"assets_buttons_resized/NextButton.png")

    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_click_interaction()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.placer_manager.reset()

        if(self.game_manager.game_state == GameState.MENU):
            self.simulate_menu()
        if(self.game_manager.game_state == GameState.LOSE_SCREEN):
            self.simulate_lose()

        if(self.game_manager.game_state == GameState.HOW_TO_PLAY):
            self.simulate_how_to_play()
        
        if (self.game_manager.game_state == GameState.PAUSE):
            if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_SPACE):
                self.game_manager.game_state = GameState.GAME
            return

        if (self.game_manager.game_state == GameState.GAME):
            self.building_manager.simulate()
            self.choice_manager.simulate()
            self.event_manager.simulate()
            self.wave_manager.simulate()    
            self.animation_handler.simulate_all()    
            if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_SPACE):
                self.game_manager.game_state = GameState.PAUSE
    def draw(self):
        pyxel.cls(0)
        
        if self.game_manager.game_state == GameState.MENU:
            self.draw_menu()
        if self.game_manager.game_state == GameState.GAME or self.game_manager.game_state == GameState.LOSE_SCREEN or self.game_manager.game_state == GameState.PAUSE:
            self.draw_game()
        if self.game_manager.game_state == GameState.LOSE_SCREEN:
            self.draw_lose_screen()
        if self.game_manager.game_state == GameState.PAUSE:
            self.draw_pause()
        if self.game_manager.game_state == GameState.HOW_TO_PLAY:
            self.draw_how_to_play()

    def draw_how_to_play(self):
        pyxel.images[1].load(0,0,"assets/ScreenFinal.png")
        pyxel.blt(0,0,1,0,0,256,256)
        pyxel.blt(NEXT_BUTTON[0],NEXT_BUTTON[1],2,0,16*12,NEXT_BUTTON[2],NEXT_BUTTON[3])

        messages_dict = {
            0:"The goal of the game is to\nsurvive as long as possible\nWhen your king is dead\nyou lose the game",
            1:"This is the map.\nMost things happen here",
            2:"When we press with the mouse\nleft mouse button on anything\ndescription with info will be\nshown on bottom screen...",
            3:"For example when we press on\nthe King it will look like\nthis.",
            4:"You can move selected unit with\nmouse+CTRL\nYou can move the king for\nexample",
            5:"Below map is the choice\nbar.\nYou can get resources from here\nand building to build.",
            6:"On the bottom right is \ncalendar..\nIt shows current events",
            7:"After some time\nWaves of enemies will spawn.\nGood luck",
            8:"",
        }

        rects_dict = {
            0: (),
            1: ((0,12*16,16*16,16*4), (12*16,0,16*4,16*16)),
            2: ((0,12*16,16*16,16*4), (12*16,0,16*4,16*16)),
            3: ((12*16,0,16*4,16*16),(0*16,12*16,16*16,16)),
            4: (),
            5: (),
            6: (),
            7: (),
            8: (),
        }
        # Draw current tip:
        pyxel.rect(16*4,0,16*8,16*2+3,7)
        pyxel.rect(16*4,3,16*8-3,16*2-3,0)

        pyxel.text(16*4+4,0+4,messages_dict[self.game_manager.how_page],7)
        for rect in rects_dict[self.game_manager.how_page]:
            pyxel.rect(rect[0],rect[1],rect[2],rect[3],0)

    def draw_menu(self):
        # Draw menu?
        # draw play button
        pyxel.images[1].load(0,0,"assets/MenuArt.png")
        pyxel.blt(0,0,1,0,0,256,256)
        
        pyxel.rect(PLAY_BUTTON[0],PLAY_BUTTON[1],PLAY_BUTTON[2],PLAY_BUTTON[3], 7)
        pyxel.blt(PLAY_BUTTON[0],PLAY_BUTTON[1],2,0,0,PLAY_BUTTON[2],PLAY_BUTTON[3])
        # draw quit button
        pyxel.rect(QUIT_BUTTON[0],QUIT_BUTTON[1],QUIT_BUTTON[2],QUIT_BUTTON[3], 7)
        pyxel.blt(QUIT_BUTTON[0],QUIT_BUTTON[1],2,0,16*2,QUIT_BUTTON[2],QUIT_BUTTON[3])

        pyxel.rect(HOW_TO_PLAY_BUTTON[0],HOW_TO_PLAY_BUTTON[1],HOW_TO_PLAY_BUTTON[2],HOW_TO_PLAY_BUTTON[3], 7)
        pyxel.blt(HOW_TO_PLAY_BUTTON[0],HOW_TO_PLAY_BUTTON[1],2,0,16*10,HOW_TO_PLAY_BUTTON[2],HOW_TO_PLAY_BUTTON[3])

        # Draw game version
        pyxel.text(210, 240, "Version:\n2024.08.24", 7)
        pass
    def draw_lose_screen(self):
        # draw play button
        pyxel.rect(PLAY_AGAIN_BUTTON[0],PLAY_AGAIN_BUTTON[1],PLAY_AGAIN_BUTTON[2],PLAY_AGAIN_BUTTON[3], 7)
        pyxel.blt(PLAY_AGAIN_BUTTON[0],PLAY_AGAIN_BUTTON[1],2,0,16*4,PLAY_AGAIN_BUTTON[2],PLAY_AGAIN_BUTTON[3])
        # draw quit button
        pyxel.rect(GO_TO_MENU_BUTTON[0],GO_TO_MENU_BUTTON[1],GO_TO_MENU_BUTTON[2],GO_TO_MENU_BUTTON[3], 7)
        pyxel.blt(GO_TO_MENU_BUTTON[0],GO_TO_MENU_BUTTON[1],2,0,16*6,GO_TO_MENU_BUTTON[2],GO_TO_MENU_BUTTON[3])
        pass
    def draw_pause(self):
        # draw play button
        pyxel.rect(RESUME_BUTTON[0],RESUME_BUTTON[1],RESUME_BUTTON[2],RESUME_BUTTON[3], 7)
        pyxel.blt(RESUME_BUTTON[0],RESUME_BUTTON[1],2,0,16*8,RESUME_BUTTON[2],RESUME_BUTTON[3])
        
        # Handle Pause
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        (mouse_x, mouse_y) = (pyxel.mouse_x,pyxel.mouse_y)

        if (self.is_in_button(RESUME_BUTTON,mouse_x, mouse_y)):
            self.game_manager.game_state = GameState.GAME
    
    def is_in_rect(self,o_x, o_y ,x, y, w, h):
        if (x<=o_x<=x+w and y<=o_y<=y+h):
            return True
        return False
    def is_in_button(self, button, o_x, o_y):
        (x,y,w,h) = (button[0],button[1],button[2],button[3])
        return self.is_in_rect(o_x, o_y ,x, y, w, h)
    def simulate_menu(self):
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        (mouse_x, mouse_y) = (pyxel.mouse_x,pyxel.mouse_y)

        if (self.is_in_button(PLAY_BUTTON,mouse_x, mouse_y)):
            self.game_reset()
            self.game_manager.game_state = GameState.GAME

        if (self.is_in_button(QUIT_BUTTON,mouse_x, mouse_y)):
            pyxel.quit() 

        if (self.is_in_button(HOW_TO_PLAY_BUTTON,mouse_x, mouse_y)):
            self.game_manager.game_state = GameState.HOW_TO_PLAY 
            self.game_manager.how_page = 0

    def simulate_lose(self):
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        (mouse_x, mouse_y) = (pyxel.mouse_x,pyxel.mouse_y)

        if (self.is_in_button(PLAY_AGAIN_BUTTON,mouse_x, mouse_y)):
            self.game_reset()
            self.game_manager.game_state = GameState.GAME

        if (self.is_in_button(GO_TO_MENU_BUTTON,mouse_x, mouse_y)):
            self.game_manager.game_state = GameState.MENU 
        
    def simulate_how_to_play(self):
        if self.game_manager.how_page > 7:
            self.game_manager.game_state=GameState.MENU
            return
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        (mouse_x, mouse_y) = (pyxel.mouse_x,pyxel.mouse_y)

        if (self.is_in_button(NEXT_BUTTON,mouse_x, mouse_y)):
            self.game_manager.how_page+=1
        
        
    def draw_game(self):
        self.draw_tile_map()
        self.animation_handler.draw_effects(0)

        self.mouse_hover_tile_select()
        self.draw_resources()
        self.choice_manager.draw_choice_pane()
        self.animation_handler.draw_all()
        self.animation_handler.draw_effects(1)

        self.draw_buildings()
        self.placer_manager.draw_selected()
        
        self.draw_hp_bar()

        self.descriptions_manager.draw_selected_description()
        self.event_manager.draw_events()
        self.particle_manager.render_particles()
        
        self.animation_handler.draw_effects(2)

        self.wave_manager.draw()

    def game_reset(self):
        # generate all managers
        
        self.resource_manager = ResourceManager()
        self.tile_manager = TileManager(TILE_MAP_WIDTH=TILE_MAP_WIDTH, TILE_MAP_HEIGHT=TILE_MAP_HEIGHT)
        self.building_manager = BuildingManager(tile_manager=self.tile_manager, resource_manager=self.resource_manager)
        self.placer_manager = PlacerManager(building_manager=self.building_manager)
        self.choice_manager = ChoiceManager(resource_manager=self.resource_manager,
                                            placer_manager=self.placer_manager,
                                            building_manager=self.building_manager,
                                            CHOICE_BAR_SIZE=CHOICE_BAR_SIZE, 
                                            CHOICE_PANE_BASE_X=CHOICE_PANE_BASE_X, 
                                            CHOICE_PANE_BASE_Y=CHOICE_PANE_BASE_Y, 
                                            TILE_WIDTH=TILE_WIDTH,
                                            TILE_HEIGHT=TILE_HEIGHT)
        self.descriptions_manager = DescriptionsManager(placer_manager=self.placer_manager,
                                                        tile_manager=self.tile_manager)
        self.particle_manager = ParticleManager()
        
        self.event_manager = EventManager()
        self.event_manager.building_manager = self.building_manager
        self.event_manager.resource_manager = self.resource_manager

        self.wave_manager = WaveManager(event_manager=self.event_manager)

        self.animation_handler = AnimationHandler()

        # Aditional requirements
        self.choice_manager.event_manager = self.event_manager
        self.choice_manager.animation_manager = self.animation_handler

        self.building_manager.event_manager = self.event_manager
        
        self.event_manager.animation_handler = self.animation_handler

        self.animation_handler.building_manager = self.building_manager
        # post inits
        self.building_manager.post_init()

    def draw_tile_map(self):
        # draw all tiles 
        # For each tile (x,y)
        # - get its type
        # - correct coords
        # - draw it!
        for tile_y in range(TILE_MAP_HEIGHT):
            for tile_x in range(TILE_MAP_WIDTH):
                # get tile draw position:
                tile_draw_x = tile_x*TILE_WIDTH
                tile_draw_y = tile_y*TILE_HEIGHT

                # get tile type:
                tile_type = self.tile_manager.tile_map[tile_y][tile_x]
                # get tile sprite:
                (tile_u, tile_v) = tile_sprites[TileIndex.from_value(tile_type)]

                pyxel.blt(tile_draw_x, tile_draw_y, 0, tile_u, tile_v, TILE_WIDTH, TILE_HEIGHT)
                # pyxel.rect(tile_draw_x, tile_draw_y, TILE_WIDTH, TILE_HEIGHT, (tile_x+tile_y)%16)
    
    def mouse_hover_tile_select(self):
        # handling choice bar
        if (pyxel.mouse_y >= CHOICE_PANE_BASE_Y and pyxel.mouse_y < CHOICE_PANE_BASE_Y+16 and 
            pyxel.mouse_x >= CHOICE_PANE_BASE_X and pyxel.mouse_x < CHOICE_PANE_BASE_X+16*CHOICE_BAR_SIZE):
            # We clicked the choice bar choice:
            hovered_index = int((pyxel.mouse_x - CHOICE_PANE_BASE_X)/16)
            self.choice_manager.hover_over_choice(hovered_index)
            return 
        self.placer_manager.choice_hover = None
        self.placer_manager.choice_hover_event = None

        # cancel button handling:
        if (pyxel.mouse_y >= CHOICE_PANE_BASE_Y and pyxel.mouse_y < CHOICE_PANE_BASE_Y+16 and 
            pyxel.mouse_x > CHOICE_PANE_BASE_X+16*(CHOICE_BAR_SIZE+1) and pyxel.mouse_x < CHOICE_PANE_BASE_X+16*(CHOICE_BAR_SIZE+2)):
            self.placer_manager.cancel_hover = True
            return
        self.placer_manager.cancel_hover = False

        if (pyxel.mouse_x >= TILE_MAP_WIDTH*TILE_WIDTH or pyxel.mouse_y >= TILE_MAP_HEIGHT*TILE_HEIGHT ):
            return
        # Get tile idex_x and y
        tile_y = int(pyxel.mouse_y / TILE_HEIGHT)
        tile_x = int(pyxel.mouse_x / TILE_WIDTH)

        tile_draw_x = tile_x*TILE_WIDTH
        tile_draw_y = tile_y*TILE_HEIGHT

        # load hover mouse sprite?
        (sprite_u, sprite_v) = self.placer_manager.get_placer_icon(tile_y, tile_x)
        if (self.placer_manager.placing_object != None):
            building_being_placed:Building = self.placer_manager.placing_object
            if building_being_placed.radius > 0:
                # Draw rectangle
                rect_x = tile_draw_x - (building_being_placed.radius)*16
                rect_y = tile_draw_y - (building_being_placed.radius)*16
                rect_w = (2*(building_being_placed.radius) +1)*16
                rect_h = (2*(building_being_placed.radius) +1)*16
                pyxel.rectb(rect_x, rect_y, rect_w, rect_h, 7)
        if pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_SPACE):
            if self.placer_manager.selected_object != None and self.placer_manager.selected_object.is_moving_unit and self.placer_manager.selected_object.player_faction:
                if (self.building_manager.try_to_move(tile_x, tile_y)):
                    (sprite_u, sprite_v) = (80,16)
                elif(self.building_manager.try_attack(tile_x, tile_y ,self.placer_manager.selected_object)):
                    (sprite_u, sprite_v) = (112, 16)
                else:
                    (sprite_u, sprite_v) = (96,16)

        pyxel.blt(tile_draw_x, tile_draw_y, 0, sprite_u, sprite_v, TILE_WIDTH, TILE_HEIGHT, 0)
    
    def mouse_click_interaction(self):
        # handling choice bar
        if (pyxel.mouse_y >= CHOICE_PANE_BASE_Y and pyxel.mouse_y < CHOICE_PANE_BASE_Y+16 and 
            pyxel.mouse_x >= CHOICE_PANE_BASE_X and pyxel.mouse_x < CHOICE_PANE_BASE_X+16*CHOICE_BAR_SIZE):
            # We clicked the choice bar choice:
            clicked_index = int((pyxel.mouse_x - CHOICE_PANE_BASE_X)/16)
            self.choice_manager.handle_click(clicked_index=clicked_index)
            return 

        # cancel button handling:
        if (pyxel.mouse_y >= CHOICE_PANE_BASE_Y and pyxel.mouse_y < CHOICE_PANE_BASE_Y+16 and 
            pyxel.mouse_x > CHOICE_PANE_BASE_X+16*(CHOICE_BAR_SIZE+1) and pyxel.mouse_x < CHOICE_PANE_BASE_X+16*(CHOICE_BAR_SIZE+2)):
            self.placer_manager.reset()
            return

        # TODO: we can click somewhere else it will not be the map interaction then
        if (pyxel.mouse_x >= TILE_MAP_WIDTH*TILE_WIDTH or pyxel.mouse_y >= TILE_MAP_HEIGHT*TILE_HEIGHT ):
            return
        # Get tile idex_x and y
        tile_y = int(pyxel.mouse_y / TILE_HEIGHT)
        tile_x = int(pyxel.mouse_x / TILE_WIDTH)
        
        # interaction with map!
        if self.placer_manager.placing_mode == True:
            if (not self.building_manager.can_be_built(self.placer_manager.placing_object, tile_x, tile_y)):
                return
            self.building_manager.build_building(self.placer_manager.placing_object, tile_x, tile_y)
            self.placer_manager.reset()
        elif pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_SPACE):
            # try to move unit
            if self.placer_manager.selected_object != None and self.placer_manager.selected_object.is_moving_unit and self.placer_manager.selected_object.player_faction:
                # Try to move
                if (self.building_manager.try_to_move(tile_x, tile_y)):
                    self.building_manager.set_move_destination(tile_x,tile_y,self.placer_manager.selected_object, from_main=True)
                elif(self.building_manager.try_attack(tile_x, tile_y ,self.placer_manager.selected_object)):
                    self.building_manager.select_attack_target(tile_x, tile_y ,self.placer_manager.selected_object)

        else:
            # we can select something
            self.placer_manager.reset()
            self.placer_manager.select(tile_y=tile_y, tile_x=tile_x)
    
    def draw_resources(self):
        iteration_index = 0
        for resource in ResourcesIndex:
            if not self.resource_manager.is_resource_unlocked[resource]:
                continue
            resource_name = resource_names[resource]
            resource_amount = str(self.resource_manager.resource_amount[resource])
            resource_max = str(self.resource_manager.max_amount[resource])
            
            resource_draw_x = RESOURCES_BASE_X + 1 + 10
            resource_draw_y = RESOURCE_BASE_Y + 10 * iteration_index
            
            pyxel.text(resource_draw_x, resource_draw_y+1, resource_name, 7)
            
            resource_draw_x = RESOURCES_BASE_X + 26 + 18
            pyxel.text(resource_draw_x, resource_draw_y+1, f'{resource_amount}/{resource_max}', 7)
            
            sprite_x, sprite_y = resource_mini_icons[resource]
            pyxel.blt(RESOURCES_BASE_X+1 , resource_draw_y, 0, sprite_x, sprite_y, 8, 8, 0)
            iteration_index+=1

    def draw_buildings(self):
        # get a map from building manager:
        # for all buildings there:
        # get its x,y
        # get its sprite
        # draw building there!
        for building in self.building_manager.building_dict.values():
            building: Building = building
            (sprite_u, sprite_v) = (building.sprite_coords[0], building.sprite_coords[1])
            (tile_x, tile_y) = (building.x, building.y)
            draw_x = TILE_WIDTH*tile_x
            draw_y = TILE_HEIGHT*tile_y
            # pyxel.blt(draw_x, draw_y, 0, sprite_u, sprite_v, TILE_WIDTH, TILE_HEIGHT,0)
            
            # Draw enemy mark!
            if building.is_moving_unit:
                if building.player_faction:
                    if ((pyxel.frame_count+15) % 90 > 75):
                        pyxel.rectb(draw_x, draw_y, TILE_WIDTH, TILE_HEIGHT, 7)
                if not building.player_faction:
                    if (pyxel.frame_count % 90 > 75):
                        pyxel.rectb(draw_x, draw_y, TILE_WIDTH, TILE_HEIGHT, 8)
            
    def draw_hp_bar(self):
        for building in self.building_manager.building_dict.values():
            building: Building = building
            (tile_x, tile_y) = (building.x, building.y)
            draw_x = TILE_WIDTH*tile_x
            draw_y = TILE_HEIGHT*tile_y
            
            # Draw health bar
            if building.current_hp < building.max_hp:
                pyxel.rectb(draw_x, draw_y, TILE_WIDTH, 3, 0)
                pyxel.rect(draw_x+1, draw_y+1, TILE_WIDTH-2, 1, 8)
                hp_percentage = building.current_hp / building.max_hp
                green_bar_width = int((TILE_WIDTH-2) * hp_percentage)

                # Draw the green bar (foreground) - represents current HP
                pyxel.rect(draw_x+1, draw_y+1, green_bar_width, 1, 3)

App()