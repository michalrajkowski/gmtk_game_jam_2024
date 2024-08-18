from enum import Enum
import random

class TileIndex(Enum):
    PLAINS = 0
    FOREST = 1
    MONTAIN = 2
    RIVER = 3

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")
    
tile_sprites = {
    TileIndex.PLAINS : (0,0),
    TileIndex.FOREST : (32,0),
    TileIndex.MONTAIN : (16,0),
    TileIndex.RIVER : (48,0),
}

tile_names = {
    TileIndex.PLAINS : "Plains",
    TileIndex.FOREST : "Forest",
    TileIndex.MONTAIN : "Montain",
    TileIndex.RIVER : "River",
}

tile_descriptions = {
    TileIndex.PLAINS : "- good for placing buildings\n- does not produce any resource",
    TileIndex.FOREST : "- source of Wood",
    TileIndex.MONTAIN : "- source of Stone\n- hides rare ores and gems",
    TileIndex.RIVER : "- source of Food",
}
class TileManager:
    def __init__(self, TILE_MAP_WIDTH, TILE_MAP_HEIGHT) -> None:
        self.TILE_MAP_WIDTH = TILE_MAP_WIDTH
        self.TILE_MAP_HEIGHT = TILE_MAP_HEIGHT
        self.generate_tilemap()

    def generate_tilemap(self):
        self.tile_map = [[0 for _ in range(self.TILE_MAP_HEIGHT)] for _ in range(self.TILE_MAP_WIDTH)]
        for y in range(0, self.TILE_MAP_HEIGHT):
            for x in range(0, self.TILE_MAP_WIDTH):
                plane_chance = 0.75
                if (random.random() > plane_chance):
                    self.tile_map[y][x] = random.randint(1,3)

    def is_in_tilemap(self, x, y):
        if (0 <= x < 12 and 0 <= y < 12):
            return True
        return False
    def get_neigbour_tiles(self, point_x,point_y,radius):
        nei_tiles=[]
        for y in range(point_y - radius, point_y+radius+1):
            for x in range(point_x - radius, point_x + radius+1):
                if (not self.is_in_tilemap(x,y)):
                    continue
                if (x == point_x and y == point_y):
                    continue
                nei_tiles.append(self.tile_map[y][x])
        return nei_tiles