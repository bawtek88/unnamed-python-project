from .stats import PlayerStats
from .controller import PlayerController

import settings
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.stats = PlayerStats()
        self.controller = PlayerController(self)

    def move_up(self):
        self.rect.y -= self.stats.speed * (1 / settings.FPS)  # Assuming 60 FPS

    def move_down(self):
        self.rect.y += self.stats.speed * (1 / settings.FPS)

    def move_left(self):
        self.rect.x -= self.stats.speed * (1 / settings.FPS)

    def move_right(self):
        self.rect.x += self.stats.speed * (1 / settings.FPS)