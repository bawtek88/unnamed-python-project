import logging
import pygame
import pygame_gui

import settings
from player.entity import Player
import util.debug_mode as debug_mode

class Game:
    def __init__(self):
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
        
        self._fps_font = pygame.font.Font(None, 28)
        self._fps_refresh_interval = 0.5
        self._fps_refresh_accumulator = 0.0
        self._fps_surface = self._fps_font.render("FPS:", True, (255, 255, 255))
        self._fps_rect = self._fps_surface.get_rect(topright=(self.screen.get_width() - 12, 12))
        
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)

        self.logger = logging.getLogger("hadron")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            stream = logging.StreamHandler()
            stream.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
            self.logger.addHandler(stream)

        self.debug_console = None
        self._skip_next_debug_textinput = False
        
        if settings.DEBUG_MODE:
            registry = debug_mode.DebugCommandRegistry()

            self.debug_console = debug_mode.DebugConsole(
                manager=self.ui_manager,
                screen_size=self.screen.get_size(),
                command_registry=registry,
                max_lines=settings.DEBUG_CONSOLE_MAX_LINES,
                start_visible=settings.DEBUG_CONSOLE_START_VISIBLE,
                margin=settings.DEBUG_CONSOLE_MARGIN,
                panel_height=settings.DEBUG_CONSOLE_HEIGHT,
            )

            def cmd_help(args, ctx):
                ctx.log("Commands: " + ", ".join(registry.names()))

            def cmd_clear(args, ctx):
                self.debug_console.clear()

            def cmd_fps_limit(args, ctx):
                ctx.log(f"FPS_LIMIT: {ctx.get_fps():.0f}")
            
            def cmd_screensize(args, ctx):
                width, height = self.screen.get_size()
                ctx.log(f"Screen size: {width}x{height}")
                
            def cmd_stats(args, ctx):
                stats = self.player.stats
                ctx.log(f"Health: {stats.current_hp}/{stats.max_hp}")
                ctx.log(f"Stamina: {stats.current_stamina}/{stats.max_stamina}")
                ctx.log(f"Shield: {stats.current_shield}/{stats.max_shield}")
                ctx.log(f"Speed: {stats.speed}")
            

            registry.register("help", cmd_help)
            registry.register("clear", cmd_clear)
            registry.register("fpslimit", cmd_fps_limit)
            registry.register("screensize", cmd_screensize)
            registry.register("playerstats", cmd_stats)

            self.debug_console.attach_logger(self.logger)
            self.debug_console.push_line("Debug console ready. Type \"help\" for available commands.")

    def run(self):
        while self.running:
            time_delta = self.clock.tick(settings.FPS_LIMIT) / 1000.0
            current_fps = self.clock.get_fps()
            
            if settings.SHOW_FPS:
                self._fps_refresh_accumulator += time_delta
                if self._fps_refresh_accumulator >= self._fps_refresh_interval:
                    self._fps_refresh_accumulator = 0.0
                    fps_int = int(current_fps)
                    self._fps_surface = self._fps_font.render(f"FPS: {fps_int}", True, (255, 255, 255))
                    self._fps_rect = self._fps_surface.get_rect(topright=(self.screen.get_width() - 12, 12))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                
                if self.debug_console and self.debug_console.is_toggle_event(event):
                    self.debug_console.toggle()
                    if self.debug_console.visible:
                        self._skip_next_debug_textinput = True
                    continue

                if self._skip_next_debug_textinput and event.type == pygame.TEXTINPUT:
                    self._skip_next_debug_textinput = False
                    continue

                if self.debug_console and self.debug_console.visible:
                    if self.debug_console.process_history_event(event):
                        continue
                    self.debug_console.process_event(event)
                
                self.ui_manager.process_events(event)                


            if self.debug_console:
                self.debug_console.set_fps_snapshot(current_fps)

            console_open = bool(self.debug_console and self.debug_console.visible)
            if not console_open:
                keys_pressed = pygame.key.get_pressed()
                self.player.controller.input(keys_pressed, time_delta)

            self.all_sprites.update()
            self.ui_manager.update(time_delta)

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            
            if settings.SHOW_FPS:
                self.screen.blit(self._fps_surface, self._fps_rect)
            
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()
