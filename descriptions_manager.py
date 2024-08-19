from placer_manager import PlacerManager
from tile_manager import TileManager, TileIndex, tile_sprites, tile_names, tile_descriptions
from buildings import Building
import pyxel
# Render descriptions for choices and other ui thingies. It should probably be white frame with black inside + text?
class DescriptionsManager:
    def __init__(self, placer_manager:PlacerManager, tile_manager: TileManager) -> None:
        self.placer_manager = placer_manager
        self.tile_manager = tile_manager

    
    def draw_selected_description(self):
        pyxel.rectb(0,208, 192, 48, 7)
        if self.placer_manager.cancel_hover!= False:
            (cancel_u, cancel_v) = (48,48)
            pyxel.blt(0 + 3,
                       208 + 3,
                       0, cancel_u, cancel_v, 16, 16)
            pyxel.text(0 + 3 + 16 + 2,
                       208 + 3,
                       "Choices Left / Cancel Building",
                       7)
            pyxel.text(0 + 3 + 16 + 4,
                       208 + 3+ 8,
                       "- shows left choices in queue\n- when building: cancels building",
                       7)
        elif self.placer_manager.choice_hover!= None:
            building :Building= self.placer_manager.choice_hover
            building_sprite = building.sprite_coords
            pyxel.blt(0 + 3,
                       208 + 3,
                       0, building_sprite[0], building_sprite[1],16, 16)
            pyxel.text(0 + 3 + 16 + 2,
                       208 + 3,
                       building.name,
                       7)
            pyxel.text(0 + 3 + 16 + 4,
                       208 + 3+ 8,
                       building.description,
                       7)
        elif self.placer_manager.selected_object != None:
            # draw description for object
            building :Building= self.placer_manager.selected_object
            building_sprite = building.sprite_coords
            pyxel.blt(0 + 3,
                       208 + 3,
                       0, building_sprite[0], building_sprite[1],16, 16)
            pyxel.text(0 + 3 + 16 + 2,
                       208 + 3,
                       building.name,
                       7)
            pyxel.text(0 + 3 + 16 + 2 + 80,
                       208 + 3,
                       f"Hp {building.current_hp}/{building.max_hp}",
                       7)
            pyxel.text(0 + 3 + 16 + 4,
                       208 + 3+ 8,
                       building.description,
                       7)

        elif self.placer_manager.selected_tile != None:
            # draw description for tile
            # draw tile icon
            # draw tile name next to it
            # draw tile description if necesery?
            tile_x = self.placer_manager.selected_tile[0]
            tile_y = self.placer_manager.selected_tile[1]
            tile_index_number = self.tile_manager.tile_map[tile_y][tile_x]
            tile_idx = TileIndex.from_value(tile_index_number)
            tile_name = tile_names[tile_idx]
            tile_sprite = tile_sprites[tile_idx]
            tile_description= tile_descriptions[tile_idx]
            # Draw sprite
            pyxel.blt(0 + 3,
                       208 + 3,
                       0, tile_sprite[0], tile_sprite[1],16, 16)
            pyxel.text(0 + 3 + 16 + 2,
                       208 + 3,
                       tile_name,
                       7)
            pyxel.text(0 + 3 + 16 + 4,
                       208 + 3+ 8,
                       tile_description,
                       7)
        else:
            pyxel.text(0 + 3,
                       208 + 3,
                       "Nothing Selected",
                       7)