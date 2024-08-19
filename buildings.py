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
        self.damage_reduction = 0

        self.attack_damage = 1
        self.attack_range = 1
        self.can_attack = True
        self.attack_cooldown_max = 1.0
        self.attack_cooldown_current = self.attack_cooldown_max 

        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown

        self.radius = 0

        self.is_moving_unit = False
        self.move_me = False

    def simulate_building(self):
        self.current_cooldown -= float(1/30)
        self.attack_cooldown_current -= float(1/30)
        if self.focused_enemy!= None:
            # check if exists
            if not self.building_manager.check_if_exists(self.focused_enemy):
                self.focused_enemy = None
        if (self.current_cooldown <= 0.0):
            self.current_cooldown = self.max_cooldown
            self.do_building_action()
        if (self.attack_cooldown_current <= 0.0):
            self.attack_cooldown_current = self.attack_cooldown_max
            self.try_to_attack()

    def try_to_attack(self):
        if self.focused_enemy == None:
            # choose enemy
            self.choose_enemy()
        if self.focused_enemy == None:
            return
        
        # Check if is in range
        if (abs(self.focused_enemy.x - self.x) > self.attack_range or abs(self.focused_enemy.y - self.y) > self.attack_range):
            return
        
        # Attack the enemy
        self.focused_enemy.take_damage(self.attack_damage, self)

    def choose_enemy(self):
        pass

    def take_damage(self,incoming_damage, attacking_unit=None):
        real_damage = max(incoming_damage - self.damage_reduction,0)
        self.current_hp -= real_damage
        self.particle_manager.add_particle(f"{-1*real_damage} Hp", (self.x, self.y), color_number=2)
        
        if (self.current_hp <= 0):
            self.on_death()
            self.building_manager.delete_building(self)

    def on_death(self):
        print(f"{self.name} died!")
        pass
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
        self.max_hp = 5
        self.current_hp = 5
        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown

    def do_building_action(self):
        self.take_damage(1)


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

    def on_death(self):
        return super().on_death()
        # TODO: lose game
        print("\nYOU LOST THE GAME\n")

    # Animals
class Wolf(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Wolf"
        self.description = "- meat and fur\n- neutral but will bite back!"
        self.sprite_coords = (96,64)
        self.max_hp = 5
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = False

    def simulate_building(self):
        super().simulate_building()

    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()
        # drop meat and leather

class Wolf_Tamed(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Tamed Wolf"
        self.description = "CTRL+Left Mouse to move\n- attacks back when attacked"
        self.sprite_coords = (96,64)
        self.max_hp = 5
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = True

    def simulate_building(self):
        super().simulate_building()

    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()
