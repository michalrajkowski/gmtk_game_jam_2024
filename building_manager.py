from buildings import Building
from typing import Dict, Tuple
from tile_manager import TileManager, TileIndex
from buildings import House, Mine, Fishermans, Tower, MovingUnit, King
from resource_manager import ResourceManager
import pyxel
from collections import deque

# has array of buildings
# check if they can be built somewhere etc?
# used for simulating them?

class BuildingManager:
    def __init__(self, tile_manager:TileManager, resource_manager:ResourceManager):
        self.resource_manager = resource_manager
        self.tile_manager = tile_manager
        self.building_dict = {
            (6,6):King(6,6)
        }
        self.possible_buildings = [
            House(),
            Mine(),
            Fishermans(),
            Tower(),
        ]

    def simulate(self):
        to_move_list = []
        for building in self.building_dict.values():
            building.simulate_building()
            if building.is_moving_unit:
                building :MovingUnit= building
                if building.move_me == True:
                    building.move_me = False
                    if building.moving_destination == None:
                        continue
                    # move unit next step
                    to_move_list.append(building)
        for building in to_move_list:
            (move_x, move_y) = self.generate_next_move_step(building=building)
            if (move_x == -1):
                continue
            # move to the next move step!
            self.move_building(building, move_x, move_y)
            if (move_x == building.moving_destination[0] and move_y == building.moving_destination[1]):
                building.moving_destination=None

    def move_building(self, building: Building, new_x, new_y):
        dict_key = (building.y, building.x)
        del self.building_dict[dict_key]
        building.x = new_x
        building.y = new_y
        self.building_dict[(new_y,new_x)] = building

    def build_building(self, building: Building, x,y):
        building.x = x
        building.y = y
        self.building_dict[(y,x)] = building
        building.resource_manager = self.resource_manager
        building.tile_manager = self.tile_manager

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

    def try_to_move(self, tile_x, tile_y):
        if self.is_occupied(tile_x, tile_y):
            return False
        return True
    
    # Function that finds path between current position of unit and the move goal of it
    def generate_next_move_step(self, building:MovingUnit):
        path = self.bfs_shortest_path(building.x, building.y, building.moving_destination[0], building.moving_destination[1])
        if (len(path) > 0):
            return path[1]
        return (-1, -1)
    
    def bfs_shortest_path(self, start_x, start_y, goal_x, goal_y):
        # Directions for moving in 4 possible directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Initialize BFS queue and visited set
        queue = deque([(start_x, start_y)])
        visited = set()
        visited.add((start_x, start_y))
        
        # Dictionary to store the parent of each node to reconstruct the path
        parent = {}
        
        while queue:
            x, y = queue.popleft()
            
            # Check if the goal is reached
            if (x, y) == (goal_x, goal_y):
                # Reconstruct the path from goal to start using the parent dictionary
                path = []
                while (x, y) != (start_x, start_y):
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.append((start_x, start_y))
                path.reverse()  # Reverse the path to start from the beginning
                return path
            
            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check if the new position is within bounds and not visited
                if 0 <= nx < 12 and 0 <= ny < 12 and (nx, ny) not in visited and self.try_to_move(nx, ny):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
        
        # If the goal is not reachable, return an empty list
        return []

    def set_move_destination(self, tile_x, tile_y, building:Building):
        building : MovingUnit = building
        building.moving_destination = (tile_x, tile_y)

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
