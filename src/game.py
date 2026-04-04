import pygame
import pygame_gui
import settings
from player.entity import Player

class Game:
    def __init__(self): #TODO : add debug mode
        pygame.init()
        if settings.MONITOR_SIZE_OVERRIDE:
            display_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        else:
            display_size = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(display_size)
        pygame.display.set_caption("Project Hadron")
        self.ui_manager = pygame_gui.UIManager(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                

            keys_pressed = pygame.key.get_pressed()
            self.player.controller.input(keys_pressed)
            
            self.all_sprites.update()

            # Draw
            self.screen.fill((0, 0, 0))  # Clear screen with black
            self.all_sprites.draw(self.screen)
            
            pygame.display.flip()  
            self.clock.tick(settings.FPS)

        pygame.quit()
