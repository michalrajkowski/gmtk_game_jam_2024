import pyxel
import math
import random
from enum import Enum
from resource_manager import ResourceManager,ResourcesIndex, resource_sprites
# stores current choices
# choices has id and types
# and costs?
# handles what to do next based on clicks?

class Choice:
    def __init__(self) -> None:
        self.sprite_coords = (0, 64)
        self.is_resource_choice = False
        self.is_building_choice = False

class NullChoice(Choice):
    def __init__(self) -> None:
        super().__init__()
        self.sprite_coords = (16,48)


class ResourceChoice(Choice):
    def __init__(self, resource_type=0, resource_amount=1) -> None:
        super().__init__()
        self.is_resource_choice = True
        self.resource_type = resource_type
        self.resource_amount = resource_amount
        resource_enum = ResourcesIndex(resource_type)
        self.sprite_coords = resource_sprites[resource_enum]

class BuildingChoice(Choice):
    def __init__(self) -> None:
        super().__init__()
        self.is_building_choice = True

class ChoiceManager:
    def __init__(self, CHOICE_BAR_SIZE,CHOICE_PANE_BASE_X,CHOICE_PANE_BASE_Y,TILE_WIDTH,TILE_HEIGHT,resource_manager:ResourceManager) -> None:
        self.resource_manager=resource_manager
        self.CHOICE_PANE_BASE_X = CHOICE_PANE_BASE_X
        self.CHOICE_PANE_BASE_Y = CHOICE_PANE_BASE_Y
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT

        self.choice_bar_size = CHOICE_BAR_SIZE
        self.choice_bar = [NullChoice() for _ in range(self.choice_bar_size)]
        self.cooldown = 3.0
        self.max_cooldown = 3.0
    
    def draw_choice_pane(self):
        for i in range(self.choice_bar_size):
            choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*i
            choice_draw_y = self.CHOICE_PANE_BASE_Y
            

            # draw choice frame:
            tile_u = 0
            tile_v = 3*self.TILE_WIDTH
            pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT)

            # draw choice bar choices:

            # draw correct choice resource
            # choose this choice sprite:
            this_choice : Choice = self.choice_bar[i]
            (tile_u, tile_v) = (this_choice.sprite_coords[0], this_choice.sprite_coords[1])
            pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT,0)

        # draw cooldown field:
        # draw field temp
        # get int number and draw it
        # (draw circle around the cooldown number? (That is percent filled))
        choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*self.choice_bar_size
        choice_draw_y = self.CHOICE_PANE_BASE_Y
        (tile_u, tile_v) = (32,48)
        pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT)
        # draw number
        number_int = str(int(self.cooldown))
        if self.cooldown < 10.0:
            number_int = str(round(self.cooldown, 1))
        pyxel.text(choice_draw_x+3, choice_draw_y+5, number_int, 7)

    def handle_click(self, clicked_index):
        this_choice : Choice = self.choice_bar[clicked_index]
        if this_choice.is_building_choice:
            pass
        elif this_choice.is_resource_choice:
            # increment resource 
            # set all choices to null
            this_choice: ResourceChoice = this_choice
            self.resource_manager.increment_resource(ResourcesIndex.from_value(this_choice.resource_type), this_choice.resource_amount)
            self.choice_bar = [NullChoice() for _ in range(self.choice_bar_size)]
        else:
            # null choice
            pass

    def simulate(self):
        self.cooldown -= float(1/30)
        if self.cooldown <= 0:
            self.cooldown = self.max_cooldown
            self.generate_choices()

    def generate_choices(self):
        for i in range(self.choice_bar_size):
            resource_type = random.choice(list(ResourcesIndex)).value
            choice = ResourceChoice(resource_type=resource_type)
            self.choice_bar[i] = choice


    