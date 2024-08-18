from enum import Enum


class ResourcesIndex(Enum):
    WOOD = 1
    STONE = 2
    FOOD = 3
    IRON = 4

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")

resource_sprites = {
    ResourcesIndex.WOOD: (16, 32),
    ResourcesIndex.STONE: (0, 32),
    ResourcesIndex.FOOD: (32, 32),
    ResourcesIndex.IRON: (48, 32),
}

resource_names = {
    ResourcesIndex.WOOD: "wood",
    ResourcesIndex.STONE: "stone",
    ResourcesIndex.FOOD: "food",
    ResourcesIndex.IRON: "iron",
}

class ResourceManager:
    def __init__(self) -> None:
        
        # for all resources the amount is 0
        self.resource_amount = {resource: 0 for resource in ResourcesIndex}
        self.max_amount = {resource: 10 for resource in ResourcesIndex}

    def increment_resource(self, resource: ResourcesIndex, value: int) -> None:
        if resource not in self.resource_amount:
            raise ValueError(f"Resource {resource} is not valid.")
        
        new_amount = self.resource_amount[resource] + value
        
        if new_amount > self.max_amount[resource]:
            new_amount = self.max_amount[resource]
        
        self.resource_amount[resource] = new_amount