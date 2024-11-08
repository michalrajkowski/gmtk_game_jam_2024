import pyxel
from buildings import Goblin, Tower, Necromancer
from building_manager import BuildingManager
import random
from resource_manager import ResourcesIndex, resource_names, resource_sprites, resource_mini_icons
from enum import Enum
from animation_handler import Point
class TimePhase(Enum):
    DAY = 0
    NIGHT = 1
    NONE = 2


class EventRarity(Enum):
    COMMON = 0
    RARE = 1
    LEGENDARY = 2

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid value: {value}")

class Event:
    def __init__(self, x=0, y=0, duration = 1.0, max_action_cooldown = 1.0, draw_event=False, event_source=None, time_phase=None):
        self.event_manager = None
        self.building_manager = None
        self.resource_manager = None
        self.animation_handler = None
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
        self.description = ""
        self.first_tick = True
        self.event_source = event_source
        self.time_phase = time_phase if time_phase!=None else TimePhase.NONE

    
    def placing_condition(self):
        pass
    
    def on_start(self):
        pass

    def on_end(self):
        pass

    def simulate(self):
        if self.first_tick:
            self.first_tick = False
            self.on_start()
        
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
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (16,80)
        self.duration = 3.0
        self.max_duration = self.duration
        self.name = "AAAA"

class Event_B(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (32,80)
        self.duration = 3.0
        self.max_duration = self.duration
        self.event_art_path = "assets/goblin.jpg"
        self.name = "BBBB"

class Resource_Event(Event):
    def __init__(self, resource_index:ResourcesIndex, resource_amount=1,x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.resource_index = resource_index
        self.resource_amount = resource_amount
        self.icon = resource_sprites[resource_index]
        self.duration = 3.0
        self.max_duration = self.duration
        self.event_art_path = "assets/goblin.jpg"
        self.description = f"- Increase {resource_names[resource_index]} by {self.resource_amount}"
        self.name = f"Resource {resource_names[resource_index]} +{self.resource_amount}"

    def on_start(self):
        # Add resource
        self.resource_manager.increment_resource(self.resource_index, self.resource_amount)


class Goblin_Army(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (112,64)
        self.duration = 20.0
        self.max_duration = self.duration
        self.max_action_cooldown = 1.0
        self.action_cooldown = self.max_action_cooldown
        self.goblin_army_spawn_duration = 15.0
        self.event_art_path = "assets/goblin.jpg"
        self.name = "Goblin Army"

    def do_event_action(self):
        if self.duration <= self.goblin_army_spawn_duration:
            return
        # Spawn goblin
        new_goblin = Goblin(0,0)
        # Get spot where to spawn
        x_array = list(range(12))
        random.shuffle(x_array)
        for x in x_array:
            if(self.building_manager.can_be_built(new_goblin,x, 0)):
                self.building_manager.build_building(new_goblin,x,0)
                return
        # Spawn goblin

class Peacefull_Day(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (112,80)
        self.duration = 1.0#20.0
        self.max_duration = self.duration
        self.max_action_cooldown = 1.0
        self.action_cooldown = self.max_action_cooldown
        self.goblin_army_spawn_duration = 15.0
        self.event_art_path = "assets/day.jpg"
        self.name = "Peacefull Day"
        self.description = "The night has ended\nSunlight will be thier doom!"
        self.time_phase = TimePhase.DAY

    def do_event_action(self):
        pass

class Peacefull_Night(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (128,80)
        self.duration = 1.0#20.0
        self.max_duration = self.duration
        self.max_action_cooldown = 1.0
        self.action_cooldown = self.max_action_cooldown
        self.goblin_army_spawn_duration = 15.0
        self.event_art_path = "assets/day.jpg"
        self.name = "Peacefull Night"
        self.time_phase = TimePhase.NIGHT

    def do_event_action(self):
        pass

class Undead_Army(Event):
    def __init__(self, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.icon = (64,80)
        self.duration = 20.0
        self.max_duration = self.duration
        self.max_action_cooldown = 1.0
        self.action_cooldown = self.max_action_cooldown
        self.necro_number = 1
        self.event_art_path = "assets/skeletons.jpeg"
        self.name = "Undead Army"

    def on_start(self):
        super().on_start()
        # Spawn 3 necromancers
        for i in range(self.necro_number):

            new_necromancer = Necromancer(0,0)
            # Get spot where to spawn
            x_array = list(range(12))
            random.shuffle(x_array)
            for x in x_array:
                if(self.building_manager.can_be_built(new_necromancer,x, 11)):
                    self.building_manager.build_building(new_necromancer,x,11)
                    break

class MeleeAttack_Event(Event):
    def __init__(self, object_original, object_target, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.object_original = object_original
        self.object_target = object_target
    
    def on_start(self):
        from animation_handler import MeleeAttackAnimation, AnimationHandler
        super().on_start()
        # Spawn animation?
        attack_animation = MeleeAttackAnimation(self.object_original, self.object_target, self.duration) # We multiply by 1.5 coz during 66% animation time we attack
        self.animation_handler: AnimationHandler = self.animation_handler
        self.animation_handler.add_animation(attack_animation)
        

    def on_end(self):
        from buildings import Building
        super().on_end()
        # Deal damage?
        self.object_original.end_attack()

    def do_event_action(self):
        from buildings import Building
        super().do_event_action()
        # Deal damage?
        self.object_original : Building = self.object_original
        self.object_original.deal_damage(self.object_target, self.object_original.attack_damage)

class DamageHit_event(Event):
    def __init__(self, object_original, x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.object_original = object_original
    
    def on_start(self):
        from animation_handler import Hit_Effect, AnimationHandler
        super().on_start()
        # Spawn animation?
        hit_effect = Hit_Effect(self.object_original, self.duration) # We multiply by 1.5 coz during 66% animation time we attack
        self.animation_handler: AnimationHandler = self.animation_handler
        self.animation_handler.add_effect(hit_effect)

class DrawText_event(Event):
    def __init__(self,object_assigned_to=None, text="", color=7, image_icon = None, image_size=(8,8)  ,x=0, y=0, duration=1, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        if object_assigned_to == None:
            object_assigned_to = Point(10,10)    
        self.object_assigned_to = object_assigned_to
        self.text = text
        self.color = color
        self.image_icon = image_icon
        self.image_size = image_size

    def on_start(self):
        from animation_handler import Text_effect
        super().on_start()
        text_effect = Text_effect(self.object_assigned_to, self.duration,self.text, self.color,self.image_icon, self.image_size)
        self.animation_handler.add_effect(text_effect)
        self.duration = -1
    

class DrawResource_event(Event):
    def __init__(self, tile, resource : ResourcesIndex, amount ,x=0, y=0, duration=0, max_action_cooldown=1, draw_event=False, event_source=None):
        super().__init__(x, y, duration, max_action_cooldown, draw_event, event_source)
        self.tile = tile
        self.resource = resource
        self.amount = amount
    def on_start(self):
        super().on_start()
        for event in self.event_manager.event_list:
            if event.event_source == None:
                continue
            if event.event_source != self.event_source:
                continue
            if event.first_tick == False:
                continue
            self.duration+=0.4
        # Look for simmilar events in event list
        # Get the greatest duration from them
        # this_duration should be the greatest duration + 0.2
        print(self.duration)
    def on_end(self):
        resource_name = resource_names[self.resource]
        resource_string = f"+{self.amount}{resource_name}"
        resource_icon = resource_mini_icons[self.resource]
        point = Point(self.tile[0]*16, self.tile[1]*16)
        text_event = DrawText_event(point, resource_string, image_icon=resource_icon, image_size=(8,8))
        self.event_manager.add_event(text_event)
        return super().on_end()

class EventManager:
    def __init__(self):
        self.event_list = []
        self.building_manager = None
        self.resource_manager = None
        self.animation_handler = None
    
    def add_event(self, event):
        self.event_list.append(event)
        event.building_manager = self.building_manager
        event.resource_manager = self.resource_manager
        event.event_manager = self
        event.animation_handler = self.animation_handler
    
    def simulate(self):
        for event in list(self.event_list):
            event.simulate()

    def draw_events(self):
        for event in list(self.event_list):
            event.draw()
