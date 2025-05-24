import os
import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create directories if they don't exist
os.makedirs("assets/images", exist_ok=True)

# Background styles to create
bg_styles = ["default", "forest", "desert", "snow", "night"]

# Function to create a background for a specific style and level
def create_background(style, level_num):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Base color and elements depend on style
    if style == "default":
        # Blue gradient
        base_color = (0, 0, 50)
        for y in range(SCREEN_HEIGHT):
            intensity = y / SCREEN_HEIGHT
            color = [int(c * (1 + intensity * 0.5)) for c in base_color]
            color = [min(255, c) for c in color]
            pygame.draw.line(surf, color, (0, y), (SCREEN_WIDTH, y))
        
        # Add stars
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
    
    elif style == "forest":
        # Green gradient
        for y in range(SCREEN_HEIGHT):
            green = min(255, int(50 + (y / SCREEN_HEIGHT) * 100))
            pygame.draw.line(surf, (0, green, 0), (0, y), (SCREEN_WIDTH, y))
        
        # Add trees
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            height = random.randint(100, 200)
            width = random.randint(20, 40)
            # Tree trunk
            pygame.draw.rect(surf, (100, 50, 0), (x, SCREEN_HEIGHT - height, width, height))
            # Tree top
            pygame.draw.circle(surf, (0, 150, 0), (x + width//2, SCREEN_HEIGHT - height - 50), 60)
    
    elif style == "desert":
        # Sandy gradient
        for y in range(SCREEN_HEIGHT):
            intensity = y / SCREEN_HEIGHT
            r = min(255, int(200 + intensity * 55))
            g = min(255, int(150 + intensity * 50))
            b = min(255, int(50 + intensity * 50))
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add cacti
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            height = random.randint(50, 150)
            width = random.randint(10, 30)
            pygame.draw.rect(surf, (0, 100, 0), (x, SCREEN_HEIGHT - height, width, height))
            # Cactus arms
            arm_height = height // 3
            pygame.draw.rect(surf, (0, 100, 0), (x - width//2, SCREEN_HEIGHT - height + arm_height, width//2, width))
            pygame.draw.rect(surf, (0, 100, 0), (x + width, SCREEN_HEIGHT - height + arm_height * 2, width//2, width))
    
    elif style == "snow":
        # Snowy gradient
        for y in range(SCREEN_HEIGHT):
            intensity = 1 - (y / SCREEN_HEIGHT)
            color = min(255, int(200 + intensity * 55))
            pygame.draw.line(surf, (color, color, 255), (0, y), (SCREEN_WIDTH, y))
        
        # Add snowflakes
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 4)
            pygame.draw.circle(surf, (255, 255, 255), (x, y), size)
    
    elif style == "night":
        # Dark gradient
        for y in range(SCREEN_HEIGHT):
            intensity = y / SCREEN_HEIGHT
            color = min(50, int(10 + intensity * 40))
            pygame.draw.line(surf, (color, color, color + 20), (0, y), (SCREEN_WIDTH, y))
        
        # Add stars and moon
        for _ in range(300):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT * 2 // 3)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
        
        # Moon
        pygame.draw.circle(surf, (200, 200, 180), (SCREEN_WIDTH - 100, 100), 50)
        pygame.draw.circle(surf, (50, 50, 70), (SCREEN_WIDTH - 120, 80), 40)
    
    # Add level-specific elements
    level_text = f"Level {level_num + 1}"
    font = pygame.font.SysFont(None, 24)
    text_surf = font.render(level_text, True, (255, 255, 255))
    surf.blit(text_surf, (20, 20))
    
    return surf

# Function to create a parallax layer for a specific style
def create_parallax_layer(style, layer_num):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    if style == "default":
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
    
    elif style == "forest":
        if layer_num == 1:  # Far background
            # Distant forest
            for i in range(15):
                width = random.randint(100, 200)
                height = random.randint(100, 200)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (0, 50, 0)
                pygame.draw.circle(surf, color, (x + width//2, SCREEN_HEIGHT - height//2), width//2)
        
        elif layer_num == 2:  # Middle layer
            # Closer trees
            for i in range(10):
                x = random.randint(0, SCREEN_WIDTH)
                height = random.randint(100, 200)
                width = random.randint(20, 40)
                # Tree trunk
                pygame.draw.rect(surf, (80, 40, 0), (x, SCREEN_HEIGHT - height, width, height))
                # Tree top
                pygame.draw.circle(surf, (0, 100, 0), (x + width//2, SCREEN_HEIGHT - height - 50), 70)
        
        elif layer_num == 3:  # Front layer
            # Foreground bushes
            for i in range(20):
                x = random.randint(0, SCREEN_WIDTH)
                size = random.randint(30, 60)
                pygame.draw.circle(surf, (0, 120, 0), (x, SCREEN_HEIGHT - size//2), size)
    
    elif style == "desert":
        if layer_num == 1:  # Far background
            # Distant mountains
            for i in range(5):
                width = random.randint(200, 400)
                height = random.randint(100, 200)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (150, 100, 50)
                pygame.draw.polygon(surf, color, [
                    (x, SCREEN_HEIGHT),
                    (x + width//2, SCREEN_HEIGHT - height),
                    (x + width, SCREEN_HEIGHT)
                ])
        
        elif layer_num == 2:  # Middle layer
            # Sand dunes
            for i in range(8):
                width = random.randint(100, 300)
                height = random.randint(50, 100)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (200, 180, 100)
                pygame.draw.circle(surf, color, (x + width//2, SCREEN_HEIGHT + height//2), height)
        
        elif layer_num == 3:  # Front layer
            # Cacti and rocks
            for i in range(8):
                x = random.randint(0, SCREEN_WIDTH)
                height = random.randint(40, 100)
                width = random.randint(10, 20)
                pygame.draw.rect(surf, (0, 100, 0), (x, SCREEN_HEIGHT - height, width, height))
                # Cactus arms
                pygame.draw.rect(surf, (0, 100, 0), (x - width//2, SCREEN_HEIGHT - height + height//3, width//2, width))
    
    elif style == "snow":
        if layer_num == 1:  # Far background
            # Distant mountains
            for i in range(5):
                width = random.randint(200, 400)
                height = random.randint(150, 250)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (200, 200, 220)
                pygame.draw.polygon(surf, color, [
                    (x, SCREEN_HEIGHT),
                    (x + width//2, SCREEN_HEIGHT - height),
                    (x + width, SCREEN_HEIGHT)
                ])
        
        elif layer_num == 2:  # Middle layer
            # Snow hills
            for i in range(8):
                width = random.randint(100, 300)
                height = random.randint(50, 100)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (220, 220, 240)
                pygame.draw.circle(surf, color, (x + width//2, SCREEN_HEIGHT + height//2), height)
        
        elif layer_num == 3:  # Front layer
            # Snow-covered trees
            for i in range(10):
                x = random.randint(0, SCREEN_WIDTH)
                height = random.randint(50, 150)
                width = random.randint(10, 30)
                # Tree trunk
                pygame.draw.rect(surf, (100, 80, 60), (x, SCREEN_HEIGHT - height, width, height))
                # Snow-covered top
                pygame.draw.circle(surf, (230, 230, 250), (x + width//2, SCREEN_HEIGHT - height - 30), 40)
    
    elif style == "night":
        if layer_num == 1:  # Far background
            # Distant city silhouette
            for i in range(20):
                width = random.randint(30, 100)
                height = random.randint(50, 200)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (20, 20, 30)
                pygame.draw.rect(surf, color, (x, SCREEN_HEIGHT - height, width, height))
                # Windows
                for _ in range(random.randint(2, 8)):
                    wx = x + random.randint(5, width-10)
                    wy = SCREEN_HEIGHT - height + random.randint(10, height-10)
                    wsize = random.randint(3, 8)
                    pygame.draw.rect(surf, (255, 255, 150), (wx, wy, wsize, wsize))
        
        elif layer_num == 2:  # Middle layer
            # Hills and trees
            for i in range(8):
                width = random.randint(100, 300)
                height = random.randint(50, 100)
                x = random.randint(0, SCREEN_WIDTH - width)
                color = (10, 10, 30)
                pygame.draw.circle(surf, color, (x + width//2, SCREEN_HEIGHT + height//2), height)
        
        elif layer_num == 3:  # Front layer
            # Foreground trees
            for i in range(10):
                x = random.randint(0, SCREEN_WIDTH)
                height = random.randint(100, 200)
                width = random.randint(10, 30)
                # Tree silhouette
                pygame.draw.rect(surf, (5, 5, 15), (x, SCREEN_HEIGHT - height, width, height))
                pygame.draw.circle(surf, (5, 5, 15), (x + width//2, SCREEN_HEIGHT - height - 40), 50)
    
    return surf

# Create level backgrounds for each style
print("Creating level backgrounds...")
for style in bg_styles:
    for level in range(10):
        bg = create_background(style, level)
        if style == "default":
            filename = f"assets/images/background_{level+1}.png"
        else:
            filename = f"assets/images/background_{style}_{level+1}.png"
        pygame.image.save(bg, filename)
        print(f"Created {filename}")

# Create parallax backgrounds for each style
print("\nCreating parallax backgrounds...")
for style in bg_styles:
    for layer in range(1, 4):
        bg_layer = create_parallax_layer(style, layer)
        if style == "default":
            filename = f"assets/images/bg_layer{layer}.png"
        else:
            filename = f"assets/images/bg_{style}_layer{layer}.png"
        pygame.image.save(bg_layer, filename)
        print(f"Created {filename}")

print("\nAll background styles have been created!")
print("You can now select these backgrounds in the game.")
