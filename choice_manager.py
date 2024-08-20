import pyxel
import math
import random
from enum import Enum
from resource_manager import ResourceManager,ResourcesIndex, resource_sprites
from buildings import Building, House
from placer_manager import PlacerManager
from building_manager import BuildingManager
from event_manager import EventRarity,Event, EventManager, Goblin_Army, Resource_Event
import copy
# stores current choices
# choices has id and types
# and costs?
# handles what to do next based on clicks?

class Choice:
    def __init__(self) -> None:
        self.sprite_coords = (0, 64)
        self.is_resource_choice = False
        self.is_building_choice = False
        self.is_event_choice = False

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
    def __init__(self, building:Building) -> None:
        super().__init__()
        self.is_building_choice = True
        self.building:Building = building
        self.sprite_coords = building.sprite_coords

class EventChoice(Choice):
    def __init__(self, event:Event) -> None:
        super().__init__()
        self.is_event_choice = True
        self.event = event
        self.sprite_coords = event.icon

events = [

]

events_bars = [
    # Goblins?
    [EventChoice(Goblin_Army()), EventChoice(Goblin_Army()), EventChoice(Goblin_Army()), EventChoice(Goblin_Army())],
    
    # Regular resource
    [EventChoice(Resource_Event(resource_index=ResourcesIndex.WOOD, resource_amount=1)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.STONE, resource_amount=1)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.FOOD, resource_amount=1)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.IRON, resource_amount=1)),]
]

legendary_events = [
    # Supreme Supreme resource
    [EventChoice(Resource_Event(resource_index=ResourcesIndex.WOOD, resource_amount=99)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.STONE, resource_amount=99)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.FOOD, resource_amount=99)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.IRON, resource_amount=25)),],
]

rare_events = [
    # Supreme resource
    [EventChoice(Resource_Event(resource_index=ResourcesIndex.WOOD, resource_amount=10)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.STONE, resource_amount=10)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.FOOD, resource_amount=10)),
     EventChoice(Resource_Event(resource_index=ResourcesIndex.IRON, resource_amount=5)),],
]

common_events = [

]

class ChoiceManager:
    def __init__(self, CHOICE_BAR_SIZE,CHOICE_PANE_BASE_X,CHOICE_PANE_BASE_Y,TILE_WIDTH,TILE_HEIGHT,resource_manager:ResourceManager,
                 placer_manager:PlacerManager,
                 building_manager:BuildingManager) -> None:
        self.building_manager = building_manager
        self.resource_manager=resource_manager
        self.event_manager=None
        self.placer_manager = placer_manager
        self.CHOICE_PANE_BASE_X = CHOICE_PANE_BASE_X
        self.CHOICE_PANE_BASE_Y = CHOICE_PANE_BASE_Y
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT

        self.choice_bar_size = CHOICE_BAR_SIZE
        self.choice_bar = None
        self.cooldown = 5.0
        self.max_cooldown = 5.0
        self.choice_queue = []
        self.max_choice_queue = 4
        self.extra_choices = []
        self.press_max_cooldown = 0.01
        self.press_current_cooldown = 0.0

        self.legendary_chance = 1
        self.rare_chance = 5
        self.common_chance = 80

        self.this_choice_rarity = None
        self.event_source_name = None
    
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
            this_choice = None
            if self.choice_bar == None:
                temp_choicebar = [NullChoice() for _ in range(self.choice_bar_size)]
                this_choice = temp_choicebar[i]
            else:
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

        # Draw cancel button
        if self.placer_manager.placing_mode == True:
            choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*(self.choice_bar_size+1)
            choice_draw_y = self.CHOICE_PANE_BASE_Y
            (tile_u, tile_v) = (48,48)
            pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT)
        else:
            # Draw spare choices
            choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*(self.choice_bar_size+1)
            choice_draw_y = self.CHOICE_PANE_BASE_Y
            # (tile_u, tile_v) = (48,48)
            # pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT)
            (tile_u, tile_v) = (32,48)
            pyxel.blt(choice_draw_x, choice_draw_y, 0, tile_u, tile_v, self.TILE_WIDTH, self.TILE_HEIGHT)
            spare_choices_number_str = str(len(self.choice_queue))
            pyxel.text(choice_draw_x+2, choice_draw_y+5, f"{spare_choices_number_str}/{self.max_choice_queue}",7)

        # Draw choice name and its rarity
        color_index = {
            EventRarity.COMMON: 7,
            EventRarity.RARE: 2,
            EventRarity.LEGENDARY: 9,
        }

        choice_name = {
            EventRarity.COMMON: "Common Choice",
            EventRarity.RARE: "Rare Choice",
            EventRarity.LEGENDARY: "LEGENDARY CHOICE",
        }

        if self.choice_bar == None:
            choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*(self.choice_bar_size+1)
            choice_draw_y = self.CHOICE_PANE_BASE_Y
            pyxel.text(choice_draw_x+18, choice_draw_y+2, f"Wait for next choice",13)
        else:
            # Draw 
            choice_draw_x = self.CHOICE_PANE_BASE_X + self.TILE_WIDTH*(self.choice_bar_size+1)
            choice_draw_y = self.CHOICE_PANE_BASE_Y
            draw_text_rarity = choice_name[self.this_choice_rarity]
            draw_text_color = color_index[self.this_choice_rarity]
            pyxel.text(choice_draw_x+18, choice_draw_y+2, draw_text_rarity,draw_text_color)
            if self.event_source_name != None:
                pyxel.text(choice_draw_x+20, choice_draw_y+9, self.event_source_name, 7)


    def handle_click(self, clicked_index):
        if self.press_current_cooldown >= 0.0:
            # play sound?
            return
        if self.choice_bar == None:
            return
        
        this_choice : Choice = self.choice_bar[clicked_index]
        if this_choice.is_event_choice:
            this_choice: EventChoice = this_choice

            # add event to queue
            self.event_manager : EventManager = self.event_manager
            self.event_manager.add_event(this_choice.event)

            self.choice_queue.remove(self.choice_bar)
            self.choice_bar = None
            self.try_get_choicebar_from_queue()
        elif this_choice.is_building_choice:
            # decrement resources
            this_choice: BuildingChoice = this_choice
    
            for resource, cost in this_choice.building.building_cost.items():
                self.resource_manager.increment_resource(resource, -1*cost)
            # enter placing mode with this building
            self.placer_manager.placing_mode=True
            self.placer_manager.placing_object = this_choice.building

            # clear choice bar
            self.choice_queue.remove(self.choice_bar)
            self.choice_bar = None
            self.try_get_choicebar_from_queue()
            return
        elif this_choice.is_resource_choice:
            # increment resource 
            # set all choices to null
            this_choice: ResourceChoice = this_choice
            self.resource_manager.increment_resource(ResourcesIndex.from_value(this_choice.resource_type), this_choice.resource_amount)
            
            # clear choice bar
            self.choice_queue.remove(self.choice_bar)
            self.choice_bar = None
            self.try_get_choicebar_from_queue()
        else:
            # null choice
            return
    def hover_over_choice(self, hover_index):
        if self.choice_bar == None:
            return
        this_choice : Choice = self.choice_bar[hover_index]
        if this_choice.is_building_choice:
            # decrement resources
            this_choice: BuildingChoice = this_choice
            this_choice_building = this_choice.building
            self.placer_manager.choice_hover = this_choice_building
        if this_choice.is_event_choice:
            # decrement resources
            this_choice: Event = this_choice
            this_choice_event = this_choice.event
            self.placer_manager.choice_hover_event = this_choice_event
            
    def simulate(self):
        self.cooldown -= float(1/30)
        self.press_current_cooldown -= float(1/30)
        if self.cooldown <= 0:
            self.cooldown = self.max_cooldown
            if len(self.choice_queue) < self.max_choice_queue:
                self.choice_queue.append(None)
        if self.choice_bar == None:
            self.try_get_choicebar_from_queue()
    
    def try_get_choicebar_from_queue(self):
        if len(self.choice_queue) != 0:
            # Get event!!!
            new_choice_bar = self.choice_queue[0]
            if new_choice_bar == None:
                new_choice_bar = self.generate_choices()
                self.choice_queue.pop(0)
                self.choice_queue.insert(0, new_choice_bar)
            else:
                # ADD EVENT BUNDLE TO CHOICEBAR IF ADDED FROM SOMEWHERE ELSE
                event_bundle = new_choice_bar
                self.this_choice_rarity = event_bundle[1]
                self.event_source_name = event_bundle[2]
                new_choice_bar = event_bundle[0]

            self.choice_bar = new_choice_bar
            # Epic animations depending on rarity?

            self.press_current_cooldown = self.press_max_cooldown
        # else:
        #    self.choice_bar = [NullChoice() for _ in range(self.choice_bar_size)]
    def get_weighted_result(self, weights, results):
        cumulative_weights = []
        current_sum = 0
        for weight in weights:
            current_sum += weight
            cumulative_weights.append(current_sum)
        
        # Generate a random number between 0 and the sum of all weights
        total_weight = cumulative_weights[-1]
        random_num = random.uniform(0, total_weight)
        
        # Determine which choice corresponds to the random number
        for i, cumulative_weight in enumerate(cumulative_weights):
            if random_num <= cumulative_weight:
                return results[i]

    def generate_choices(self):
        # find what buildings can be built

        # Basic event,
        # Rare event,
        # Legendary event,

        # Basic event:
        # - generate event rarity
        # - find what can be built
        # - 
        # Generate current event rarity:
        weights = [self.common_chance, self.rare_chance, self.legendary_chance]
        results = [EventRarity.COMMON,EventRarity.RARE,EventRarity.LEGENDARY]
        
        event_rarity = self.get_weighted_result(weights, results)
        

        # Generate temp bar
        temp_choice_bar = []
        self.this_choice_rarity = event_rarity
        self.event_source_name = None

        if event_rarity == EventRarity.LEGENDARY:
            # regular events list?
            random_index = random.randint(0, len(legendary_events)-1)
            temp_choice_bar = copy.deepcopy(legendary_events[random_index])
            return temp_choice_bar

        if event_rarity == EventRarity.RARE:
            random_index = random.randint(0, len(legendary_events)-1)
            temp_choice_bar = copy.deepcopy(rare_events[random_index])
            return temp_choice_bar

        
        possible_to_build = self.building_manager.buildings_possible_to_build()
        # choice len = len(possible_to_build)
        
        # unlocked_buildings_lits?

        # First field is always a resource?
        for i in range(self.choice_bar_size):
            if i == 0 or i > len(possible_to_build):
                # gen resource:
                # TODO chooses from all items, needs some filtrations maybe?
                random_choice=random.random()
                if random_choice > 0.66:
                    choice = EventChoice(Resource_Event(resource_index=ResourcesIndex.FOOD, resource_amount=1))
                elif random_choice > 0.33:
                    choice = EventChoice(Resource_Event(resource_index=ResourcesIndex.STONE, resource_amount=1))
                else:
                    choice = EventChoice(Resource_Event(resource_index=ResourcesIndex.WOOD, resource_amount=1))
                temp_choice_bar.append(choice)

            else:
                # generate building
                building_choice = random.randint(0, len(possible_to_build)-1)
                choosen_building = copy.deepcopy(possible_to_build[building_choice])
                new_building = choosen_building
                choice = BuildingChoice(new_building)
                temp_choice_bar.append(choice)
        random.shuffle(temp_choice_bar)
        return temp_choice_bar