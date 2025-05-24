import os
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create directories if they don't exist
os.makedirs("assets/images/player", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# Function to create a simple player sprite
def create_player_sprite(state, dimension, frame_num, color):
    surf = pygame.Surface((TILE_SIZE-4, TILE_SIZE-4), pygame.SRCALPHA)
    
    # Base rectangle
    pygame.draw.rect(surf, color, (0, 0, TILE_SIZE-4, TILE_SIZE-4))
    
    # Add details based on state
    if state == "idle":
        # Blinking effect
        if frame_num == 2:
            pygame.draw.rect(surf, (255, 255, 255), ((TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 2, 2))
            pygame.draw.rect(surf, (255, 255, 255), (3*(TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 2, 2))
    elif state == "run":
        # Running legs
        leg_height = (TILE_SIZE-4) // 3
        leg_offset = (frame_num % 2) * 4 - 2
        pygame.draw.rect(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-leg_height+leg_offset, 4, leg_height))
        pygame.draw.rect(surf, (0, 0, 0), (3*(TILE_SIZE-4)//4, (TILE_SIZE-4)-leg_height-leg_offset, 4, leg_height))
    elif state == "jump":
        # Jumping pose
        pygame.draw.ellipse(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-10, (TILE_SIZE-4)//2, 8))
    elif state == "fall":
        # Falling pose
        pygame.draw.ellipse(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-6, (TILE_SIZE-4)//2, 4))
    
    return surf

# Function to create a Mario-style sprite sheet
def create_mario_sprite_sheet():
    dimensions = ["normal", "inverse", "ethereal", "time", "magnetic"]
    states = ["idle", "run", "jump", "fall"]
    
    # Colors for each dimension
    colors = {
        "normal": (0, 0, 255),      # Blue
        "inverse": (255, 0, 0),     # Red
        "ethereal": (128, 0, 128),  # Purple
        "time": (255, 255, 0),      # Yellow
        "magnetic": (0, 255, 255)   # Cyan
    }
    
    # Create a sprite sheet with 4 frames for each state and dimension
    sheet_width = 4 * TILE_SIZE
    sheet_height = len(states) * len(dimensions) * TILE_SIZE
    
    sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    
    for state_idx, state in enumerate(states):
        for dim_idx, dimension in enumerate(dimensions):
            for frame in range(4):
                sprite = create_player_sprite(state, dimension, frame, colors[dimension])
                
                # Position in sprite sheet
                x = frame * TILE_SIZE
                y = (state_idx * len(dimensions) + dim_idx) * TILE_SIZE
                
                # Draw to sprite sheet
                sheet.blit(sprite, (x + 2, y + 2))  # +2 for centering in tile
    
    return sheet

# Function to create a simple background
def create_background(level_num):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create a gradient background based on level number
    base_color = [(0, 0, 50), (0, 50, 0), (50, 0, 0), (0, 50, 50), 
                 (50, 0, 50), (50, 50, 0), (30, 30, 30), (0, 0, 80),
                 (0, 80, 0), (80, 0, 0)][level_num % 10]
    
    for y in range(SCREEN_HEIGHT):
        intensity = y / SCREEN_HEIGHT
        color = [int(c * (1 + intensity * 0.5)) for c in base_color]
        color = [min(255, c) for c in color]
        pygame.draw.line(surf, color, (0, y), (SCREEN_WIDTH, y))
    
    # Add some stars or decorations
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
    
    return surf

# Function to create a parallax background layer
def create_parallax_layer(layer_num):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Different style for each layer
    if layer_num == 1:  # Far background
        # Draw distant mountains
        for i in range(5):
            width = random.randint(100, 300)
            height = random.randint(50, 150)
            x = random.randint(0, SCREEN_WIDTH - width)
            color = (20, 20, 40)
            pygame.draw.polygon(surf, color, [
                (x, SCREEN_HEIGHT),
                (x + width//2, SCREEN_HEIGHT - height),
                (x + width, SCREEN_HEIGHT)
            ])
    
    elif layer_num == 2:  # Middle layer
        # Draw hills
        for i in range(8):
            width = random.randint(80, 200)
            height = random.randint(40, 100)
            x = random.randint(0, SCREEN_WIDTH - width)
            color = (30, 50, 30)
            pygame.draw.circle(surf, color, (x + width//2, SCREEN_HEIGHT + height//2), height)
    
    elif layer_num == 3:  # Front layer
        # Draw trees or foreground elements
        for i in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            height = random.randint(50, 150)
            width = random.randint(10, 30)
            # Tree trunk
            pygame.draw.rect(surf, (60, 30, 10), (x, SCREEN_HEIGHT - height, width, height))
            # Tree top
            pygame.draw.circle(surf, (0, 80, 0), (x + width//2, SCREEN_HEIGHT - height - 30), 40)
    
    return surf

# Function to create a simple game object sprite
def create_game_object(obj_type):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    if obj_type == "wall":
        # Create a brick wall pattern
        pygame.draw.rect(surf, (150, 75, 0), (0, 0, TILE_SIZE, TILE_SIZE))
        for i in range(0, TILE_SIZE, 10):
            for j in range(0, TILE_SIZE, 5):
                offset = 5 if (j // 5) % 2 == 0 else 0
                pygame.draw.rect(surf, (200, 100, 50), (i + offset, j, 8, 4))
        pygame.draw.rect(surf, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 1)
    
    elif obj_type == "platform":
        # Create a platform
        pygame.draw.rect(surf, (0, 150, 0), (0, 0, TILE_SIZE, TILE_SIZE//4))
        pygame.draw.line(surf, (0, 100, 0), (0, 0), (TILE_SIZE, 0), 2)
        pygame.draw.line(surf, (0, 200, 0), (0, TILE_SIZE//4), (TILE_SIZE, TILE_SIZE//4), 2)
    
    elif obj_type == "metal_wall":
        # Create a metal wall
        pygame.draw.rect(surf, (192, 192, 192), (0, 0, TILE_SIZE, TILE_SIZE))
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.line(surf, (160, 160, 160), (i, 0), (i, TILE_SIZE), 1)
        for j in range(0, TILE_SIZE, 8):
            pygame.draw.line(surf, (160, 160, 160), (0, j), (TILE_SIZE, j), 1)
        pygame.draw.rect(surf, (128, 128, 128), (0, 0, TILE_SIZE, TILE_SIZE), 1)
    
    elif obj_type == "collectible":
        # Create a coin/collectible
        pygame.draw.circle(surf, (255, 215, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
        pygame.draw.circle(surf, (255, 255, 200), (TILE_SIZE//2 - 2, TILE_SIZE//2 - 2), TILE_SIZE//8)
    
    elif obj_type == "hazard":
        # Create a hazard/spike
        pygame.draw.polygon(surf, (255, 50, 50), [
            (TILE_SIZE//2, 0),
            (0, TILE_SIZE),
            (TILE_SIZE, TILE_SIZE)
        ])
        pygame.draw.polygon(surf, (200, 0, 0), [
            (TILE_SIZE//2, TILE_SIZE//4),
            (TILE_SIZE//4, TILE_SIZE),
            (3*TILE_SIZE//4, TILE_SIZE)
        ])
    
    elif obj_type.startswith("portal_"):
        # Extract dimension from portal type
        dimension = obj_type.split("_")[1]
        
        # Set color based on dimension
        if dimension == "normal":
            color = (0, 0, 255)  # Blue
        elif dimension == "inverse":
            color = (255, 0, 0)  # Red
        elif dimension == "ethereal":
            color = (128, 0, 128)  # Purple
        elif dimension == "time":
            color = (255, 255, 0)  # Yellow
        elif dimension == "magnetic":
            color = (0, 255, 255)  # Cyan
        else:
            color = (255, 255, 255)  # White default
        
        # Draw portal
        pygame.draw.circle(surf, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 2)
        pygame.draw.circle(surf, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
        pygame.draw.circle(surf, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//8)
    
    elif obj_type.startswith("powerup_"):
        # Extract powerup type
        powerup_type = obj_type.split("_")[1]
        
        # Set color based on powerup type
        if powerup_type == "health":
            color = (0, 255, 0)  # Green
            symbol = "+"
        elif powerup_type == "speed":
            color = (0, 255, 255)  # Cyan
            symbol = ">"
        elif powerup_type == "jump":
            color = (255, 255, 0)  # Yellow
            symbol = "^"
        elif powerup_type == "invincibility":
            color = (255, 255, 255)  # White
            symbol = "*"
        else:
            color = (200, 200, 200)  # Gray default
            symbol = "?"
        
        # Draw powerup
        pygame.draw.circle(surf, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 4)
        pygame.draw.circle(surf, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 8)
        
        # Draw symbol
        font = pygame.font.SysFont(None, 24)
        text = font.render(symbol, True, color)
        text_rect = text.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
        surf.blit(text, text_rect)
    
    return surf

# Create player animation frames
print("Creating player animation frames...")
dimensions = ["normal", "inverse", "ethereal", "time", "magnetic"]
states = ["idle", "run", "jump", "fall"]
colors = {
    "normal": (0, 0, 255),      # Blue
    "inverse": (255, 0, 0),     # Red
    "ethereal": (128, 0, 128),  # Purple
    "time": (255, 255, 0),      # Yellow
    "magnetic": (0, 255, 255)   # Cyan
}

for dimension in dimensions:
    for state in states:
        for frame in range(1, 5):
            sprite = create_player_sprite(state, dimension, frame, colors[dimension])
            filename = f"assets/images/player/{state}_{dimension}_{frame}.png"
            pygame.image.save(sprite, filename)
            print(f"Created {filename}")

# Create Mario sprite sheet
print("Creating Mario sprite sheet...")
mario_sheet = create_mario_sprite_sheet()
pygame.image.save(mario_sheet, "assets/images/mario.png")
print("Created assets/images/mario.png")

# Create background images
print("Creating background images...")
for level in range(1, 11):
    bg = create_background(level - 1)
    pygame.image.save(bg, f"assets/images/background_{level}.png")
    print(f"Created assets/images/background_{level}.png")

# Create parallax background layers
print("Creating parallax background layers...")
for layer in range(1, 4):
    bg_layer = create_parallax_layer(layer)
    pygame.image.save(bg_layer, f"assets/images/bg_layer{layer}.png")
    print(f"Created assets/images/bg_layer{layer}.png")

# Create game object sprites
print("Creating game object sprites...")
game_objects = [
    "wall", "platform", "metal_wall", "collectible", "hazard",
    "portal_normal", "portal_inverse", "portal_ethereal", "portal_time", "portal_magnetic",
    "powerup_health", "powerup_speed", "powerup_jump", "powerup_invincibility"
]

for obj in game_objects:
    sprite = create_game_object(obj)
    pygame.image.save(sprite, f"assets/images/{obj}.png")
    print(f"Created assets/images/{obj}.png")

print("\nAll placeholder assets have been created!")
print("You can now run the game with these basic assets.")
print("Replace them with your own custom assets for a better look.")
