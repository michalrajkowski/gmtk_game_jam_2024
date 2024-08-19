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
        
        self.selected_tile = None
        self.selected_object = None
        
        self.choice_hover = None
        self.cancel_hover = False

    def reset(self):
        self.placing_mode = False
        self.placing_object = None
        self.selected_tile = None
        self.selected_object = None

    def get_placer_icon(self, tile_y, tile_x):
        if (self.placing_mode == False):
            return placer_icons["default"]
        can_be_built = self.building_manager.can_be_built(self.placing_object, tile_x, tile_y)
        if (can_be_built == True):
            return placer_icons["building"]
        else:
            return placer_icons["building_invalid"]
    
    def select(self, tile_y, tile_x):
        if self.building_manager.is_occupied(tile_x=tile_x, tile_y=tile_y):
            self.selected_object = self.building_manager.get_building(tile_x=tile_x, tile_y=tile_y)
        self.selected_tile = (tile_x, tile_y)

    def draw_selected(self):
        if self.selected_object != None:
            self.building_manager.draw_selection_building(self.selected_object)
        elif self.selected_tile != None:
            self.building_manager.draw_selection(self.selected_tile[0], self.selected_tile[1])