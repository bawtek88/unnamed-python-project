from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .entity import Player


class PlayerController:
    def __init__(self, player):
        self.player = player
    
    def input(self, keys_pressed, time_delta, solid_objects = None):
        if solid_objects is None:
            solid_objects = []
        
        self.manage_sprint(keys_pressed, time_delta)

        move_direction = pygame.Vector2(0, 0)

        if keys_pressed[pygame.K_w]:
            move_direction.y -= 1
        if keys_pressed[pygame.K_s]:
            move_direction.y += 1
        if keys_pressed[pygame.K_a]:
            move_direction.x -= 1
        if keys_pressed[pygame.K_d]:
            move_direction.x += 1
            
        if move_direction.length() > 0:
            move_direction = move_direction.normalize()
            
        self.player.move_and_collide(move_direction, time_delta, solid_objects)
    
    def manage_sprint(self, keys_pressed, time_delta):
        sprinting = keys_pressed[pygame.K_LSHIFT] and self.player.stats.current_stamina > 0

        if sprinting:
            self.player.stats.speed = self.player.stats.default_speed * 2
            self.player.stats.stamina_accumulator -= self.player.stats.stamina_depletion_rate * time_delta
        else:
            self.player.stats.speed = self.player.stats.default_speed
            if self.player.stats.current_stamina < self.player.stats.max_stamina:
                self.player.stats.stamina_accumulator += self.player.stats.stamina_regen_rate * time_delta
        
        while self.player.stats.stamina_accumulator <= -1:
            self.player.stats.current_stamina -= 1
            self.player.stats.stamina_accumulator += 1
        while self.player.stats.stamina_accumulator >= 1:
            self.player.stats.current_stamina += 1
            self.player.stats.stamina_accumulator -= 1
        
        
        self.player.stats.current_stamina = max(0, min(self.player.stats.max_stamina, self.player.stats.current_stamina))

    def move_and_collide(self, move_direction, time_delta, solid_objects):
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

        for obj in solid_objects:
            if obj.collision_rect is None:
                continue

        if self.rect.colliderect(obj.collision_rect):
            if dy > 0:
                self.rect.bottom = obj.collision_rect.top
            elif dy < 0:
                self.rect.top = obj.collision_rect.bottom