from resource_manager import ResourceManager,ResourcesIndex, resource_sprites, resources_from_tiles, resource_names
from tile_manager import TileIndex, TileManager
from particles_manager import ParticleManager
import random
# jakie cechy powinien mieć base building
# - pozycja
# - sprite pos?
# - cooldown/what it does?

class Building:
    def __init__(self, x=0, y=0):
        self.resource_manager: ResourceManager = None
        self.tile_manager: TileManager = None
        self.particle_manager = ParticleManager()
        self.building_manager = None
        self.id = 0
        self.name = "MISSING NAME"
        self.x = x
        self.y = y
        self.sprite_coords = (0, 64)
        self.building_cost = {}
        self.can_be_placed_on = [TileIndex.PLAINS]
        self.description = ""

        self.player_faction = True
        self.focused_enemy=None
        
        self.max_hp = 1
        self.current_hp = self.max_hp
        self.exists = True

        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown

        self.radius = 0

        self.is_moving_unit = False
        self.move_me = False

    def simulate_building(self):
        self.current_cooldown -= float(1/30)
        print(self.building_manager)
        if self.focused_enemy!= None:
            # check if exists
            if not self.building_manager.check_if_exists(self.focused_enemy):
                self.focused_enemy = None
        if (self.current_cooldown <= 0.0):
            self.current_cooldown = self.max_cooldown
            self.do_building_action()

    def do_building_action(self):
        pass 

class House(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "House"
        self.sprite_coords = (16,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 1
        }
        self.radius = 1
        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown

        self.description = "- gather resources from neighbour tiles"

    def do_building_action(self):
        # Try to gather random resource from neibhour stuff
        neighbour_fields = self.tile_manager.get_neigbour_tiles(self.x, self.y, self.radius)
        random.shuffle(neighbour_fields)
        for i in neighbour_fields:
            if TileIndex.from_value(i) in [TileIndex.FOREST, TileIndex.MONTAIN, TileIndex.RIVER]:
                # gather resource, return
                self.resource_manager.increment_resource(resources_from_tiles[TileIndex.from_value(i)], 1)
                self.particle_manager.add_particle(f"+1{resource_names[resources_from_tiles[TileIndex.from_value(i)]]}", (self.x, self.y))
                return

class Mine(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Mine"
        self.sprite_coords = (32,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 3
        }
        self.can_be_placed_on = [TileIndex.MONTAIN]

    def do_building_action(self):
        # Gather 1 Stone
        self.resource_manager.increment_resource(ResourcesIndex.STONE, 1)
        self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.STONE]}", (self.x, self.y))
        

class Fishermans(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Fishermans"
        self.sprite_coords = (48,64)
        self.building_cost = {
            ResourcesIndex.STONE: 0,
            ResourcesIndex.WOOD: 3
        }
        self.can_be_placed_on = [TileIndex.RIVER]
        self.max_cooldown = 5.0
        self.current_cooldown = self.max_cooldown

    def do_building_action(self):
        self.building_manager.delete_building(self)


class Tower(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Tower"
        self.sprite_coords = (64,64)
        self.building_cost = {
            ResourcesIndex.STONE: 5,
            ResourcesIndex.WOOD: 2
        }

        self.radius = 2


class MovingUnit(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.is_moving_unit = True
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.max_hp = 4
        self.current_hp = self.max_hp
        self.moving_destination = None
        #self.focused_enemy = None
    def simulate_building(self):
        super().simulate_building()
        self.speed_cooldown -= float(1/30)
        if (self.speed_cooldown <= 0.0):
            self.speed_cooldown = self.speed
            self.move_me=True



class King(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "King"
        self.description = "CTRL+Left Mouse to move\n- lose the King = lose the game"
        self.sprite_coords = (80,64)
        self.max_hp = 20
        self.current_hp = self.max_hp
        self.speed = 0.2
        self.speed_cooldown = self.speed

    def simulate_building(self):
        super().simulate_building()