import pyxel
class Particle:
    def __init__(self, text: str, position, color_number=7, duration=0.5):
        self.text = text
        self.position = position
        self.color_number = color_number
        self.duration = duration

    def update(self, dt):
        # Decrement the duration of the particle
        self.duration -= dt
        # Check if the particle should be removed
        return self.duration <= 0

class ParticleManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.particle_list = []
        pass
    
    def add_particle(self, text: str, position, color_number=7, duration=0.5):
        particle = Particle(text, position, color_number, duration)
        self.particle_list.append(particle)

    def render_particles(self):
        for particle in self.particle_list[:]:
            if particle.update(float(1/30)):
                self.particle_list.remove(particle)
            else:
                self.render_particle(particle)

    def render_particle(self, particle: Particle):
        pyxel.text(particle.position[0]*16, particle.position[1]*16, particle.text, particle.color_number)