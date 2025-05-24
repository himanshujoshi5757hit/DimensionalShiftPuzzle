import pygame
import sys
import math
from enum import Enum

# Initialize Pygame
pygame.init()

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

# Dimension types
class Dimension(Enum):
    NORMAL = 0    # Regular physics
    INVERSE = 1   # Inverted gravity
    ETHEREAL = 2  # Pass through certain objects
    TIME = 3      # Time slows down

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE - 4
        self.height = TILE_SIZE - 4
        self.vel_x = 0
        self.vel_y = 0
        self.can_jump = False
        self.dimension = Dimension.NORMAL
        self.color = BLUE
        self.shift_cooldown = 0
        self.ethereal_objects = []  # Objects player can pass through in ethereal dimension
    
    def update(self, walls, platforms, dimension_portals, collectibles):
        # Apply dimension-specific physics
        if self.dimension == Dimension.NORMAL:
            gravity = 0.5
            self.color = BLUE
        elif self.dimension == Dimension.INVERSE:
            gravity = -0.5
            self.color = RED
        elif self.dimension == Dimension.ETHEREAL:
            gravity = 0.5
            self.color = PURPLE
        elif self.dimension == Dimension.TIME:
            gravity = 0.25  # Half gravity in time dimension
            self.color = YELLOW
        
        # Apply gravity
        self.vel_y += gravity
        
        # Limit falling speed
        if self.vel_y > 10:
            self.vel_y = 10
        elif self.vel_y < -10:
            self.vel_y = -10
            
        # Move in x direction
        self.x += self.vel_x
        
        # Check for collisions in x direction
        self.check_collision_x(walls, platforms)
        
        # Move in y direction
        self.y += self.vel_y
        
        # Check for collisions in y direction
        self.check_collision_y(walls, platforms)
        
        # Check for dimension portals
        for portal in dimension_portals:
            if self.collides_with(portal) and self.shift_cooldown <= 0:
                self.dimension = portal.target_dimension
                self.shift_cooldown = 30  # Prevent rapid shifting
        
        # Check for collectibles
        for collectible in collectibles[:]:
            if self.collides_with(collectible):
                collectibles.remove(collectible)
        
        # Update cooldown
        if self.shift_cooldown > 0:
            self.shift_cooldown -= 1
    
    def check_collision_x(self, walls, platforms):
        # Create player rectangle for collision detection
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for wall in walls:
            # Skip ethereal walls if in ethereal dimension
            if self.dimension == Dimension.ETHEREAL and wall in self.ethereal_objects:
                continue
                
            if player_rect.colliderect(wall.rect):
                if self.vel_x > 0:  # Moving right
                    self.x = wall.rect.left - self.width
                elif self.vel_x < 0:  # Moving left
                    self.x = wall.rect.right
                self.vel_x = 0
    
    def check_collision_y(self, walls, platforms):
        self.can_jump = False
        
        # Create player rectangle for collision detection
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for wall in walls:
            # Skip ethereal walls if in ethereal dimension
            if self.dimension == Dimension.ETHEREAL and wall in self.ethereal_objects:
                continue
                
            if player_rect.colliderect(wall.rect):
                if self.vel_y > 0:  # Moving down
                    self.y = wall.rect.top - self.height
                    self.can_jump = True
                elif self.vel_y < 0:  # Moving up
                    self.y = wall.rect.bottom
                self.vel_y = 0
        
        # Check platform collisions (only from above if normal gravity, from below if inverted)
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.dimension == Dimension.NORMAL and self.vel_y > 0:
                    # Only collide when falling in normal dimension
                    self.y = platform.rect.top - self.height
                    self.can_jump = True
                    self.vel_y = 0
                elif self.dimension == Dimension.INVERSE and self.vel_y < 0:
                    # Only collide when "falling" upward in inverse dimension
                    self.y = platform.rect.bottom
                    self.can_jump = True
                    self.vel_y = 0
    
    def collides_with(self, obj):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(obj.rect)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Wall:
    def __init__(self, x, y, width, height, color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_ethereal = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Platform(Wall):
    def __init__(self, x, y, width, height=10):
        super().__init__(x, y, width, height, GREEN)

class DimensionPortal:
    def __init__(self, x, y, target_dimension):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.target_dimension = target_dimension
        
        # Set color based on target dimension
        if target_dimension == Dimension.NORMAL:
            self.color = BLUE
        elif target_dimension == Dimension.INVERSE:
            self.color = RED
        elif target_dimension == Dimension.ETHEREAL:
            self.color = PURPLE
        elif target_dimension == Dimension.TIME:
            self.color = YELLOW
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw portal effect
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        pygame.draw.circle(screen, WHITE, self.rect.center, 10)

class Collectible:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + TILE_SIZE//4, y + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
        self.color = (255, 215, 0)  # Gold color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Level:
    def __init__(self, layout, start_pos, end_pos):
        self.walls = []
        self.platforms = []
        self.dimension_portals = []
        self.collectibles = []
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.end_rect = pygame.Rect(end_pos[0], end_pos[1], TILE_SIZE, TILE_SIZE)
        
        # Parse level layout
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                pos_x = x * TILE_SIZE
                pos_y = y * TILE_SIZE
                
                if cell == '#':  # Wall
                    self.walls.append(Wall(pos_x, pos_y, TILE_SIZE, TILE_SIZE))
                elif cell == 'P':  # Platform
                    self.platforms.append(Platform(pos_x, pos_y, TILE_SIZE))
                elif cell == 'N':  # Normal dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.NORMAL))
                elif cell == 'I':  # Inverse dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.INVERSE))
                elif cell == 'E':  # Ethereal dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.ETHEREAL))
                elif cell == 'T':  # Time dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.TIME))
                elif cell == 'C':  # Collectible
                    self.collectibles.append(Collectible(pos_x, pos_y))
                elif cell == 'X':  # Ethereal wall
                    wall = Wall(pos_x, pos_y, TILE_SIZE, TILE_SIZE, (200, 200, 200))
                    wall.is_ethereal = True
                    self.walls.append(wall)
    
    def draw(self, screen):
        # Draw end point
        pygame.draw.rect(screen, GREEN, self.end_rect)
        
        # Draw level elements
        for wall in self.walls:
            wall.draw(screen)
        for platform in self.platforms:
            platform.draw(screen)
        for portal in self.dimension_portals:
            portal.draw(screen)
        for collectible in self.collectibles:
            collectible.draw(screen)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dimensional Shift Puzzle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.levels = self.create_levels()
        self.current_level = 0
        self.player = Player(*self.levels[self.current_level].start_pos)
        self.game_state = "playing"  # "playing", "level_complete", "game_over", "game_complete"
        self.message_timer = 0
        
        # Set ethereal objects for player
        for wall in self.levels[self.current_level].walls:
            if wall.is_ethereal:
                self.player.ethereal_objects.append(wall)
    
    def create_levels(self):
        levels = []
        
        # Level 1: Introduction to basic movement and normal dimension
        level1_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  #               #",
            "#                  #",
            "#         C        #",
            "#        ###       #",
            "#                  #",
            "#                  #",
            "#              E   #",
            "#             #### #",
            "#                  #",
            "#                  #",
            "########PPP#########",
        ]
        
        # Level 2: Introduction to inverse gravity
        level2_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  #               #",
            "#         I        #",
            "#        ###       #",
            "#                  #",
            "#                  #",
            "#                  #",
            "#              N   #",
            "#             #### #",
            "#                  #",
            "#         E        #",
            "####################",
        ]
        
        # Level 3: Introduction to ethereal dimension
        level3_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  #               #",
            "#                  #",
            "#         E        #",
            "#        ###       #",
            "#                  #",
            "#        X         #",
            "#        X    N    #",
            "#        X   ##### #",
            "#        X         #",
            "#        X         #",
            "####################",
        ]
        
        # Level 4: Introduction to time dimension
        level4_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  #               #",
            "#                  #",
            "#         T        #",
            "#        ###       #",
            "#                  #",
            "#                  #",
            "#              N   #",
            "#             #### #",
            "#                  #",
            "#                  #",
            "####################",
        ]
        
        # Level 5: Combining all dimensions
        level5_layout = [
            "####################",
            "#        C         #",
            "#        #         #",
            "#  S     #         #",
            "#  #     #         #",
            "#        #    I    #",
            "#        #   ##### #",
            "#        #         #",
            "#        #         #",
            "#        X         #",
            "#        X    E    #",
            "#        X   ##### #",
            "#        X         #",
            "#        X    T    #",
            "####################",
        ]
        
        # Convert layouts to actual levels
        for i, layout in enumerate([level1_layout, level2_layout, level3_layout, level4_layout, level5_layout]):
            # Find start position
            start_pos = (0, 0)
            for y, row in enumerate(layout):
                for x, cell in enumerate(row):
                    if cell == 'S':
                        start_pos = (x * TILE_SIZE, y * TILE_SIZE)
            
            # Set end position (for now, just the opposite corner)
            end_pos = (SCREEN_WIDTH - 2 * TILE_SIZE, TILE_SIZE)
            
            # Replace 'S' with empty space in the layout
            layout = [row.replace('S', ' ') for row in layout]
            
            levels.append(Level(layout, start_pos, end_pos))
        
        return levels
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_state == "level_complete":
                    if event.key == pygame.K_SPACE:
                        self.next_level()
                elif self.game_state == "game_complete" or self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.__init__()  # Reset game
        
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            
            # Handle movement
            if keys[pygame.K_LEFT]:
                self.player.vel_x = -5
            elif keys[pygame.K_RIGHT]:
                self.player.vel_x = 5
            else:
                self.player.vel_x = 0
            
            # Handle jumping
            if keys[pygame.K_SPACE] and self.player.can_jump:
                if self.player.dimension == Dimension.NORMAL:
                    self.player.vel_y = -10
                elif self.player.dimension == Dimension.INVERSE:
                    self.player.vel_y = 10
                elif self.player.dimension == Dimension.ETHEREAL:
                    self.player.vel_y = -10
                elif self.player.dimension == Dimension.TIME:
                    self.player.vel_y = -7  # Slower jump in time dimension
        
        return True
    
    def update(self):
        if self.game_state == "playing":
            current_level = self.levels[self.current_level]
            
            # Update player
            self.player.update(current_level.walls, current_level.platforms, 
                              current_level.dimension_portals, current_level.collectibles)
            
            # Check if player reached the end
            if pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height).colliderect(current_level.end_rect):
                if len(current_level.collectibles) == 0:  # All collectibles must be collected
                    self.game_state = "level_complete"
                    self.message_timer = 180  # Show message for 3 seconds
            
            # Check if player fell off the level
            if self.player.y > SCREEN_HEIGHT + 100 or self.player.y < -100:
                self.game_state = "game_over"
                self.message_timer = 180
        
        # Update timers
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw current level
        self.levels[self.current_level].draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Draw current dimension
        dimension_text = f"Dimension: {self.player.dimension.name}"
        dimension_surface = self.font.render(dimension_text, True, WHITE)
        self.screen.blit(dimension_surface, (10, 10))
        
        # Draw collectibles count
        collectibles_text = f"Collectibles: {len(self.levels[self.current_level].collectibles)} remaining"
        collectibles_surface = self.font.render(collectibles_text, True, WHITE)
        self.screen.blit(collectibles_surface, (10, 50))
        
        # Draw level number
        level_text = f"Level: {self.current_level + 1}/{len(self.levels)}"
        level_surface = self.font.render(level_text, True, WHITE)
        self.screen.blit(level_surface, (SCREEN_WIDTH - level_surface.get_width() - 10, 10))
        
        # Draw messages based on game state
        if self.game_state == "level_complete" and self.message_timer > 0:
            if self.current_level < len(self.levels) - 1:
                message = "Level Complete! Press SPACE to continue"
            else:
                message = "Congratulations! You completed all levels!"
                self.game_state = "game_complete"
            
            message_surface = self.font.render(message, True, WHITE)
            self.screen.blit(message_surface, 
                           (SCREEN_WIDTH//2 - message_surface.get_width()//2, 
                            SCREEN_HEIGHT//2 - message_surface.get_height()//2))
        
        elif self.game_state == "game_over" and self.message_timer > 0:
            message = "Game Over! Press SPACE to restart"
            message_surface = self.font.render(message, True, WHITE)
            self.screen.blit(message_surface, 
                           (SCREEN_WIDTH//2 - message_surface.get_width()//2, 
                            SCREEN_HEIGHT//2 - message_surface.get_height()//2))
        
        elif self.game_state == "game_complete":
            message = "Congratulations! You completed all levels! Press SPACE to play again"
            message_surface = self.font.render(message, True, WHITE)
            self.screen.blit(message_surface, 
                           (SCREEN_WIDTH//2 - message_surface.get_width()//2, 
                            SCREEN_HEIGHT//2 - message_surface.get_height()//2))
    
    def next_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            self.player = Player(*self.levels[self.current_level].start_pos)
            
            # Set ethereal objects for player
            self.player.ethereal_objects = []
            for wall in self.levels[self.current_level].walls:
                if wall.is_ethereal:
                    self.player.ethereal_objects.append(wall)
            
            self.game_state = "playing"
        else:
            self.game_state = "game_complete"
    
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
