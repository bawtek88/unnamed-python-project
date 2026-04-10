import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset = pygame.Vector2(0,0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing_factor = 0.05
    def snap(self, target_rect):
        target_x = target_rect.centerx - self.screen_width // 2
        target_y = target_rect.centery - self.screen_height // 2

        self.offset.x += (target_x - self.offset.x) * self.smoothing_factor
        self.offset.y += (target_y - self.offset.y) * self.smoothing_factor

    def apply_rect(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    



