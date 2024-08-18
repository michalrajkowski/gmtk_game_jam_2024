from resource_manager import ResourceManager,ResourcesIndex, resource_sprites
from tile_manager import TileIndex
# jakie cechy powinien mieć base building
# - pozycja
# - sprite pos?
# - cooldown/what it does?

class Building:
    def __init__(self, x=0, y=0):
        self.id = 0
        self.name = "MISSING NAME"
        self.x = x
        self.y = y
        self.sprite_coords = (0, 64)
        self.building_cost = {}
        self.can_be_placed_on = [TileIndex.PLAINS]
        self.description = ""

class House(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "House"
        self.sprite_coords = (16,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 1
        }
        self.description = "- gather resources from neighbour tiles"
class Mine(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Mine"
        self.sprite_coords = (32,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 3
        }
        self.can_be_placed_on = [TileIndex.MONTAIN]
class Fishermans(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Fishermans"
        self.sprite_coords = (48,64)
        self.building_cost = {
            ResourcesIndex.STONE: 0,
            ResourcesIndex.WOOD: 3
        }
        self.can_be_placed_on = [TileIndex.RIVER]
class Tower(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Tower"
        self.sprite_coords = (64,64)
        self.building_cost = {
            ResourcesIndex.STONE: 5,
            ResourcesIndex.WOOD: 2
        }