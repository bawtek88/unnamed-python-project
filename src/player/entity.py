from .stats import PlayerStats
from .controller import PlayerController
from .inventory import Inventory

import settings
from pygame import Surface
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((50, 50))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.stats = PlayerStats()
        self.controller = PlayerController(self)
        self.inventory = Inventory(self.stats.basic_inventory_capacity)

    def move_up(self):
        self.rect.y -= self.stats.speed * (1 / settings.FPS_LIMIT)  # Assuming 60 FPS_LIMIT

    def move_down(self):
        self.rect.y += self.stats.speed * (1 / settings.FPS_LIMIT)

    def move_left(self):
        self.rect.x -= self.stats.speed * (1 / settings.FPS_LIMIT)

    def move_right(self):
        self.rect.x += self.stats.speed * (1 / settings.FPS_LIMIT)