from enum import Enum

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
class TileManager:
    def __init__(self, TILE_MAP_WIDTH, TILE_MAP_HEIGHT) -> None:
        self.TILE_MAP_WIDTH = TILE_MAP_WIDTH
        self.TILE_MAP_HEIGHT = TILE_MAP_HEIGHT
        self.generate_tilemap()

    def generate_tilemap(self):
        self.tile_map = [[0 for _ in range(self.TILE_MAP_HEIGHT)] for _ in range(self.TILE_MAP_WIDTH)]