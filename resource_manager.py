from enum import Enum

class ResourcesIndex(Enum):
    WOOD = 1
    STONE = 2
    FOOD = 3
    IRON = 4
    BLANK_1 = 5
    BLANK_2 = 6
    BLANK_3 = 7
    BLANK_4 = 8
    BLANK_5 = 9
    BLANK_6 = 10
    BLANK_7 = 11
    BLANK_8 = 12

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")

# All BLANK entries share the same sprite as IRON
resource_sprites = {
    ResourcesIndex.WOOD: (16, 32),
    ResourcesIndex.STONE: (0, 32),
    ResourcesIndex.FOOD: (32, 32),
    ResourcesIndex.IRON: (48, 32),
    ResourcesIndex.BLANK_1: (48, 32),
    ResourcesIndex.BLANK_2: (48, 32),
    ResourcesIndex.BLANK_3: (48, 32),
    ResourcesIndex.BLANK_4: (48, 32),
    ResourcesIndex.BLANK_5: (48, 32),
    ResourcesIndex.BLANK_6: (48, 32),
    ResourcesIndex.BLANK_7: (48, 32),
    ResourcesIndex.BLANK_8: (48, 32),
}

# Names for each resource, including the BLANK entries
resource_names = {
    ResourcesIndex.WOOD: "wood",
    ResourcesIndex.STONE: "stone",
    ResourcesIndex.FOOD: "food",
    ResourcesIndex.IRON: "iron",
    ResourcesIndex.BLANK_1: "blank_1",
    ResourcesIndex.BLANK_2: "blank_2",
    ResourcesIndex.BLANK_3: "blank_3",
    ResourcesIndex.BLANK_4: "blank_4",
    ResourcesIndex.BLANK_5: "blank_5",
    ResourcesIndex.BLANK_6: "blank_6",
    ResourcesIndex.BLANK_7: "blank_7",
    ResourcesIndex.BLANK_8: "blank_8",
}


class ResourceManager:
    def __init__(self) -> None:
        
        # for all resources the amount is 0
        self.resource_amount = {resource: 5 for resource in ResourcesIndex}
        self.max_amount = {resource: 10 for resource in ResourcesIndex}

    def increment_resource(self, resource: ResourcesIndex, value: int) -> None:
        if resource not in self.resource_amount:
            raise ValueError(f"Resource {resource} is not valid.")
        
        new_amount = self.resource_amount[resource] + value
        
        if new_amount > self.max_amount[resource]:
            new_amount = self.max_amount[resource]
        
        self.resource_amount[resource] = new_amount
    def get_resource_amount(self, resource: ResourcesIndex):
        return self.resource_amount[resource]