import pyxel
import math
import random
import numpy

# Renders sprites with their animations
# Makes sure that there is not many animations at the same time for sprite

# The movement / calculation of offset of things on the screen
def normalize(vector):
    magnitude = math.sqrt(sum(comp**2 for comp in vector))
    if magnitude == 0:
        return (0,0)
    return ([comp / magnitude for comp in vector])

def lerp(a, b, t):
    return a + t * (b - a)

class ObjectAnimation:
    def __init__(self, object_assigned_to, max_time, starting_offset_x=0, starting_offset_y=0) -> None:
        self.object_assigned_to = object_assigned_to
        self.animation_handler = None
        self.starting_offset_x = starting_offset_x
        self.starting_offset_y = starting_offset_y
        self.offset_x = 0
        self.offset_y = 0
        self.current_time = 0.0
        self.max_time = max_time

    def simulate(self):
        self.current_time += (1/30)
        if self.current_time >= self.max_time:
            self.delete_animation()
            return
        self.calculate_offsets()
    
    def delete_animation(self):
        self.animation_handler.delete_animation(self)

    def calculate_offsets(self):
        pass

class MeleeAttackAnimation(ObjectAnimation):
    def __init__(self, object_assigned_to, target_object, max_time, starting_offset_x=0, starting_offset_y=0) -> None:
        super().__init__(object_assigned_to, max_time, starting_offset_x, starting_offset_y)
        self.target_object = target_object

    def calculate_offsets(self):
        
        # Here we calculate the offsets for the thing:
        # Get animation point
        # function "smooth/lerp" between them
        
        # move backwards?
        (e_x, e_y) = (self.target_object.x*16 + 8, self.target_object.y*16 + 8)
        (o_x, o_y) = (self.object_assigned_to.x*16 + 8, self.object_assigned_to.y*16 + 8)

        dir_x = e_x - o_x
        dir_y = e_y - o_y
        
        vector_dir = [dir_x,dir_y]
        vector_dir_normalized = normalize(vector_dir) 
        point_1 = (int(-1*vector_dir_normalized[0]*2), int(-1*vector_dir_normalized[1]*2))

        # chaaarge!
        point_2 = (int(dir_x/2), int(dir_y/2))

        # move to its starting place
        point_3 = (0,0)

        f_1 = 0.33*self.max_time
        f_2 = 0.66*self.max_time
        f_3 = self.max_time
        if (self.current_time < f_1):
            t = self.current_time / f_1
            n_x = lerp(0,point_1[0], t)
            n_y = lerp(0,point_1[1], t)
            (self.offset_x, self.offset_y) = (n_x, n_y)
        elif(self.current_time < f_2):
            t = (self.current_time - f_1) / (f_2 - f_1)
            n_x = lerp(point_1[0],point_2[0], t)
            n_y = lerp(point_1[1],point_2[1], t)
            (self.offset_x, self.offset_y) = (n_x, n_y)
        else:
            t = (self.current_time - f_2) / (f_3 - f_2)
            n_x = lerp(point_2[0],point_3[0], t)
            n_y = lerp(point_2[1],point_3[1], t)
            (self.offset_x, self.offset_y) = (n_x, n_y)


# Graphical thing drawn on the screen
# Has the layer, which tells the order of drawing them
# Attack event spawns animation and is tied to it?
class Effect:
    def __init__(self, object_assigned_to, max_time, starting_offset_x=0, starting_offset_y=0, relative=True) -> None:
        self.object_assigned_to = object_assigned_to
        self.animation_handler = None
        self.starting_offset_x = starting_offset_x
        self.starting_offset_y = starting_offset_y
        self.x = object_assigned_to.x*16
        self.y = object_assigned_to.y*16
        self.current_time = 0.0
        self.max_time = max_time

    def simulate(self):
        self.current_time += (1/30)
        if self.current_time >= self.max_time:
            self.delete_effect()
            return
        self.calculate_offsets()

    def calculate_offsets(self):
        pass

    def delete_effect(self):
        self.animation_handler.delete_effect(self)

    def draw(self):
        pass

class Point():
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
        pass

class Particle_effect(Effect):
    def __init__(self, object_assigned_to, max_time, starting_offset_x=0, starting_offset_y=0, relative=True,
                 particle_number=0, particle_speed=0,particle_color=0, speed_randomizer =0.0) -> None:
        super().__init__(object_assigned_to, max_time, starting_offset_x, starting_offset_y, relative)
        # create particles
        self.x = object_assigned_to.x
        self.y = object_assigned_to.y
        self.particle_number : int = particle_number
        self.particle_speed : float =particle_speed
        self.particle_color : int = particle_color
        self.particle_list = []
        for i in range(self.particle_number):
            px = self.x + 8
            py = self.y + 8
            vx = random.random() * numpy.sign(random.random() - 0.5)
            vy = random.random() * numpy.sign(random.random() - 0.5)
            v_normalized = normalize([vx, vy])
            particle = (px, py, v_normalized[0], v_normalized[1], particle_speed - random.random()*speed_randomizer)
            self.particle_list.append(particle)

    def calculate_offsets(self):
        for particle in self.particle_list[:]:
            print(particle)
            n_particle = (float(particle[0])+float(particle[2])*particle[4],
                          float(particle[1])+float(particle[3])*particle[4],
                          particle[2],
                          particle[3],
                          particle[4]) 
            self.particle_list.remove(particle)
            self.particle_list.append(n_particle)

    def draw(self):
        for particle in self.particle_list[:]:
            pyxel.pset(int(particle[0]),int(particle[1]),self.particle_color)

    # particle animation is a splash of particle moving into random direction and lifetime from origin points?

class Hit_Effect(Effect):
    def __init__(self, object_assigned_to, max_time, starting_offset_x=0, starting_offset_y=0, relative=True) -> None:
        super().__init__(object_assigned_to, max_time, starting_offset_x, starting_offset_y, relative)

    def draw(self):
        from buildings import Building
        # get building position:
        building = self.object_assigned_to
        buildng_animation = self.animation_handler.find_object_animation(building)
        (offset_x, offset_y) = (0,0)
        if buildng_animation != None:
            (offset_x, offset_y) = (buildng_animation.offset_x,buildng_animation.offset_y)

        building: Building = building
        (sprite_u, sprite_v) = (building.sprite_coords[0], building.sprite_coords[1])
        (tile_x, tile_y) = (building.x, building.y)
        draw_x = 16*tile_x + offset_x
        draw_y = 16*tile_y + offset_y

        pyxel.rect(256-16, 256-16, 16, 16, 0)
        pyxel.blt(256-16, 256-16, 0, sprite_u, sprite_v, 16, 16,0)
        # Draw white pixel on each pixel
        for j in range(16):
            for i in range(16):
                c = pyxel.pget(256-16+i, 256-16+j)
                if c == 0:
                    continue
                pyxel.pset(draw_x+i, draw_y+j,7)
        



class AnimationHandler:
    
    def __init__(self) -> None:
        pass
        self.animations_list = []
        self.effects_list = []
        self.building_manager = None
    
    def simulate_all(self):
        for animation in self.animations_list[:]:
            animation.simulate()
        for effect in self.effects_list[:]:
            effect.simulate()
        pass

    def find_object_animation(self,object):
        for animation in self.animations_list:
            if animation.object_assigned_to == object:
                return animation
        return None

    def draw_all(self):
        from buildings import Building
        # Draw all buildings
        for building in self.building_manager.building_dict.values():
            # Find building animation
            buildng_animation = self.find_object_animation(building)
            (offset_x, offset_y) = (0,0)
            if buildng_animation != None:
                (offset_x, offset_y) = (buildng_animation.offset_x,buildng_animation.offset_y)

            building: Building = building
            (sprite_u, sprite_v) = (building.sprite_coords[0], building.sprite_coords[1])
            (tile_x, tile_y) = (building.x, building.y)
            draw_x = 16*tile_x + offset_x
            draw_y = 16*tile_y + offset_y
            pyxel.blt(draw_x, draw_y, 0, sprite_u, sprite_v, 16, 16,0)
        for effect in self.effects_list:
            effect.draw()


    def calculate_objects_offsets():
        pass
    
    def delete_animation(self, animation):
        self.animations_list.remove(animation)

    def add_animation(self, animation):
        self.animations_list.append(animation)
        animation: ObjectAnimation = animation
        animation.animation_handler = self

    def delete_effect(self, effect):
        self.effects_list.remove(effect)

    def add_effect(self, effect):
        self.effects_list.append(effect)
        effect.animation_handler = self

    def draw_sprite(self):
        # Get each player's offset?

        # Get players offset from his animation?

        # draws effects bottom layer

        # draws sprite
        
        # Draw effects above layer
        # Effect can have absolute or relative positioning
        pass