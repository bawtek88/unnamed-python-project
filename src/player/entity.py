from .stats import PlayerStats
from .controller import PlayerController
from .inventory import Inventory

import pygame
import settings
from pygame import Surface
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        #self.image = Surface((50, 50))
        #self.image.fill((255, 255, 255))
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        self.position = pygame.Vector2(self.rect.topleft)
        
        self.stats = PlayerStats()
        self.controller = PlayerController(self)
        self.inventory = Inventory(self.stats.basic_inventory_capacity)

    def move(self, direction, time_delta):
        self.position.x += direction.x * self.stats.speed * time_delta
        self.position.y += direction.y * self.stats.speed * time_delta
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def get_pos(self):
        return self.position.x, self.position.y