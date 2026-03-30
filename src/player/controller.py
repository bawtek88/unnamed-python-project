import pygame

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