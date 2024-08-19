import pyxel
import random
from building_manager import BuildingManager
from choice_manager import ChoiceManager
from buildings import Building
from resource_manager import ResourceManager, ResourcesIndex, resource_names, resource_sprites
from placer_manager import PlacerManager
from tile_manager import TileManager, TileIndex, tile_sprites
from descriptions_manager import DescriptionsManager
from buildings import Building
from particles_manager import ParticleManager

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

class TileMap:
    def __init__(self):
        pass
    

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Bubbles", capture_scale=1)
        pyxel.mouse(True)

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

        # load tilemap images:
        pyxel.load("tiles.pyxres")

        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_click_interaction()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.placer_manager.reset()

        self.building_manager.simulate()
        self.choice_manager.simulate()
        

    def draw(self):
        pyxel.cls(0)
        # pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        self.draw_tile_map()
        self.draw_buildings()
        self.mouse_hover_tile_select()
        self.draw_resources()
        self.choice_manager.draw_choice_pane()
        self.placer_manager.draw_selected()
        self.draw_hp_bar()

        self.descriptions_manager.draw_selected_description()
        self.particle_manager.render_particles()
        # pyxel.blt(61, 66, 0, 0, 0, 38, 16)

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
        if pyxel.btn(pyxel.KEY_CTRL):
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
        elif pyxel.btn(pyxel.KEY_CTRL):
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
            resource_name = resource_names[resource]
            resource_amount = str(self.resource_manager.resource_amount[resource])
            resource_max = str(self.resource_manager.max_amount[resource])
            
            resource_draw_x = RESOURCES_BASE_X + 1 + 18
            resource_draw_y = RESOURCE_BASE_Y + 16 * iteration_index
            
            pyxel.text(resource_draw_x, resource_draw_y+6, resource_name, 7)
            
            resource_draw_x = RESOURCES_BASE_X + 26 + 18
            pyxel.text(resource_draw_x, resource_draw_y+6, f'{resource_amount}/{resource_max}', 7)
            
            sprite_x, sprite_y = resource_sprites[resource]
            pyxel.blt(RESOURCES_BASE_X + 1, resource_draw_y, 0, sprite_x, sprite_y, TILE_WIDTH, TILE_HEIGHT, 0)
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
            pyxel.blt(draw_x, draw_y, 0, sprite_u, sprite_v, TILE_WIDTH, TILE_HEIGHT,0)
            
            
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