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

    def move_and_collide(self, move_direction, time_delta, solid_objects):
        if move_direction.length_squared() == 0:
            return

        dx = move_direction.x * self.stats.speed * time_delta
        dy = move_direction.y * self.stats.speed * time_delta

        self.rect.x += round(dx)

        for obj in solid_objects:
            if obj.collision_rect is None:
                continue

            if self.rect.colliderect(obj.collision_rect):
                if dx > 0:
                    self.rect.right = obj.collision_rect.left
                elif dx < 0:
                    self.rect.left = obj.collision_rect.right

        self.rect.y += round(dy)

        for obj in solid_objects:
            if obj.collision_rect is None:
                continue

            if self.rect.colliderect(obj.collision_rect):
                if dy > 0:
                    self.rect.bottom = obj.collision_rect.top
                elif dy < 0:
                    self.rect.top = obj.collision_rect.bottom

        self.position.update(self.rect.topleft)

    def get_pos(self):
        return self.rect.x, self.rect.y
    
    def get_stamina(self):
        return self.stats.current_stamina
