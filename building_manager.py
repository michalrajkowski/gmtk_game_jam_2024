from buildings import Building
from typing import Dict, Tuple
from tile_manager import TileManager, TileIndex
from buildings import House, Mine, Fishermans, Tower
from resource_manager import ResourceManager
import pyxel

# has array of buildings
# check if they can be built somewhere etc?
# used for simulating them?

class BuildingManager:
    def __init__(self, tile_manager:TileManager, resource_manager:ResourceManager):
        self.resource_manager = resource_manager
        self.tile_manager = tile_manager
        self.building_dict = {
        }
        self.possible_buildings = [
            House(),
            Mine(),
            Fishermans(),
            Tower(),
        ]
    def build_building(self, building: Building, x,y):
        building.x = x
        building.y = y
        self.building_dict[(y,x)] = building

    def draw_building(self, building: Building):
        (tile_x, tile_y) = (building.x, building.y)
        self.draw_selection(tile_x, tile_y)
        
    def draw_selection(self, tile_x, tile_y):
        if (pyxel.frame_count%60 > 30):
            (select_u, select_v) = (48, 16)
        else:
            (select_u, select_v) = (64, 16)
        tile_draw_x = tile_x*16
        tile_draw_y = tile_y*16
        pyxel.blt(tile_draw_x, tile_draw_y, 0, select_u, select_v, 16, 16, 0)

    def is_occupied(self, tile_x, tile_y):
        if (tile_y, tile_x) in self.building_dict:
            return True
        return False
    
    def get_building(self, tile_x, tile_y):
        return self.building_dict[(tile_y, tile_x)]

    def can_be_built(self, building: Building, x,y):
        if (y,x) in self.building_dict:
            return False
        # TODO : check terrain?
        tile_type = TileIndex.from_value(self.tile_manager.tile_map[y][x])
        if not tile_type in building.can_be_placed_on:
            return False
        return True
    
    def check_resources_for_this_building(self, building:Building):
        for resource, cost in building.building_cost.items():
            if self.resource_manager.get_resource_amount(resource=resource) - cost < 0:
                return False
        return True
    def buildings_possible_to_build(self):
        possible_to_build = []
        for building in self.possible_buildings:
            if self.check_resources_for_this_building(building):
                possible_to_build.append(building)
        return possible_to_build
