import pyxel
import random

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

TILE_WIDTH = 16
TILE_HEIGHT = 16
TILE_MAP_WIDTH = 12
TILE_MAP_HEIGHT = 12

class TileMap:
    def __init__(self):
        pass
    

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Bubbles", capture_scale=1)
        pyxel.mouse(True)

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

    def draw(self):
        pyxel.cls(0)
        # pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        self.draw_tile_map()
        self.mouse_hover_tile_select()
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

        # TODO: we can click somewhere else it will not be the map interaction then
        if (pyxel.mouse_x >= TILE_MAP_WIDTH*TILE_WIDTH or pyxel.mouse_y >= TILE_MAP_HEIGHT*TILE_HEIGHT ):
            return
        # Get tile idex_x and y
        tile_y = int(pyxel.mouse_y / TILE_HEIGHT)
        tile_x = int(pyxel.mouse_x / TILE_WIDTH)
        
        # interaction

        # basic interaction - random tile:
        self.tile_map[tile_y][tile_x] = (self.tile_map[tile_y][tile_x]+random.randint(1,3))%4


App()