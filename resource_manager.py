from enum import Enum
from tile_manager import TileIndex

class ResourcesIndex(Enum):
    WOOD = 1
    STONE = 2
    FOOD = 3
    LEATHER = 4
    IRON = 5
    GOLD = 6
    MITHRIL = 7
    
    #BLANK_1 = 5
    #BLANK_2 = 6
    #BLANK_3 = 7
    #BLANK_4 = 8
    #BLANK_5 = 9
    #BLANK_6 = 10
    #BLANK_7 = 11
    #BLANK_8 = 12

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")


resources_from_tiles = {
    TileIndex.FOREST : ResourcesIndex.WOOD,
    TileIndex.MONTAIN : ResourcesIndex.STONE,
    TileIndex.RIVER : ResourcesIndex.FOOD
}
# All BLANK entries share the same sprite as IRON
resource_sprites = {
    ResourcesIndex.WOOD: (16, 32),
    ResourcesIndex.STONE: (0, 32),
    ResourcesIndex.FOOD: (32, 32),
    ResourcesIndex.IRON: (48, 32),
    ResourcesIndex.LEATHER: (64, 32),
    ResourcesIndex.GOLD: (80, 32),
    ResourcesIndex.MITHRIL: (96, 32),
}

resource_mini_icons = {
    ResourcesIndex.WOOD: (112, 32),
    ResourcesIndex.STONE: (120, 32),
    ResourcesIndex.FOOD: (112, 40),
    ResourcesIndex.IRON: (120, 40),
    ResourcesIndex.LEATHER: (128, 32),
    ResourcesIndex.GOLD: (136, 32),
    ResourcesIndex.MITHRIL: (128, 40),
}

# Names for each resource, including the BLANK entries
resource_names = {
    ResourcesIndex.WOOD: "wood",
    ResourcesIndex.STONE: "stone",
    ResourcesIndex.FOOD: "food",
    ResourcesIndex.IRON: "iron",
    ResourcesIndex.LEATHER: "leather",
    ResourcesIndex.GOLD: "gold",
    ResourcesIndex.MITHRIL: "mithril",
    #ResourcesIndex.BLANK_1: "blank_1",
    #ResourcesIndex.BLANK_2: "blank_2",
    #ResourcesIndex.BLANK_3: "blank_3",
    #ResourcesIndex.BLANK_4: "blank_4",
    #ResourcesIndex.BLANK_5: "blank_5",
    #ResourcesIndex.BLANK_6: "blank_6",
    #ResourcesIndex.BLANK_7: "blank_7",
    #ResourcesIndex.BLANK_8: "blank_8",
}


class ResourceManager:
    def __init__(self) -> None:
        
        # for all resources the amount is 0
        self.resource_amount = {resource: 0 for resource in ResourcesIndex}
        self.max_amount = {resource: 10 for resource in ResourcesIndex}
        self.is_resource_unlocked = {resource: False for resource in ResourcesIndex}
        self.is_resource_unlocked[ResourcesIndex.WOOD] = True
        self.is_resource_unlocked[ResourcesIndex.FOOD] = True
        self.is_resource_unlocked[ResourcesIndex.STONE] = True

    def increment_resource(self, resource: ResourcesIndex, value: int) -> None:
        if resource not in self.resource_amount:
            raise ValueError(f"Resource {resource} is not valid.")
        
        if self.is_resource_unlocked[resource] == False:
            self.is_resource_unlocked[resource] = True

        new_amount = self.resource_amount[resource] + value
        
        if new_amount > self.max_amount[resource]:
            new_amount = self.max_amount[resource]
        
        self.resource_amount[resource] = new_amount
    def get_resource_amount(self, resource: ResourcesIndex):
        return self.resource_amount[resource]
    
    def change_max_resource(self, value, change_resource= None):
        if change_resource == None:
            for resource in ResourcesIndex:
                self.max_amount[resource] += value
        else:
            self.max_amount[change_resource]+=value