from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .entity import Player


class PlayerController:
    def __init__(self, player):
        self.player = player

    def input(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.player.move_up()
        if keys_pressed[pygame.K_s]:
            self.player.move_down()
        if keys_pressed[pygame.K_a]:
            self.player.move_left()
        if keys_pressed[pygame.K_d]:
            self.player.move_right()
        if keys_pressed[pygame.K_LSHIFT] and self.player.stats.current_stamina > 0:
            self.player.stats.speed = self.player.stats.default_speed * 2
            self.player.stats.current_stamina -= 1
        else:
            self.player.stats.speed = self.player.stats.default_speed
            if self.player.stats.current_stamina < self.player.stats.max_stamina and not keys_pressed[pygame.K_LSHIFT]:
                self.player.stats.current_stamina += 1