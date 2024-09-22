try:
    from glowing import make_glowy2
except ImportError:
    make_glowy2 = None
from utils import *
import pygame
from pygame import Color
from bounce import Bounce


class Square:
    def __init__(self, x: float = 0, y: float = 0, dx: int = 1, dy: int = 1):
        self.pos = [x, y]
        self.dir = [dx, dy]
        self.died = False
        self.time_since_glow_start = 0
    
    def draw_glowing3(self, win, rect):
        if self.died:
            return
        
        # Draw glowing border
        if Config.square_glow:
            if pygame.time.get_ticks() - self.time_since_glow_start < Config.square_glow_duration * 1000:
                progress = 1 - (pygame.time.get_ticks() - self.time_since_glow_start) / (Config.square_glow_duration * 1000)
                val = int(progress * Config.glow_intensity)
            else:
                val = 1
            val = max(val, Config.square_min_glow)

            # Draw glow border (this would be where the glow shader is applied)
            glowy_borders = make_glowy2((rect.size[0] + 40, rect.size[1] + 40), Config.glow_color, val)
            surface = pygame.Surface(rect.inflate(100, 100).size, pygame.SRCALPHA)
            surface.blit(glowy_borders, (20, 20), special_flags=pygame.BLEND_RGBA_ADD)
            win.blit(surface, rect.move(-40, -40).topleft, special_flags=pygame.BLEND_RGBA_ADD)
        
        # Draw square with interior color
        pygame.draw.rect(win, Config.current_square_color, rect)
    
    def change_color_on_impact(self):
        # Choose the next pastel color in the list
        current_index = Config.pastel_colors.index(Config.current_square_color)
        new_index = (current_index + 1) % len(Config.pastel_colors)
        Config.current_square_color = Config.pastel_colors[new_index]

    def title_screen_physics(self, bounding: pygame.Rect):
        self.reg_move()
        r = self.rect
        
        if r.right > bounding.right or r.left < bounding.left:
            self.dir[0] *= -1  # Reverse horizontal direction
            self.change_color_on_impact()  # Change color on horizontal boundary impact
        elif r.bottom > bounding.bottom or r.top < bounding.top:
            self.dir[1] *= -1  # Reverse vertical direction
            self.change_color_on_impact()  # Change color on vertical boundary impact
        
    def reg_move(self):
        self.pos[0] += self.dir[0] * Config.square_speed * Config.dt
        self.pos[1] += self.dir[1] * Config.square_speed * Config.dt

    @property
    def rect(self):
        return pygame.Rect(self.pos[0] - Config.SQUARE_SIZE // 2, self.pos[1] - Config.SQUARE_SIZE // 2, Config.SQUARE_SIZE, Config.SQUARE_SIZE)

# Dummy function to create a glowing border (replace with real shader logic)
def make_glowy2(size, color, intensity):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surface, color, surface.get_rect(), intensity)
    return surface

    def start_bounce(self):
        self.time_since_glow_start = pygame.time.get_ticks()

    def obey_bounce(self, bounce: Bounce):
        # planned bounces
        self.start_bounce()
        self.pos = bounce.square_pos
        self.dir = bounce.square_dir
        self.latest_bounce_direction = bounce.bounce_dir
        self.last_bounce_time = bounce.time
        return

    def reg_move(self, use_dt: bool = True):
        self.x += self.dir_x * Config.square_speed * (Config.dt if use_dt else 1 / FRAMERATE)
        self.y += self.dir_y * Config.square_speed * (Config.dt if use_dt else 1 / FRAMERATE)
