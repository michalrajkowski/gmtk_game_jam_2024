from resource_manager import ResourceManager,ResourcesIndex, resource_sprites, resources_from_tiles, resource_names
from tile_manager import TileIndex, TileManager
from particles_manager import ParticleManager
from game_manager import GameManager, GameState
# from event_manager import MeleeAttack_Event
import random
# jakie cechy powinien mieć base building
# - pozycja
# - sprite pos?
# - cooldown/what it does?
def get_weighted_result(weights, results):
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

class Building:
    def __init__(self, x=0, y=0):
        self.game_manager: GameManager = GameManager()
        self.resource_manager: ResourceManager = None
        self.tile_manager: TileManager = None
        self.particle_manager = ParticleManager()
        self.event_manager = None
        self.building_manager = None
        self.id = 0
        self.name = "MISSING NAME"
        self.x = x
        self.y = y
        self.sprite_coords = (0, 64)
        self.building_cost = {}
        self.can_be_placed_on = [TileIndex.PLAINS]
        self.description = ""

        self.first_iteration = True

        self.player_faction = True
        self.focused_enemy=None
        
        self.max_hp = 1
        self.current_hp = self.max_hp
        self.damage_reduction = 0
        self.is_alive = True

        self.is_busy = False

        self.attack_damage = 1
        self.attack_range = 1
        self.can_attack = True
        self.attack_cooldown_max = 1.0
        self.attack_cooldown_current = self.attack_cooldown_max 

        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown

        self.speed = 1.0
        self.speed_cooldown = self.speed

        self.radius = 0

        self.is_moving_unit = False
        self.move_me = False

        self.regenerate_hp_cooldown = 20.0
        self.regenerate_hp_max = 20.0

    def randomize_cooldowns(self):
        self.current_cooldown =  self.max_cooldown - 1 + random.random()
        self.speed_cooldown = random.uniform(0,self.speed)
        self.attack_cooldown_current = random.uniform(0,self.attack_cooldown_max)

    def simulate_building(self):
        if (self.first_iteration):
            self.on_build()
            self.randomize_cooldowns()
            self.first_iteration = False

        self.current_cooldown -= float(1/30)
        self.attack_cooldown_current -= float(1/30)
        self.regenerate_hp_cooldown -= float(1/30)
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
        if (self.regenerate_hp_cooldown <=0.0):
            self.regenerate_hp_cooldown = self.regenerate_hp_max
            self.heal()


    def heal(self):
        from event_manager import DrawText_event
        from animation_handler import Point
        if self.player_faction == False:
            return
        
        if self.current_hp <= self.max_hp:
            self.current_hp+=1
            draw_text_event = DrawText_event(Point(self.x*16, self.y*16), f"+1 HP", color=3)   #((self.x, self.y), resources_from_tiles[TileIndex.from_value(i)], 1)
            self.event_manager.add_event(draw_text_event)
            # self.particle_manager.add_particle(f"+1 Hp", (self.x, self.y), color_number=3)


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
        self.start_attack()

    def choose_enemy(self):
        pass

    def take_damage(self,incoming_damage, attacking_unit=None):
        from event_manager import DamageHit_event, DrawText_event
        from animation_handler import Point
        real_damage = max(incoming_damage - self.damage_reduction,0)
        self.current_hp -= real_damage
        point = Point(self.x*16, self.y*16)
        draw_text_event = DrawText_event(point, f"{-1*real_damage} Hp", color=8, duration=0.5)   #((self.x, self.y), resources_from_tiles[TileIndex.from_value(i)], 1)
        self.event_manager.add_event(draw_text_event)
        #self.particle_manager.add_particle(f"{-1*real_damage} Hp", (self.x, self.y), color_number=2)
        
        hit_event = DamageHit_event(self,duration=0.2)
        self.event_manager.add_event(hit_event)

        if (self.current_hp <= 0):
            self.is_alive = False
            self.on_death()
            self.building_manager.delete_building(self)

    def deal_damage(self, target, damage):
        target:Building = target
        target.take_damage(damage, self)
        

    def start_attack(self, attack_number=0):
        # create correct attack animation?
        # Basic attack is to just deal damage
        
        self.deal_damage(self.focused_enemy, self.attack_damage)
        self.is_busy=True

    def end_attack(self):
        self.is_busy = False

    def on_build(self):
        pass
    def on_death(self):
        
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
        self.max_cooldown = 20.0
        self.current_cooldown = self.max_cooldown

        self.description = "- gather resources from neighbour tiles"

    def do_building_action(self):
        # Try to gather random resource from neibhour stuff
        from event_manager import DrawResource_event
        neighbour_fields = self.tile_manager.get_neigbour_tiles(self.x, self.y, self.radius)
        random.shuffle(neighbour_fields)
        for i in neighbour_fields:
            if TileIndex.from_value(i) in [TileIndex.FOREST, TileIndex.MONTAIN, TileIndex.RIVER]:
                # gather resource, return
                self.resource_manager.increment_resource(resources_from_tiles[TileIndex.from_value(i)], 1)
                draw_resource_event = DrawResource_event((self.x, self.y), resources_from_tiles[TileIndex.from_value(i)], 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                #self.particle_manager.add_particle(f"+1{resource_names[resources_from_tiles[TileIndex.from_value(i)]]}", (self.x, self.y))
                return

class Field(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Field"
        self.sprite_coords = (160,64)
        self.building_cost = {
            ResourcesIndex.WOOD: 2
        }
        self.field_sprites = [(128,64), (144,64), (160,64)]
        self.can_be_placed_on = [TileIndex.PLAINS]
        self.radius = 0
        self.max_cooldown = 20.0
        self.current_cooldown = self.max_cooldown

        self.description = "- produces food\n- food production takes a long time"

    def simulate_building(self):
        super().simulate_building()
        # add sprite based on growth state
        growth_state = float(self.current_cooldown / self.max_cooldown)
        if growth_state > 0.66:
            self.sprite_coords = self.field_sprites[0]
        elif growth_state > 0.33:
            self.sprite_coords = self.field_sprites[1]
        else:
            self.sprite_coords = self.field_sprites[2]
        

    def do_building_action(self):
        from event_manager import DrawResource_event
        draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.FOOD, 1, event_source=self)
        self.event_manager.add_event(draw_resource_event)
        self.resource_manager.increment_resource(ResourcesIndex.FOOD, 1)
        #self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.FOOD]}", (self.x, self.y))

class Lumberjack(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Lumberjack Hut"
        self.sprite_coords = (176,64)
        self.building_cost = {
            ResourcesIndex.WOOD: 5
        }
        self.radius = 1
        self.max_cooldown = 10.0
        self.current_cooldown = self.max_cooldown

        self.description = "- collect wood from forests\n- forests number increase efficiency"

    def do_building_action(self):
        # Try to gather random resource from neibhour stuff
        neighbour_fields = self.tile_manager.get_neigbour_tiles(self.x, self.y, self.radius)
        random.shuffle(neighbour_fields)
        # calculate all forests number
        forests_number = 0
        for i in neighbour_fields:
            if TileIndex.from_value(i) in [TileIndex.FOREST]:
                forests_number+=1
        if forests_number > 0:
            self.resource_manager.increment_resource(ResourcesIndex.WOOD, 1)
            from event_manager import DrawResource_event
            draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.WOOD, 1, event_source=self)
            self.event_manager.add_event(draw_resource_event)
            # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.WOOD]}", (self.x, self.y))
        # Reduce cooldown based on forests number:
        self.current_cooldown -= forests_number

class Mine(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Mine"
        self.sprite_coords = (32,64)
        self.building_cost = {
            ResourcesIndex.STONE: 1,
            ResourcesIndex.WOOD: 3,
            ResourcesIndex.LEATHER: 1,
        }
        self.mithril_chance = 1
        self.gold_chance = 10
        self.stone_chance = 200
        self.max_cooldown = 4.0
        self.current_cooldown = self.max_cooldown
        self.can_be_placed_on = [TileIndex.MONTAIN]
        self.description = "- collects stone\n- has small chance to mine valuables\n- can only be built on mountains"

    def do_building_action(self):
        # Gather 1 Stone
        weigths = [self.stone_chance, self.gold_chance, self.mithril_chance]
        results = [ResourcesIndex.STONE, ResourcesIndex.GOLD, ResourcesIndex.MITHRIL]
        random_resource = get_weighted_result(weigths, results)
        self.resource_manager.increment_resource(random_resource, 1)
        from event_manager import DrawResource_event
        draw_resource_event = DrawResource_event((self.x, self.y), random_resource, 1, event_source=self)
        self.event_manager.add_event(draw_resource_event)
        # self.particle_manager.add_particle(f"+1{resource_names[random_resource]}", (self.x, self.y))

class Smelter(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Smelter"
        self.sprite_coords = (240,64)
        self.building_cost = {
            ResourcesIndex.STONE: 11,
        }
        self.mithril_chance = 1
        self.gold_chance = 10
        self.stone_chance = 200
        self.max_cooldown = 10.0
        self.current_cooldown = self.max_cooldown
        self.can_be_placed_on = [TileIndex.PLAINS]
        self.description = "- Produces Iron"

    def do_building_action(self):
        # Gather 1 Stone
        self.resource_manager.increment_resource(ResourcesIndex.IRON, 1)
        from event_manager import DrawResource_event
        draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.IRON, 1, event_source=self)
        self.event_manager.add_event(draw_resource_event)
        # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.IRON]}", (self.x, self.y))

class Fisherman_Hut(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Fisherman"
        self.sprite_coords = (192,64)
        self.building_cost = {
            ResourcesIndex.WOOD: 4
        }
        self.radius = 1
        self.max_cooldown = 10.0
        self.current_cooldown = self.max_cooldown

        self.food_chance = 100
        self.gold_fish_chance = 1
        self.treasure_chance = 1

        self.description = "- gathers food from lakes\n- has small chance to fish goldfish or treasure\n- number of ponds increases his efficiency"

    def do_building_action(self):
        from event_manager import DrawResource_event, DrawText_event
        from animation_handler import Point
        # Try to gather random resource from neibhour stuff
        neighbour_fields = self.tile_manager.get_neigbour_tiles(self.x, self.y, self.radius)
        random.shuffle(neighbour_fields)
        # calculate all forests number
        river_number = 0
        for i in neighbour_fields:
            if TileIndex.from_value(i) in [TileIndex.RIVER]:
                river_number+=1
        if river_number == 0:
            return
        
        weigths = [self.food_chance, self.gold_fish_chance+river_number, self.treasure_chance+river_number]
        results = ["food", "goldfish", "treasure"]
        random_result = get_weighted_result(weigths, results)
        if random_result == "food":
            self.resource_manager.increment_resource(ResourcesIndex.FOOD, 1)
            draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.FOOD, 1, event_source=self)
            self.event_manager.add_event(draw_resource_event)
            # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.FOOD]}", (self.x, self.y))
        elif random_result == "goldfish":
            text_event = DrawText_event(Point(16*self.x, 16*self.y), "GOLDFISH", 10, event_source=self)
            self.event_manager.add_event(text_event)

            self.resource_manager.increment_resource(ResourcesIndex.GOLD, 1)
            
            draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.GOLD, 1, event_source=self)
            self.event_manager.add_event(draw_resource_event)
            # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.GOLD]}", (self.x, self.y))
        elif random_result == "treasure":
            # get random resources?
            text_event = DrawText_event(Point(16*self.x, 16*self.y), "TREASURE", 10, event_source=self)
            self.event_manager.add_event(text_event)
            random_amount = random.randint(0,5)
            if random_amount > 0:
                self.resource_manager.increment_resource(ResourcesIndex.WOOD, 1)
                draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.WOOD, 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.WOOD]}", (self.x, self.y))
            random_amount = random.randint(0,5)
            if random_amount > 0:
                self.resource_manager.increment_resource(ResourcesIndex.STONE, 1)
                draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.STONE, 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.STONE]}", (self.x, self.y))
            random_amount = random.randint(0,3)
            if random_amount > 0:
                self.resource_manager.increment_resource(ResourcesIndex.FOOD, 1)
                draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.FOOD, 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.FOOD]}", (self.x, self.y))
            random_amount = random.randint(0,1)
            if random_amount > 0:
                self.resource_manager.increment_resource(ResourcesIndex.IRON, 1)
                draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.IRON, 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.IRON]}", (self.x, self.y))
            random_amount = random.randint(0,1)
            if random_amount > 0:
                self.resource_manager.increment_resource(ResourcesIndex.LEATHER, 1)
                draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.LEATHER, 1, event_source=self)
                self.event_manager.add_event(draw_resource_event)
                # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.LEATHER]}", (self.x, self.y))
        
        # Reduce cooldown based on forests number:
        self.current_cooldown -= river_number

# class Hunter_camp(Building):

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

class Storage(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Storage"
        self.sprite_coords = (224,64)
        self.building_cost = {
            ResourcesIndex.STONE: 5,
            ResourcesIndex.WOOD: 5
        }
        self.max_hp = 20
        self.current_hp = 20
        self.max_cooldown = 1.0
        self.current_cooldown = self.max_cooldown
        self.description="- increases basic resource max by 5"

    def on_death(self):
        # increase basic resource number
        self.resource_manager.change_max_resource(-5)

    def on_build(self):
        # decrease bascic resource cap
        self.resource_manager.change_max_resource(5)

class Watchtower(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Watchtower"
        self.sprite_coords = (208,64)
        self.building_cost = {
            ResourcesIndex.FOOD: 2,
            ResourcesIndex.WOOD: 5
        }

        self.radius = 1
        self.attack_range = 1
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.description = "- Attacks enemy units in range"
    def choose_enemy(self):
        # Choose random unit in range
        nei_buildings = self.building_manager.get_neigbour_buildings(self.x, self.y, self.attack_range)
        for building in nei_buildings.values():
            building :Building = building
            if building.player_faction != self.player_faction:
                self.focused_enemy = building
                return
        self.focused_enemy=None

    def try_to_attack(self):
        if self.focused_enemy == None:
            # choose enemy
            self.choose_enemy()
        if self.focused_enemy == None:
            return
        
        # Check if is in range
        if (abs(self.focused_enemy.x - self.x) > self.attack_range or abs(self.focused_enemy.y - self.y) > self.attack_range):
            self.focused_enemy = None
            self.choose_enemy()
        
        if self.focused_enemy == None:
            return
        
        # Attack the enemy
        self.focused_enemy.take_damage(self.attack_damage, self)


class Tower(Building):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Tower"
        self.sprite_coords = (64,64)
        self.building_cost = {
            ResourcesIndex.STONE: 6,
            ResourcesIndex.WOOD: 3,
            ResourcesIndex.FOOD: 3,

        }

        self.radius = 2
        self.attack_range = 2
        self.max_hp = 20
        self.current_hp = self.max_hp
        self.description = "- Attacks enemy units in range\n- Very durable"

    def choose_enemy(self):
        # Choose random unit in range
        nei_buildings = self.building_manager.get_neigbour_buildings(self.x, self.y, self.attack_range)
        for building in nei_buildings.values():
            building :Building = building
            if building.player_faction != self.player_faction:
                self.focused_enemy = building
                return
        self.focused_enemy=None

    def try_to_attack(self):
        if self.focused_enemy == None:
            # choose enemy
            self.choose_enemy()
        if self.focused_enemy == None:
            return
        
        # Check if is in range
        if (abs(self.focused_enemy.x - self.x) > self.attack_range or abs(self.focused_enemy.y - self.y) > self.attack_range):
            self.focused_enemy = None
            self.choose_enemy()
        
        if self.focused_enemy == None:
            return
        
        # Attack the enemy
        self.focused_enemy.take_damage(self.attack_damage, self)

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
            if not self.is_busy:
                self.move_me=True

    def start_attack(self, attack_number=0):
        self.is_busy = True
        from event_manager import MeleeAttack_Event, EventManager
        # create correct attack animation?
        # Basic attack is to just deal damage
        attack_event = MeleeAttack_Event(self, self.focused_enemy, duration=self.attack_cooldown_max*0.5, max_action_cooldown=self.attack_cooldown_max*0.5*0.66)
        self.event_manager:EventManager = self.event_manager
        self.event_manager.add_event(attack_event)

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
        super().on_death()
        # TODO: lose game
        self.game_manager.game_state = GameState.LOSE_SCREEN

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
        # drop meat and leather
        from event_manager import DrawResource_event
        random_chance = random.random()
        self.resource_manager.increment_resource(ResourcesIndex.FOOD, 1)
        draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.FOOD, 1, event_source=self)
        self.event_manager.add_event(draw_resource_event)
        # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.FOOD]}", (self.x, self.y))
        if random_chance > 0.5:
            self.resource_manager.increment_resource(ResourcesIndex.LEATHER, 1)
            draw_resource_event = DrawResource_event((self.x, self.y), ResourcesIndex.LEATHER, 1, event_source=self)
            self.event_manager.add_event(draw_resource_event)
            # self.particle_manager.add_particle(f"+1{resource_names[ResourcesIndex.LEATHER]}", (self.x, self.y))

class Skeleton(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Skeleton"
        self.description = "- walks aimlessly and attack things in range"
        self.sprite_coords = (64,80)
        self.max_hp = 2
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = False

        self.attack_range = 1

        self.max_cooldown = 5.0
        self.current_cooldown = self.max_cooldown

    def do_building_action(self):
        # generate random walk direction
        random_walk_direction = (random.randint(0,11), random.randint(0,11))
        self.moving_destination = random_walk_direction

    def simulate_building(self):
        super().simulate_building()

    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()
        # drop meat and leather

    def choose_enemy(self):
        # choose random thing in range
        # Choose random unit in range
        nei_buildings = self.building_manager.get_neigbour_buildings(self.x, self.y, self.attack_range)
        for building in nei_buildings.values():
            building :Building = building
            if building.player_faction != self.player_faction:
                self.focused_enemy = building
                return
        self.focused_enemy=None

class Necromancer(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Necromancer"
        self.description = "- Creates army of the undead"
        self.sprite_coords = (48,80)
        self.max_hp = 5
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = False

        self.max_cooldown = 10.0
        self.current_cooldown = self.max_cooldown
        

    def simulate_building(self):
        super().simulate_building()

    def do_building_action(self):
        new_undead = Skeleton(0,0)
        for x in range(self.x - 1, self.x+2):
            for y in range(self.y - 1, self.y+2):
                if(self.building_manager.can_be_built(new_undead,x, y)):
                    self.building_manager.build_building(new_undead,x,y)
                    return


    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()
        # drop meat and leather

    def choose_enemy(self):
        # Choose random unit in range
        nei_buildings = self.building_manager.get_neigbour_buildings(self.x, self.y, self.attack_range)
        for building in nei_buildings.values():
            building :Building = building
            if building.player_faction != self.player_faction:
                self.focused_enemy = building
                return
        self.focused_enemy=None

class Goblin(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Goblin"
        self.description = ""
        self.sprite_coords = (112,64)
        self.max_hp = 3
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

    def choose_enemy(self):
        self.focused_enemy = self.building_manager.get_king()
        pass

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

class Villager(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Knight"
        self.description = "- Moving unit"
        self.sprite_coords = (80,80)
        self.max_hp = 5
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = True
        self.building_cost = {
            ResourcesIndex.FOOD: 3
        }

    def simulate_building(self):
        super().simulate_building()

    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()

class Knight(MovingUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = "Knight"
        self.description = "- Moving unit"
        self.sprite_coords = (96,80)
        self.max_hp = 20
        self.current_hp = self.max_hp
        self.speed = 1.0
        self.speed_cooldown = self.speed
        self.player_faction = True
        self.building_cost = {
            ResourcesIndex.IRON: 2,
            ResourcesIndex.FOOD: 5
        }

    def simulate_building(self):
        super().simulate_building()

    def take_damage(self, incoming_damage, attacking_unit=None):
        super().take_damage(incoming_damage, attacking_unit)
        if attacking_unit != None:
            self.focused_enemy = attacking_unit

    def on_death(self):
        return super().on_death()
