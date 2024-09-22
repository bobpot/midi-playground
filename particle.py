import random
import pygame

class Particle:
    SPEED_VARIATION = 4
    SIZE_MIN = 7
    SIZE_MAX = 14
    AGE_RATE = 20
    SLOW_DOWN_RATE = 1.2
    MAX_STRETCH_FACTOR = 3  # Maximum stretch factor for the particles
    MAX_ALPHA = 255         # Full opacity

    def __init__(self, pos: list[float], delta: list[float], invert_color: bool = False):
        self.pos = pos.copy()
        self.size = random.randint(Particle.SIZE_MIN, Particle.SIZE_MAX)
        self.stretch_factor = random.uniform(1, Particle.MAX_STRETCH_FACTOR)
        self.delta = delta.copy()
        self.delta[0] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION) / 8
        self.delta[1] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION) / 8
        # color is hallway color if invert_color is false, else it's background color
        self.color = get_colors()["hallway"] if not invert_color else get_colors()["background"]
        self.alpha = Particle.MAX_ALPHA  # Start fully opaque

    def age(self):
        self.size -= Particle.AGE_RATE * Config.dt
        self.x += self.delta[0] * Config.PARTICLE_SPEED
        self.y += self.delta[1] * Config.PARTICLE_SPEED

        # Slow down the particle speed
        self.delta[0] /= (Particle.SLOW_DOWN_RATE + FRAMERATE) * Config.dt
        self.delta[1] /= (Particle.SLOW_DOWN_RATE + FRAMERATE) * Config.dt

        # Reduce opacity gradually to create a fading effect
        self.alpha -= Particle.AGE_RATE * Config.dt * 10

        # Return true if the particle is too small or completely transparent
        return self.size <= 0 or self.alpha <= 0

    def draw(self, surface):
        # Create a surface for the particle with alpha transparency
        particle_surface = pygame.Surface((self.size * self.stretch_factor, self.size), pygame.SRCALPHA)
        stretched_rect = pygame.Rect(0, 0, self.size * self.stretch_factor, self.size)
        
        # Set color with alpha (transparency)
        color_with_alpha = (*self.color, int(self.alpha))
        
        # Draw an elongated (stretched) rectangle to simulate motion blur
        pygame.draw.ellipse(particle_surface, color_with_alpha, stretched_rect)

        # Rotate and blit the particle to simulate directional motion
        angle = math.degrees(math.atan2(self.delta[1], self.delta[0]))  # Get the angle of motion
        rotated_particle = pygame.transform.rotate(particle_surface, angle)
        surface.blit(rotated_particle, (self.x, self.y), special_flags=pygame.BLEND_RGBA_ADD)

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, val: float):
        self.pos[0] = val

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, val: float):
        self.pos[1] = val

    @property
    def rect(self):
        return pygame.Rect(self.x - self.size / 2, self.y - self.size / 2, *(2 * [self.size]))
