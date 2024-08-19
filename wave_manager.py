from event_manager import Event, EventManager, Event_A, Event_B,Goblin_Army
import random
import copy
import pyxel

possible_events_list = [
    Event_A(), Event_B(), Goblin_Army()
]

class WaveManager:

    def __init__(self, event_manager):
        self.event_list = []
        self.generate_upfront_size = 5
        self.current_event = None
        self.event_manager = event_manager
        self.add_next_events(5)
        self.current_event = self.event_list[0]
        self.next_event_start()
        self.image_art_loaded = False
    
    def simulate(self):
        self.current_event : Event = self.current_event
        #print(self.event_list)
        #print(self.current_event.action_cooldown)
        if (self.current_event.duration <= 0):
            self.next_event_start()

    def next_event_start(self):
        self.event_list.remove(self.current_event)
        self.current_event = self.event_list[0]
        next_event = self.generate_next_event()
        self.event_list.append(next_event)
        self.event_manager.add_event(self.current_event)
        # load next image art
        pyxel.images[1].load(0,0,self.current_event.event_art_path)
    
    def add_next_events(self, how_many_to_add):
        for i in range(how_many_to_add):
            next_event = self.generate_next_event()
            self.event_list.append(next_event)
    
    def generate_next_event(self):
        random_event_template = random.choice(possible_events_list)
        random_event = copy.deepcopy(random_event_template)
        return random_event
    
    def draw(self):
        # Draw upcoming waves + art?
        # Draw events "Bar"
        BASE_X = 12*16
        BASE_Y = 12*16
        # print(self.current_event.duration)
        event_percentage = self.current_event.duration / self.current_event.max_duration
        event_width = int(16 * event_percentage)
        offset_x = event_width - 16
        for i in range(5):
            event = self.event_list[i]
            event : Event = event
            (sprite_u, sprite_v) = (event.icon[0],event.icon[1])
            pyxel.blt(BASE_X+ i*16 +offset_x, BASE_Y, 0, sprite_u, sprite_v, 16, 16)
        # Draw fancy frame
        pyxel.rectb(BASE_X,BASE_Y, 16*4,16,9)
        pyxel.rectb(BASE_X,BASE_Y, 16,16,9)
        pyxel.rectb(BASE_X-1,BASE_Y-1, 16+2,16+2,10)
        pyxel.rect(BASE_X-17,BASE_Y, 16,16,0)

        # Draw event Art
        pyxel.blt(BASE_X, BASE_Y+16, 1, 0,0, 16*4, 16*3)
        pyxel.text(BASE_X+2, BASE_Y-10, f"{self.current_event.name}",7)
