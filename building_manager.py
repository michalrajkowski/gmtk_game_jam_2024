from buildings import Building
from typing import Dict, Tuple
from tile_manager import TileManager, TileIndex

# has array of buildings
# check if they can be built somewhere etc?
# used for simulating them?

class BuildingManager:
    def __init__(self, tile_manager:TileManager):
        self.tile_manager = tile_manager
        self.building_dict = {
            (3,3): Building(3,3)
        }
    def build_building(self, building: Building, x,y):
        building.x = x
        building.y = y
        self.building_dict[(y,x)] = building

    def can_be_built(self, building: Building, x,y):
        if (y,x) in self.building_dict:
            return False
        # TODO : check terrain?
        return True