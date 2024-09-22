import random
import pygame
import math

class Particle:
    SPEED_VARIATION = 4
    SIZE_MIN = 20    # Increased min size for a larger, more visible trail
    SIZE_MAX = 40    # Increased max size
    AGE_RATE = 25    # Aging rate affects how quickly the particle fades and shrinks
    SLOW_DOWN_RATE = 1.2
    MAX_STRETCH_FACTOR = 2.5  # Elongates the particles for a smoother trail
    MAX_ALPHA = 180           # Start with translucent particles

    def __init__(self, pos: list[float], delta: list[float], dt: float):
        self.pos = pos.copy()
        self.size = random.randint(Particle.SIZE_MIN, Particle.SIZE_MAX)
        self.stretch_factor = random.uniform(1.2, Particle.MAX_STRETCH_FACTOR)  # Stretch the particles
        self.delta = delta.copy()
        self.dt = dt  # Save the delta time as an instance variable

        # Randomly adjust particle speed slightly
        self.delta[0] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION) / 8
        self.delta[1] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION) / 8

        # Set color to white with initial translucency
        self.color = pygame.Color(255, 255, 255, Particle.MAX_ALPHA)
        self.alpha = Particle.MAX_ALPHA

    def age(self):
        # Shrink particle size
        self.size -= Particle.AGE_RATE * self.dt
        self.pos[0] += self.delta[0] * self.dt
        self.pos[1] += self.delta[1] * self.dt

        # Slow down particle speed
        self.delta[0] /= (Particle.SLOW_DOWN_RATE + self.dt)
        self.delta[1] /= (Particle.SLOW_DOWN_RATE + self.dt)

        # Reduce opacity gradually to create fading effect
        self.alpha -= Particle.AGE_RATE * self.dt * 5
        self.color.a = max(0, int(self.alpha))  # Ensure alpha stays non-negative

        # Return True if the particle is too small or fully transparent
        return self.size <= 0 or self.alpha <= 0

    def draw(self, surface):
        # Create a surface for the particle with alpha transparency
        particle_surface = pygame.Surface((self.size * self.stretch_factor, self.size), pygame.SRCALPHA)
        stretched_rect = pygame.Rect(0, 0, self.size * self.stretch_factor, self.size)

        # Draw an elongated translucent ellipse to simulate motion blur
        pygame.draw.ellipse(particle_surface, self.color, stretched_rect)

        # Rotate and blit the particle to simulate directional motion
        angle = math.degrees(math.atan2(self.delta[1], self.delta[0]))  # Get the angle of motion
        rotated_particle = pygame.transform.rotate(particle_surface, angle)
        surface.blit(rotated_particle, (self.pos[0], self.pos[1]), special_flags=pygame.BLEND_RGBA_ADD)


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
