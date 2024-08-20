import pyxel
from buildings import Goblin, Tower
from building_manager import BuildingManager
import random

class Event:
    def __init__(self, x=0, y=0, duration = 1.0, max_action_cooldown = 1.0, draw_event=False):
        self.event_manager = None
        self.building_manager = None
        self.duration = duration
        self.max_duration = self.duration
        self.max_action_cooldown = max_action_cooldown
        self.action_cooldown = self.max_action_cooldown
        self.x = x
        self.y = y
        self.icon = (0,80)
        self.draw_event = draw_event
        self.event_art_path = "assets/elk.jpeg"
        self.name = "MISSING!"


        self.on_start()

    
    def placing_condition(self):
        pass
    
    def on_start(self):
        pass

    def on_end(self):
        pass

    def simulate(self):
        self.action_cooldown -= float(1/30)
        self.duration -= float(1/30)
        if (self.duration <= 0.0):
            self.on_end()
            # delete myself from list
            self.event_manager.event_list.remove(self)
            return
        
        if (self.action_cooldown <= 0.0):
            self.action_cooldown = self.max_action_cooldown
            self.do_event_action()

    def do_event_action(self):
        pass

    def draw(self):
        if (self.draw_event == False):
            return 
        (sprite_u, sprite_v) = (self.icon[0], self.icon[1])
        (tile_x, tile_y) = (self.x, self.y)
        draw_x = 16*tile_x
        draw_y = 16*tile_y
        pyxel.blt(draw_x, draw_y, 0, sprite_u, sprite_v, 16, 16, 0)

class Event_A(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False):
        super().__init__(x, y, duration, max_action_cooldown, draw_event)
        self.icon = (16,80)
        self.duration = 3.0
        self.max_duration = self.duration
        self.name = "AAAA"

class Event_B(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False):
        super().__init__(x, y, duration, max_action_cooldown, draw_event)
        self.icon = (32,80)
        self.duration = 3.0
        self.max_duration = self.duration
        self.event_art_path = "assets/goblin.jpg"
        self.name = "BBBB"

class Goblin_Army(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False):
        super().__init__(x, y, duration, max_action_cooldown, draw_event)
        self.icon = (112,64)
        self.duration = 20.0
        self.max_duration = self.duration
        self.max_action_cooldown = 1.0
        self.action_cooldown = self.max_action_cooldown
        self.event_art_path = "assets/goblin.jpg"
        self.name = "Goblin Army"

    def do_event_action(self):
        # Spawn goblin
        new_goblin = Goblin(0,0)
        # Get spot where to spawn
        x_array = list(range(12))
        random.shuffle(x_array)
        for x in x_array:
            print(x)
            if(self.building_manager.can_be_built(new_goblin,x, 0)):
                self.building_manager.build_building(new_goblin,x,0)
                print("goblin built")
                return
        # Spawn goblin


class EventManager:
    def __init__(self):
        self.event_list = []
        self.building_manager = None
    
    def add_event(self, event):
        print(self.building_manager)
        self.event_list.append(event)
        event.building_manager = self.building_manager
        event.event_manager = self
    
    def simulate(self):
        for event in list(self.event_list):
            event.simulate()

    def draw_events(self):
        for event in list(self.event_list):
            event.draw()