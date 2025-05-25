import pygame
import sys
import os
import math
import random
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Import game modules
from game_engine import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE, GameState,
    Dimension, Button, TextEffect, Camera, ParallaxBackground,
    SaveSystem, load_image, load_sound
)
from game_objects import Player, Wall, Platform, DimensionPortal, Collectible
from level_manager import LevelManager
from customization import CustomizationMenu

# Create assets directories if they don't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)

class Game:
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dimensional Shift Puzzle")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        # Load sounds
        self.menu_sound = load_sound("menu_select.wav")
        self.level_complete_sound = load_sound("level_complete.wav")
        self.game_over_sound = load_sound("game_over.wav")
        self.game_complete_sound = load_sound("game_complete.wav")
        
        # Set up game state
        self.game_state = GameState.MAIN_MENU
        self.level_manager = LevelManager()
        self.player = None
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.text_effects = []
        self.message_timer = 0
        self.total_score = 0
        self.collected_items = 0
        self.total_items = 0
        self.save_system = SaveSystem()
        
        # Background and character settings
        self.current_bg_style = "default"
        self.current_character = "default"
        
        # Game enhancement attributes
        self.difficulty_level = 1  # 1=Easy, 2=Medium, 3=Hard
        self.enable_particles = True
        self.enable_sound_effects = True
        self.enable_music = True
        self.show_fps = False
        self.fullscreen = False
        
        # Create customization menu
        self.customization_menu = CustomizationMenu(self.screen, self.font_large, self.font_medium)
        self.show_customization = False
        
        # Create buttons for main menu with improved colors
        self.main_menu_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 180, 300, 50, "Start Game", (50, 100, 200), (100, 150, 255)),
            Button(SCREEN_WIDTH//2 - 150, 240, 300, 50, "Customize", (50, 150, 50), (100, 200, 100)),
            Button(SCREEN_WIDTH//2 - 150, 300, 300, 50, "Tutorial", (150, 100, 50), (200, 150, 100)),
            Button(SCREEN_WIDTH//2 - 150, 360, 300, 50, "Controls", (150, 50, 150), (200, 100, 200)),
            Button(SCREEN_WIDTH//2 - 150, 420, 300, 50, "Settings", (100, 100, 150), (150, 150, 200)),
            Button(SCREEN_WIDTH//2 - 150, 480, 300, 50, "Quit", (150, 50, 50), (200, 100, 100))
        ]
        
        # Create buttons for pause menu with improved colors
        self.pause_menu_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 200, 300, 50, "Resume", (50, 100, 200), (100, 150, 255)),
            Button(SCREEN_WIDTH//2 - 150, 260, 300, 50, "Customize", (50, 150, 50), (100, 200, 100)),
            Button(SCREEN_WIDTH//2 - 150, 320, 300, 50, "Controls", (150, 50, 150), (200, 100, 200)),
            Button(SCREEN_WIDTH//2 - 150, 380, 300, 50, "Settings", (100, 100, 150), (150, 150, 200)),
            Button(SCREEN_WIDTH//2 - 150, 440, 300, 50, "Main Menu", (150, 50, 50), (200, 100, 100))
        ]
        
        # Create buttons for controls screen
        self.controls_buttons = [
            Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Back", (100, 100, 150), (150, 150, 200))
        ]
        
        # Create buttons for settings screen
        self.settings_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 160 + i*70, 300, 50, text, color, hover)
            for i, (text, color, hover) in enumerate([
                ("Difficulty: Easy", (50, 100, 200), (100, 150, 255)),
                ("Particles: On", (50, 150, 50), (100, 200, 100)),
                ("Sound Effects: On", (150, 100, 50), (200, 150, 100)),
                ("Music: On", (100, 100, 150), (150, 150, 200)),
                ("Show FPS: Off", (150, 50, 150), (200, 100, 200)),
                ("Back", (150, 50, 50), (200, 100, 100)),
            ])
        ]
        
        # Create buttons for credits screen
        self.credits_buttons = [
            Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Back", (100, 100, 150), (150, 150, 200))
        ]

        # Create buttons for tutorial screen
        self.tutorial_buttons = [
            Button(SCREEN_WIDTH//2 - 100, 500, 200, 50, "Back", (100, 100, 150), (150, 150, 200))
        ]
        
        # Create background
        self.load_background()
        
        # Count total collectibles across all levels
        self.count_total_collectibles()
        
        # Initialize music
        try:
            if self.enable_music:
                pygame.mixer.music.load("assets/sounds/menu_music.mp3")
                pygame.mixer.music.play(-1)  # Loop indefinitely
        except:
            pass

    def draw_controls(self):
        self.screen.fill((20, 20, 50))
        # Draw title
        title_text = "Game Controls"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        controls_info = [
            "Movement Controls:",
            "- Arrow Keys or WASD: Move left/right",
            "- Space or Up Arrow or W: Jump",
            "- ESC: Pause game",
            "",
            "Dimension Information:",
            "- Blue (Normal): Standard physics",
            "- Red (Inverse): Gravity is reversed",
            "- Purple (Ethereal): Pass through special walls",
            "- Yellow (Time): Slowed physics for precision",
            "- Cyan (Magnetic): Attracted to metal objects",
            "",
            "Game Objectives:",
            "- Collect all items in each level",
            "- Reach the exit portal",
            "- Use dimension portals to change your physics",
            "- Avoid hazards and obstacles"
        ]
        y_offset = 120
        for text in controls_info:
            if text == "":
                y_offset += 10
                continue
            if ":" in text and text[-1] == ":":
                text_surf = self.font_medium.render(text, True, (255, 255, 100))
            else:
                text_surf = self.font_small.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_offset))
            y_offset += 30
        # Draw back button
        for button in self.controls_buttons:
            button.draw(self.screen)
    # Draw "Back" button in-game if in controls screen
    # (Optional: Only show if called from pause menu or in-game)
    # You can add a hint or highlight if needed    
    def load_background(self):
        try:
            # Try to load background based on current style
            if self.current_bg_style == "default":
                bg_images = [
                    "assets/images/bg_layer1.png",
                    "assets/images/bg_layer2.png",
                    "assets/images/bg_layer3.png"
                ]
            else:
                bg_images = [
                    f"assets/images/bg_{self.current_bg_style}_layer1.png",
                    f"assets/images/bg_{self.current_bg_style}_layer2.png",
                    f"assets/images/bg_{self.current_bg_style}_layer3.png"
                ]
            self.background = ParallaxBackground(bg_images, [0.2, 0.5, 0.8])
        except Exception as e:
            print(f"Failed to load background: {e}")
            # Create a simple gradient background if images not found
            self.background = None
    
    def count_total_collectibles(self):
        self.total_items = 0
        for level in self.level_manager.levels:
            self.total_items += len(level.collectibles)
    
    def start_game(self):
        self.game_state = GameState.PLAYING
        self.level_manager.current_level = 0
        self.init_level()
        self.total_score = 0
        self.collected_items = 0
        
        # Change music to level music
        try:
            current_level = self.level_manager.get_current_level()
            if current_level.music_path and os.path.exists(current_level.music_path):
                pygame.mixer.music.load(current_level.music_path)
                pygame.mixer.music.play(-1)
        except:
            pass
    
    def init_level(self):
        current_level = self.level_manager.get_current_level()
        self.player = Player(*current_level.start_pos)
        
        # Set character type
        self.player.character_type = self.current_character
        self.player.load_animations()
        
        # Set ethereal objects for player
        self.player.ethereal_objects = []
        for wall in current_level.ethereal_walls:
            self.player.ethereal_objects.append(wall)
        
        # Set metal objects for player
        self.player.metal_objects = []
        for wall in current_level.metal_walls:
            self.player.metal_objects.append(wall)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle customization menu if active
            if self.show_customization:
                character, bg_style, action = self.customization_menu.handle_events(event)
                if character:
                    self.current_character = character
                    if self.player:
                        self.player.character_type = character
                        self.player.load_animations()
                if bg_style:
                    self.current_bg_style = bg_style
                    self.load_background()
                if action == "back":
                    self.show_customization = False
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.PAUSED
                    elif self.game_state == GameState.PAUSED:
                        self.game_state = GameState.PLAYING
                    elif self.game_state in [GameState.CONTROLS, GameState.SETTINGS, GameState.CREDITS, GameState.TUTORIAL]:
                        self.game_state = GameState.MAIN_MENU
                    else:
                        return False
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.LEVEL_COMPLETE:
                        self.next_level()
                    elif self.game_state == GameState.GAME_COMPLETE or self.game_state == GameState.GAME_OVER:
                        self.game_state = GameState.MAIN_MENU
                        try:
                            if self.enable_music:
                                pygame.mixer.music.load("assets/sounds/menu_music.mp3")
                                pygame.mixer.music.play(-1)
                        except:
                            pass
                    elif self.game_state == GameState.TUTORIAL:
                        self.game_state = GameState.MAIN_MENU
                if event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_state == GameState.MAIN_MENU:
                    for i, button in enumerate(self.main_menu_buttons):
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            if i == 0:  # Start Game
                                self.start_game()
                            elif i == 1:  # Customize
                                self.show_customization = True
                            elif i == 2:  # Tutorial
                                self.game_state = GameState.TUTORIAL
                            elif i == 3:  # Controls
                                self.game_state = GameState.CONTROLS
                            elif i == 4:  # Settings
                                self.game_state = GameState.SETTINGS
                                self.update_settings_buttons()
                            elif i == 5:  # Quit
                                return False
                elif self.game_state == GameState.PAUSED:
                    for i, button in enumerate(self.pause_menu_buttons):
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            if i == 0:  # Resume
                                self.game_state = GameState.PLAYING
                            elif i == 1:  # Customize
                                self.show_customization = True
                            elif i == 2:  # Controls
                                self.game_state = GameState.CONTROLS
                            elif i == 3:  # Settings
                                self.game_state = GameState.SETTINGS
                                self.update_settings_buttons()
                            elif i == 4:  # Main Menu
                                self.game_state = GameState.MAIN_MENU
                                try:
                                    if self.enable_music:
                                        pygame.mixer.music.load("assets/sounds/menu_music.mp3")
                                        pygame.mixer.music.play(-1)
                                except:
                                    pass
                elif self.game_state == GameState.SETTINGS:
                    for i, button in enumerate(self.settings_buttons):
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            if i == 0:  # Difficulty
                                self.difficulty_level = (self.difficulty_level % 3) + 1
                            elif i == 1:  # Particles
                                self.enable_particles = not self.enable_particles
                            elif i == 2:  # Sound Effects
                                self.enable_sound_effects = not self.enable_sound_effects
                            elif i == 3:  # Music
                                self.enable_music = not self.enable_music
                                if self.enable_music:
                                    try:
                                        pygame.mixer.music.load("assets/sounds/menu_music.mp3")
                                        pygame.mixer.music.play(-1)
                                    except:
                                        pass
                                else:
                                    pygame.mixer.music.stop()
                            elif i == 4:  # Show FPS
                                self.show_fps = not self.show_fps
                            elif i == 5:  # Back
                                self.game_state = GameState.MAIN_MENU
                            self.update_settings_buttons()
                elif self.game_state == GameState.CREDITS:
                    for button in self.credits_buttons:
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            self.game_state = GameState.MAIN_MENU
                elif self.game_state == GameState.CONTROLS:
                    for button in self.controls_buttons:
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            self.game_state = GameState.MAIN_MENU
                elif self.game_state == GameState.TUTORIAL:
                    for button in self.tutorial_buttons:
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            self.game_state = GameState.MAIN_MENU

        # Handle player controls when playing
        if self.game_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.can_jump:
                self.player.jump()
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        if self.game_state == GameState.MAIN_MENU:
            for button in self.main_menu_buttons:
                button.update(mouse_pos)
        elif self.game_state == GameState.PAUSED:
            for button in self.pause_menu_buttons:
                button.update(mouse_pos)
        elif self.game_state == GameState.SETTINGS:
            for button in self.settings_buttons:
                button.update(mouse_pos)
        elif self.game_state == GameState.CREDITS:
            for button in self.credits_buttons:
                button.update(mouse_pos)
        elif self.game_state == GameState.TUTORIAL:
            for button in self.tutorial_buttons:
                button.update(mouse_pos)
        return True
    
    def update_settings_buttons(self):
        """Update settings button text based on current settings"""
        difficulty_names = ["Easy", "Medium", "Hard"]
        self.settings_buttons[0].text = f"Difficulty: {difficulty_names[self.difficulty_level-1]}"
        self.settings_buttons[1].text = f"Particles: {'On' if self.enable_particles else 'Off'}"
        self.settings_buttons[2].text = f"Sound Effects: {'On' if self.enable_sound_effects else 'Off'}"
        self.settings_buttons[3].text = f"Music: {'On' if self.enable_music else 'Off'}"
        self.settings_buttons[4].text = f"Show FPS: {'On' if self.show_fps else 'Off'}"
    
    def update(self):
        if self.game_state == GameState.PLAYING:
            current_level = self.level_manager.get_current_level()
            
            # Update level elements
            current_level.update()
            
            # Update player
            old_score = self.player.score
            old_collectibles = len(current_level.collectibles)
            
            self.player.update(
                current_level.walls, 
                current_level.platforms + current_level.moving_platforms, 
                current_level.dimension_portals, 
                current_level.collectibles,
                current_level.hazards,
                current_level.powerups
            )
            
            # Check if player collected items
            if len(current_level.collectibles) < old_collectibles:
                self.collected_items += old_collectibles - len(current_level.collectibles)
                
                # Create text effect for score
                score_gained = self.player.score - old_score
                if score_gained > 0:
                    self.text_effects.append(
                        TextEffect(f"+{score_gained}", 
                                  self.player.x + self.player.width // 2, 
                                  self.player.y - 20,
                                  (255, 255, 0))
                    )
            
            # Update camera to follow player
            self.camera.update(self.player.x + self.player.width // 2, 
                              self.player.y + self.player.height // 2)
            
            # Check if player reached the end
            if pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height).colliderect(current_level.end_rect):
                if len(current_level.collectibles) == 0:  # All collectibles must be collected
                    self.game_state = GameState.LEVEL_COMPLETE
                    self.message_timer = 180  # Show message for 3 seconds
                    self.level_complete_sound.play()
                    self.total_score += self.player.score
            
            # Check if player died
            if self.player.health <= 0 or self.player.y > SCREEN_HEIGHT + 100 or self.player.y < -100:
                self.game_state = GameState.GAME_OVER
                self.message_timer = 180
                self.game_over_sound.play()
        
        # Update text effects
        for effect in self.text_effects[:]:
            if not effect.update():
                self.text_effects.remove(effect)
        
        # Update timers
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw appropriate screen based on game state
        if self.game_state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.PAUSED:
            self.draw_game()  # Draw game in background
            self.draw_pause_menu()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.draw_game()  # Draw game in background
            self.draw_level_complete()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game()  # Draw game in background
            self.draw_game_over()
        elif self.game_state == GameState.GAME_COMPLETE:
            self.draw_game_complete()
        elif self.game_state == GameState.TUTORIAL:
            self.draw_tutorial()
        elif self.game_state == GameState.CONTROLS:
            self.draw_controls()
        elif self.game_state == GameState.SETTINGS:
            self.draw_settings()
        elif self.game_state == GameState.CREDITS:
            self.draw_credits()
        
        # Draw customization menu if active
        if self.show_customization:
            self.customization_menu.draw()
        
        # Draw FPS counter if enabled
        if self.show_fps:
            fps = int(self.clock.get_fps())
            fps_text = f"FPS: {fps}"
            fps_surf = self.font_small.render(fps_text, True, (255, 255, 0))
            self.screen.blit(fps_surf, (SCREEN_WIDTH - fps_surf.get_width() - 10, 10))
        
        pygame.display.flip()
    
    def draw_main_menu(self):
        # Draw background
        if self.background:
            self.background.draw(self.screen)
        else:
            # Draw gradient background
            for y in range(SCREEN_HEIGHT):
                color_val = int(y / SCREEN_HEIGHT * 100)
                pygame.draw.line(self.screen, (0, 0, color_val), (0, y), (SCREEN_WIDTH, y))
        
        # Draw title
        title_text = "Dimensional Shift Puzzle"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
        
        # Draw buttons
        for button in self.main_menu_buttons:
            button.draw(self.screen)
        
        # Draw version and credits
        version_text = "Version 1.0"
        version_surf = self.font_small.render(version_text, True, (200, 200, 200))
        self.screen.blit(version_surf, (10, SCREEN_HEIGHT - 30))
    
    def draw_settings(self):
        self.screen.fill((30, 40, 60))
        title_text = "Game Settings"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))

        descriptions = [
            "Changes game difficulty (enemy speed, hazard damage)",
            "Toggles visual particle effects (impacts performance)",
            "Toggles sound effects during gameplay",
            "Toggles background music",
            "Shows current frames per second (FPS)"
        ]

        for i, button in enumerate(self.settings_buttons):
            # Draw description above the first 5 buttons
            if i < len(descriptions):
                desc_surf = self.font_small.render(descriptions[i], True, (200, 200, 200))
                desc_y = button.rect.top - desc_surf.get_height() - 4
                self.screen.blit(desc_surf, (SCREEN_WIDTH//2 - desc_surf.get_width()//2, desc_y))
            button.draw(self.screen)

        # Draw keyboard shortcuts at the bottom
        shortcuts_text = "Keyboard Shortcuts: F3 - Toggle FPS, F11 - Toggle Fullscreen"
        shortcuts_surf = self.font_small.render(shortcuts_text, True, (200, 200, 200))
        self.screen.blit(shortcuts_surf, (SCREEN_WIDTH//2 - shortcuts_surf.get_width()//2, SCREEN_HEIGHT - 40))
    
    def draw_credits(self):
        # Draw background
        self.screen.fill((30, 20, 40))
        
        # Draw title
        title_text = "Credits"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Draw credits information
        credits_info = [
            "Dimensional Shift Puzzle",
            "",
            "Game Design and Programming:",
            "- Created as a unique puzzle platformer with dimensional shifting mechanics",
            "",
            "Graphics:",
            "- Procedurally generated graphics and animations",
            "- Character designs and background styles",
            "",
            "Sound Effects:",
            "- Jump, collect, and dimension shift sounds",
            "",
            "Music:",
            "- Menu and level background music",
            "",
            "Special Thanks:",
            "- To all players for enjoying this game!",
            "",
            "© 2025 Dimensional Shift Puzzle"
        ]
        
        y_offset = 120
        for text in credits_info:
            if text == "":
                y_offset += 10
                continue
                
            if ":" in text and text[-1] == ":":
                # Section header
                text_surf = self.font_medium.render(text, True, (255, 200, 100))
            elif text == credits_info[0]:
                # Game title
                text_surf = self.font_medium.render(text, True, (100, 200, 255))
            elif text == credits_info[-1]:
                # Copyright
                text_surf = self.font_small.render(text, True, (200, 200, 200))
            else:
                # Regular text
                text_surf = self.font_small.render(text, True, (255, 255, 255))
                
            self.screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_offset))
            y_offset += 30
        
        # Draw back button
        for button in self.credits_buttons:
            button.draw(self.screen)
    
    def draw_game(self):
        current_level = self.level_manager.get_current_level()
        
        # Draw background
        if self.background:
            self.background.draw(self.screen)
        else:
            # Always draw a base color first
            self.screen.fill((0, 0, 50))  # Dark blue background
            
            # Try to load level-specific background
            try:
                import os
                base_path = os.path.dirname(os.path.abspath(__file__))
                
                # Try style-specific background first
                if self.current_bg_style != "default":
                    bg_path = os.path.join(base_path, "assets", "images", 
                                         f"background_{self.current_bg_style}_{self.level_manager.current_level + 1}.png")
                else:
                    bg_path = os.path.join(base_path, "assets", "images", 
                                         f"background_{self.level_manager.current_level + 1}.png")
                
                if os.path.exists(bg_path):
                    print(f"Loading level background: {bg_path}")
                    bg_image = pygame.image.load(bg_path)
                    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    self.screen.blit(bg_image, (0, 0))
            except Exception as e:
                print(f"Failed to load level background: {e}")
        
        # Draw level
        current_level.draw(self.screen, self.camera)
        
        # Draw player
        self.player.draw(self.screen, self.camera)
        
        # Draw text effects
        for effect in self.text_effects:
            effect.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
    
    def draw_ui(self):
        # Draw current dimension
        dimension_text = f"Dimension: {self.player.dimension.name}"
        dimension_surf = self.font_small.render(dimension_text, True, (255, 255, 255))
        self.screen.blit(dimension_surf, (10, 10))
        
        # Draw health bar
        health_width = 150
        health_height = 15
        health_x = 10
        health_y = 40
        health_fill = max(0, min(self.player.health / self.player.max_health, 1)) * health_width
        
        pygame.draw.rect(self.screen, (100, 100, 100), (health_x, health_y, health_width, health_height))
        pygame.draw.rect(self.screen, (255, 0, 0), (health_x, health_y, health_fill, health_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (health_x, health_y, health_width, health_height), 1)
        
        health_text = f"Health: {self.player.health}/{self.player.max_health}"
        health_surf = self.font_small.render(health_text, True, (255, 255, 255))
        self.screen.blit(health_surf, (health_x + health_width + 10, health_y))
        
        # Draw collectibles count
        current_level = self.level_manager.get_current_level()
        collectibles_text = f"Collectibles: {len(current_level.collectibles)} remaining"
        collectibles_surf = self.font_small.render(collectibles_text, True, (255, 255, 255))
        self.screen.blit(collectibles_surf, (10, 70))
        
        # Draw score
        score_text = f"Score: {self.player.score}"
        score_surf = self.font_small.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 100))
        
        # Draw level number
        level_text = f"Level: {self.level_manager.current_level + 1}/{len(self.level_manager.levels)}"
        level_surf = self.font_small.render(level_text, True, (255, 255, 255))
        self.screen.blit(level_surf, (SCREEN_WIDTH - level_surf.get_width() - 10, 40))
        
        # Draw difficulty level if not on easy
        if self.difficulty_level > 1:
            difficulty_names = ["", "Easy", "Medium", "Hard"]
            diff_text = f"Difficulty: {difficulty_names[self.difficulty_level]}"
            diff_surf = self.font_small.render(diff_text, True, (255, 200, 100))
            self.screen.blit(diff_surf, (SCREEN_WIDTH - diff_surf.get_width() - 10, 70))
        
        # Draw controls reminder
        controls_text = "Controls: Arrow Keys/WASD to move, SPACE to jump, ESC to pause"
        controls_surf = self.font_small.render(controls_text, True, (200, 200, 200))
        self.screen.blit(controls_surf, (SCREEN_WIDTH//2 - controls_surf.get_width()//2, SCREEN_HEIGHT - 30))
    
    def draw_pause_menu(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause title
        pause_text = "Game Paused"
        pause_surf = self.font_large.render(pause_text, True, (255, 255, 255))
        self.screen.blit(pause_surf, (SCREEN_WIDTH//2 - pause_surf.get_width()//2, 100))
        
        # Draw buttons
        for button in self.pause_menu_buttons:
            button.draw(self.screen)
    
    def draw_level_complete(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw level complete message
        complete_text = "Level Complete!"
        complete_surf = self.font_large.render(complete_text, True, (255, 255, 255))
        self.screen.blit(complete_surf, (SCREEN_WIDTH//2 - complete_surf.get_width()//2, 100))
        
        # Draw score
        score_text = f"Score: {self.player.score}"
        score_surf = self.font_medium.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, 180))
        
        # Draw continue message
        if self.level_manager.current_level < len(self.level_manager.levels) - 1:
            continue_text = "Press SPACE to continue to next level"
        else:
            continue_text = "Press SPACE to complete the game"
            self.game_state = GameState.GAME_COMPLETE
            self.game_complete_sound.play()
            
        continue_surf = self.font_medium.render(continue_text, True, (255, 255, 255))
        self.screen.blit(continue_surf, (SCREEN_WIDTH//2 - continue_surf.get_width()//2, 250))
    
    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over message
        over_text = "Game Over"
        over_surf = self.font_large.render(over_text, True, (255, 0, 0))
        self.screen.blit(over_surf, (SCREEN_WIDTH//2 - over_surf.get_width()//2, 100))
        
        # Draw score
        score_text = f"Final Score: {self.total_score + self.player.score}"
        score_surf = self.font_medium.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, 180))
        
        # Draw continue message
        continue_text = "Press SPACE to return to main menu"
        continue_surf = self.font_medium.render(continue_text, True, (255, 255, 255))
        self.screen.blit(continue_surf, (SCREEN_WIDTH//2 - continue_surf.get_width()//2, 250))
    
    def draw_game_complete(self):
        # Draw background
        if self.background:
            self.background.draw(self.screen)
        else:
            # Draw celebratory background
            for y in range(SCREEN_HEIGHT):
                color_val = int(y / SCREEN_HEIGHT * 255)
                pygame.draw.line(self.screen, (0, color_val, color_val), (0, y), (SCREEN_WIDTH, y))
        
        # Draw completion message
        complete_text = "Congratulations!"
        complete_surf = self.font_large.render(complete_text, True, (255, 255, 0))
        self.screen.blit(complete_surf, (SCREEN_WIDTH//2 - complete_surf.get_width()//2, 100))
        
        # Draw secondary message
        secondary_text = "You have completed all levels!"
        secondary_surf = self.font_medium.render(secondary_text, True, (255, 255, 255))
        self.screen.blit(secondary_surf, (SCREEN_WIDTH//2 - secondary_surf.get_width()//2, 170))
        
        # Draw score
        score_text = f"Final Score: {self.total_score + self.player.score}"
        score_surf = self.font_medium.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, 220))
        
        # Draw collectibles
        collectibles_text = f"Collectibles: {self.collected_items}/{self.total_items}"
        collectibles_surf = self.font_medium.render(collectibles_text, True, (255, 255, 255))
        self.screen.blit(collectibles_surf, (SCREEN_WIDTH//2 - collectibles_surf.get_width()//2, 270))
        
        # Draw continue message
        continue_text = "Press SPACE to return to main menu"
        continue_surf = self.font_medium.render(continue_text, True, (255, 255, 255))
        self.screen.blit(continue_surf, (SCREEN_WIDTH//2 - continue_surf.get_width()//2, 350))
    
    def draw_tutorial(self):
        # Draw background
        self.screen.fill((0, 0, 30))
        
        # Draw title
        title_text = "How to Play"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Draw tutorial text
        tutorial_texts = [
            "Welcome to Dimensional Shift Puzzle!",
            "",
            "Controls:",
            "- Arrow Keys or WASD: Move left/right",
            "- Space or Up: Jump",
            "- ESC: Pause game",
            "",
            "Dimensions:",
            "- Blue (Normal): Standard physics",
            "- Red (Inverse): Gravity is reversed",
            "- Purple (Ethereal): Pass through special walls",
            "- Yellow (Time): Slowed physics for precision",
            "- Cyan (Magnetic): Attracted to metal objects",
            "",
            "Collect all items before reaching the exit!",
            "",
            "Press SPACE or click Back to return to main menu"
        ]
        
        y_offset = 120
        for text in tutorial_texts:
            text_surf = self.font_medium.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_offset))
            y_offset += 30
        # Draw Back button
        for button in self.tutorial_buttons:
            button.draw(self.screen)

    def next_level(self):
        if self.level_manager.next_level():
            self.init_level()
            self.game_state = GameState.PLAYING
            
            # Change music to level music
            try:
                current_level = self.level_manager.get_current_level()
                if current_level.music_path and os.path.exists(current_level.music_path):
                    pygame.mixer.music.load(current_level.music_path)
                    pygame.mixer.music.play(-1)
            except:
                pass
        else:
            self.game_state = GameState.GAME_COMPLETE
            self.game_complete_sound.play()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
