import pyxel
import random
from building_manager import BuildingManager
from choice_manager import ChoiceManager
from buildings import Building
from resource_manager import ResourceManager, ResourcesIndex, resource_names, resource_sprites

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
        self.building_manager = BuildingManager()
        self.resource_manager = ResourceManager()
        self.choice_manager = ChoiceManager(resource_manager=self.resource_manager,
                                            CHOICE_BAR_SIZE=CHOICE_BAR_SIZE, 
                                            CHOICE_PANE_BASE_X=CHOICE_PANE_BASE_X, 
                                            CHOICE_PANE_BASE_Y=CHOICE_PANE_BASE_Y, 
                                            TILE_WIDTH=TILE_WIDTH,
                                            TILE_HEIGHT=TILE_HEIGHT)

        self.generate_tile_map()

        # load tilemap images:
        pyxel.load("tiles.pyxres")

        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_click_interaction()

        self.choice_manager.simulate()
        

    def draw(self):
        pyxel.cls(0)
        # pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        self.draw_tile_map()
        self.draw_buildings()
        self.mouse_hover_tile_select()
        self.draw_resources()
        self.choice_manager.draw_choice_pane()
        # pyxel.blt(61, 66, 0, 0, 0, 38, 16)

    def generate_tile_map(self):
        self.tile_map = [[random.randint(0, 3) for _ in range(TILE_MAP_HEIGHT)] for _ in range(TILE_MAP_WIDTH)]
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
                tile_type = self.tile_map[tile_y][tile_x]

                # get tile w,h,u,v
                # w,h = TILE_WIDTH, TILE_HEIGTH
                # u,v = tile_type * tile_size,0 (for now)
                tile_u = tile_type*TILE_WIDTH
                tile_v = 0 

                pyxel.blt(tile_draw_x, tile_draw_y, 0, tile_u, tile_v, TILE_WIDTH, TILE_HEIGHT)
                # pyxel.rect(tile_draw_x, tile_draw_y, TILE_WIDTH, TILE_HEIGHT, (tile_x+tile_y)%16)
    def mouse_hover_tile_select(self):
        # Get the tile x/y which mouse is currently hovering over
        # Draw UI select effect on the tile field
        
        # Get tile x/y:
        # - 
        if (pyxel.mouse_x >= TILE_MAP_WIDTH*TILE_WIDTH or pyxel.mouse_y >= TILE_MAP_HEIGHT*TILE_HEIGHT ):
            return
        # Get tile idex_x and y
        tile_y = int(pyxel.mouse_y / TILE_HEIGHT)
        tile_x = int(pyxel.mouse_x / TILE_WIDTH)

        tile_draw_x = tile_x*TILE_WIDTH
        tile_draw_y = tile_y*TILE_HEIGHT

        # load hover mouse sprite?
        ui_hover_u = 0
        ui_hover_v = 16
        
        pyxel.blt(tile_draw_x, tile_draw_y, 0, ui_hover_u, ui_hover_v, TILE_WIDTH, TILE_HEIGHT, 0)
    
    def mouse_click_interaction(self):
        # get the tile
        if (pyxel.mouse_y >= CHOICE_PANE_BASE_Y and pyxel.mouse_y < CHOICE_PANE_BASE_Y+16 and 
            pyxel.mouse_x >= CHOICE_PANE_BASE_X and pyxel.mouse_x < CHOICE_PANE_BASE_X+16*CHOICE_BAR_SIZE):
            # We clicked the choice bar choice:
            clicked_index = int((pyxel.mouse_x - CHOICE_PANE_BASE_X)/16)
            self.choice_manager.handle_click(clicked_index=clicked_index)
            return 
        
            # handle this click:
            # - update resources based on clicked one
            # - generate new random click resources
            resource_idex = self.choice_bar_choices[clicked_index]
            self.resource_amount[resource_idex]+=1

            self.choice_bar_choices = [random.randint(0,3) for _ in range(self.choice_bar_choices_num)]

        # TODO: we can click somewhere else it will not be the map interaction then
        if (pyxel.mouse_x >= TILE_MAP_WIDTH*TILE_WIDTH or pyxel.mouse_y >= TILE_MAP_HEIGHT*TILE_HEIGHT ):
            return
        # Get tile idex_x and y
        tile_y = int(pyxel.mouse_y / TILE_HEIGHT)
        tile_x = int(pyxel.mouse_x / TILE_WIDTH)
        
        # interaction

        # basic interaction - random tile:
        self.tile_map[tile_y][tile_x] = (self.tile_map[tile_y][tile_x]+random.randint(1,3))%4
    
    def draw_resources(self):
        iteration_index = 0
        for resource in ResourcesIndex:
            # Get the resource name and amount from the ResourceManager
            resource_name = resource_names[resource]
            resource_amount = str(self.resource_manager.resource_amount[resource])
            resource_max = str(self.resource_manager.max_amount[resource])
            
            # Calculate the position to draw the resource name and amount
            resource_draw_x = RESOURCES_BASE_X + 1 + 18
            resource_draw_y = RESOURCE_BASE_Y + 16 * iteration_index # Adjust based on resource type
            
            # Draw the resource name
            pyxel.text(resource_draw_x, resource_draw_y+6, resource_name, 7)
            
            # Draw the resource amount
            resource_draw_x = RESOURCES_BASE_X + 26 + 18
            pyxel.text(resource_draw_x, resource_draw_y+6, f'{resource_amount}/{resource_max}', 7)
            
            # Draw the resource sprite (if needed)
            sprite_x, sprite_y = resource_sprites[resource]
            # Assuming TILE_WIDTH and TILE_HEIGHT are defined elsewhere
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
                

App()