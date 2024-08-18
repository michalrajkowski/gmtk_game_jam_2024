from building_manager import BuildingManager
placer_icons = {
    "default": (0, 16),
    "building": (16,16),
    "building_invalid": (32, 16) 
}

class PlacerManager:
    def __init__(self, building_manager:BuildingManager) -> None:
        self.placing_mode = False
        self.placing_object = None
        self.building_manager = building_manager

    def reset(self):
        self.placing_mode = False
        self.placing_object = None

    def get_placer_icon(self, tile_y, tile_x):
        if (self.placing_mode == False):
            return placer_icons["default"]
        can_be_built = self.building_manager.can_be_built(self.placing_object, tile_x, tile_y)
        if (can_be_built == True):
            return placer_icons["building"]
        else:
            return placer_icons["building_invalid"]