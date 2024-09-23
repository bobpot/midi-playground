from utils import *
from square import Square

class Camera:
    def __init__(self, x: int = 0, y: int = 0, zoom: float = 1.5):
        self.x = x
        self.y = y
        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.locked_on_square = True
        self.lock_type: CameraFollow = CameraFollow(2)
        self.zoom = zoom  # Add a zoom factor for controlling FOV (higher zoom = more zoomed out)

    def attempt_movement(self):
        if not self.locked_on_square:
            keys = pygame.key.get_pressed()
            shift_modifier = (keys[pygame.K_LSHIFT] | keys[pygame.K_RSHIFT]) + 1
            self.x += (keys[pygame.K_d] - keys[pygame.K_a]) * Config.CAMERA_SPEED * shift_modifier / FRAMERATE
            self.y += (keys[pygame.K_s] - keys[pygame.K_w]) * Config.CAMERA_SPEED * shift_modifier / FRAMERATE

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, val: Union[tuple[int, int], list[int]]):
        self.x, self.y = val

    def offset(self, pos_or_rect: Union[pygame.Rect, tuple[int, int]]) -> Union[pygame.Rect, list[int]]:
        if isinstance(pos_or_rect, pygame.Rect):
            return pos_or_rect.move(-self.x, -self.y)
        else:
            return [pos_or_rect[0] - self.x, pos_or_rect[1] - self.y]

    def follow(self, square: Square):
        zoomed_width = Config.SCREEN_WIDTH * self.zoom
        zoomed_height = Config.SCREEN_HEIGHT * self.zoom

        # square in center with zoom factor
        if self.lock_type == CameraFollow.Center:
            self.pos = [square.x - zoomed_width / 2, square.y - zoomed_height / 2]

        # camera only follows if necessary
        if self.lock_type == CameraFollow.Lazy:
            lazy_follow_distance = 250 * self.zoom  # Scale lazy follow distance by zoom
            while square.x - zoomed_width + lazy_follow_distance > self.x:
                self.x += 1
            while square.y - zoomed_height + lazy_follow_distance > self.y:
                self.y += 1
            while square.x - lazy_follow_distance < self.x:
                self.x -= 1
            while square.y - lazy_follow_distance < self.y:
                self.y -= 1

        # smooth camera with zoom factor
        if self.lock_type == CameraFollow.Smoothed:
            easing_rate = 3
            self.x = (square.x - zoomed_width / 2) * easing_rate * Config.dt + self.x - easing_rate * self.x * Config.dt
            self.y = (square.y - zoomed_height / 2) * easing_rate * Config.dt + self.y - easing_rate * self.y * Config.dt

        # camera in front of square with zoom factor
        if self.lock_type == CameraFollow.Predictive:
            self.ax = (square.x - zoomed_width / 2) * 3 * Config.dt + self.ax - 3 * self.ax * Config.dt
            self.ay = (square.y - zoomed_height / 2) * 3 * Config.dt + self.ay - 3 * self.ay * Config.dt
            damping = 1
            self.bx = square.x - damping * (self.ax - square.x) - zoomed_width / 2 - zoomed_width / 2 * damping
            self.by = square.y - damping * (self.ay - square.y) - zoomed_height / 2 - zoomed_height / 2 * damping
            self.x = self.x * (1 - 3 * Config.dt) + self.bx * 3 * Config.dt
            self.y = self.y * (1 - 3 * Config.dt) + self.by * 3 * Config.dt
