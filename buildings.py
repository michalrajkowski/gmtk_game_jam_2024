from resource_manager import ResourceManager,ResourcesIndex, resource_sprites
# jakie cechy powinien mieć base building
# - pozycja
# - sprite pos?
# - cooldown/what it does?

class Building:
    def __init__(self, x, y):
        self.id = 0
        self.name = "MISSING NAME"
        self.x = x
        self.y = y
        self.sprite_coords = (0, 64)
        self.building_cost = {}

class House(Building):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "House"
        self.sprite_coords = (16,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 1
        }
