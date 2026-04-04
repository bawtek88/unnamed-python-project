from .stats import PlayerStats
from .controller import PlayerController
from .inventory import Inventory

import pygame
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
        self.position = pygame.Vector2(self.rect.topleft)
        
        self.stats = PlayerStats()
        self.controller = PlayerController(self)
        self.inventory = Inventory(self.stats.basic_inventory_capacity)

    def _move(self, x_direction, y_direction, time_delta):
        self.position.x += x_direction * self.stats.speed * time_delta
        self.position.y += y_direction * self.stats.speed * time_delta
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def move_up(self, time_delta):
        self._move(0, -1, time_delta)

    def move_down(self, time_delta):
        self._move(0, 1, time_delta)

    def move_left(self, time_delta):
        self._move(-1, 0, time_delta)

    def move_right(self, time_delta):
        self._move(1, 0, time_delta)