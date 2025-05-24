import pygame
import sys
import os
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Game states
class GameState:
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

# Button class with improved click detection
class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(None, 32)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self.rect.collidepoint(event.pos)
            if clicked:
                print(f"Button '{self.text}' clicked at {event.pos}")
            return clicked
        return False

# Simple player class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE - 4, TILE_SIZE - 4)
        self.color = BLUE
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
    
    def update(self):
        # Apply gravity
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10
        
        # Apply velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT - 50:  # Ground level
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Simple game class
class SimpleGame:
    def __init__(self):
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Dimensional Shift Game")
        self.clock = pygame.time.Clock()
        
        # Set up fonts
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        # Set up game state
        self.game_state = GameState.MAIN_MENU
        self.player = None
        
        # Create buttons for main menu
        self.main_menu_buttons = [
            Button(SCREEN_WIDTH//2 - 100, 200, 200, 50, "Start Game"),
            Button(SCREEN_WIDTH//2 - 100, 270, 200, 50, "Controls"),
            Button(SCREEN_WIDTH//2 - 100, 340, 200, 50, "Quit")
        ]
        
        # Create buttons for pause menu
        self.pause_menu_buttons = [
            Button(SCREEN_WIDTH//2 - 100, 200, 200, 50, "Resume"),
            Button(SCREEN_WIDTH//2 - 100, 270, 200, 50, "Main Menu")
        ]
        
        # Try to load a sound
        try:
            self.menu_sound = pygame.mixer.Sound("assets/sounds/menu_select.wav")
        except:
            # Create a simple beep sound if file not found
            self.menu_sound = pygame.mixer.Sound.from_buffer(bytes([128] * 1000), 1000)
    
    def start_game(self):
        self.game_state = GameState.PLAYING
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.PAUSED
                    elif self.game_state == GameState.PAUSED:
                        self.game_state = GameState.PLAYING
                    else:
                        return False
            
            # Handle mouse clicks for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.game_state == GameState.MAIN_MENU:
                    for i, button in enumerate(self.main_menu_buttons):
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            print(f"Main menu button {i} clicked")
                            if i == 0:  # Start Game
                                self.start_game()
                            elif i == 1:  # Controls
                                print("Controls button clicked - would show controls")
                            elif i == 2:  # Quit
                                return False
                
                elif self.game_state == GameState.PAUSED:
                    for i, button in enumerate(self.pause_menu_buttons):
                        if button.is_clicked(event):
                            self.menu_sound.play()
                            print(f"Pause menu button {i} clicked")
                            if i == 0:  # Resume
                                self.game_state = GameState.PLAYING
                            elif i == 1:  # Main Menu
                                self.game_state = GameState.MAIN_MENU
        
        # Handle player controls when playing
        if self.game_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            # Handle movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.vel_x = -5
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.vel_x = 5
            else:
                self.player.vel_x = 0
            
            # Handle jumping
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.on_ground:
                self.player.vel_y = -10
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        if self.game_state == GameState.MAIN_MENU:
            for button in self.main_menu_buttons:
                button.update(mouse_pos)
        elif self.game_state == GameState.PAUSED:
            for button in self.pause_menu_buttons:
                button.update(mouse_pos)
        
        return True
    
    def update(self):
        if self.game_state == GameState.PLAYING and self.player:
            self.player.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_main_menu(self):
        # Draw title
        title_text = "Simple Dimensional Shift"
        title_surf = self.font_large.render(title_text, True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
        
        # Draw buttons
        for button in self.main_menu_buttons:
            button.draw(self.screen)
        
        # Draw instructions
        instructions = "This is a simplified version to test button functionality."
        inst_surf = self.font_small.render(instructions, True, WHITE)
        self.screen.blit(inst_surf, (SCREEN_WIDTH//2 - inst_surf.get_width()//2, 450))
    
    def draw_game(self):
        # Draw ground
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Draw player if exists
        if self.player:
            self.player.draw(self.screen)
        
        # Draw controls info
        controls_text = "Arrow Keys/WASD to move, SPACE to jump, ESC to pause"
        controls_surf = self.font_small.render(controls_text, True, WHITE)
        self.screen.blit(controls_surf, (SCREEN_WIDTH//2 - controls_surf.get_width()//2, 20))
    
    def draw_pause_menu(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause title
        pause_text = "Game Paused"
        pause_surf = self.font_large.render(pause_text, True, WHITE)
        self.screen.blit(pause_surf, (SCREEN_WIDTH//2 - pause_surf.get_width()//2, 100))
        
        # Draw buttons
        for button in self.pause_menu_buttons:
            button.draw(self.screen)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Main function
def main():
    game = SimpleGame()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
