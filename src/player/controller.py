from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .entity import Player


class PlayerController:
    def __init__(self, player):
        self.player = player

    def input(self, keys_pressed, time_delta):
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
            
        self.player.move(move_direction, time_delta)
        
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