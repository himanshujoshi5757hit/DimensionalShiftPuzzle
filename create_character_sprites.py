import os
import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create directories if they don't exist
os.makedirs("assets/images", exist_ok=True)

# Character types to create
character_types = ["default", "mario", "ninja", "robot"]

# Function to create a character sprite sheet
def create_character_sprite_sheet(character_type):
    dimensions = ["normal", "inverse", "ethereal", "time", "magnetic"]
    states = ["idle", "run", "jump", "fall"]
    
    # Colors for each dimension
    dimension_colors = {
        "normal": (0, 0, 255),      # Blue
        "inverse": (255, 0, 0),     # Red
        "ethereal": (128, 0, 128),  # Purple
        "time": (255, 255, 0),      # Yellow
        "magnetic": (0, 255, 255)   # Cyan
    }
    
    # Character-specific colors
    character_colors = {
        "default": (100, 100, 100),
        "mario": (255, 0, 0),
        "ninja": (50, 50, 50),
        "robot": (192, 192, 192)
    }
    
    # Create a sprite sheet with 4 frames for each state and dimension
    sheet_width = 4 * TILE_SIZE
    sheet_height = len(states) * len(dimensions) * TILE_SIZE
    
    sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    
    for state_idx, state in enumerate(states):
        for dim_idx, dimension in enumerate(dimensions):
            for frame in range(4):
                # Create a frame surface
                surf = pygame.Surface((TILE_SIZE-4, TILE_SIZE-4), pygame.SRCALPHA)
                
                # Base color combines character and dimension
                base_color = character_colors.get(character_type, (100, 100, 100))
                dim_color = dimension_colors.get(dimension, (255, 255, 255))
                
                # Mix the colors
                mixed_color = (
                    (base_color[0] + dim_color[0]) // 2,
                    (base_color[1] + dim_color[1]) // 2,
                    (base_color[2] + dim_color[2]) // 2
                )
                
                # Draw the character
                if character_type == "default":
                    # Simple rectangle character
                    pygame.draw.rect(surf, mixed_color, (0, 0, TILE_SIZE-4, TILE_SIZE-4))
                    
                    # Add details based on state
                    if state == "idle":
                        # Eyes
                        if frame == 2:  # Blink on frame 2
                            pygame.draw.rect(surf, (255, 255, 255), ((TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 2, 2))
                            pygame.draw.rect(surf, (255, 255, 255), (3*(TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 2, 2))
                        else:
                            pygame.draw.rect(surf, (255, 255, 255), ((TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 4, 4))
                            pygame.draw.rect(surf, (255, 255, 255), (3*(TILE_SIZE-4)//4, (TILE_SIZE-4)//4, 4, 4))
                    
                    elif state == "run":
                        # Running legs
                        leg_height = (TILE_SIZE-4) // 3
                        leg_offset = (frame % 2) * 4 - 2
                        pygame.draw.rect(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-leg_height+leg_offset, 4, leg_height))
                        pygame.draw.rect(surf, (0, 0, 0), (3*(TILE_SIZE-4)//4, (TILE_SIZE-4)-leg_height-leg_offset, 4, leg_height))
                    
                    elif state == "jump":
                        # Jumping pose
                        pygame.draw.ellipse(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-10, (TILE_SIZE-4)//2, 8))
                    
                    elif state == "fall":
                        # Falling pose
                        pygame.draw.ellipse(surf, (0, 0, 0), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-6, (TILE_SIZE-4)//2, 4))
                
                elif character_type == "mario":
                    # Mario-style character
                    # Body
                    pygame.draw.rect(surf, (255, 0, 0), (0, 0, TILE_SIZE-4, TILE_SIZE-4))
                    
                    # Face
                    pygame.draw.rect(surf, (255, 200, 150), (4, 4, TILE_SIZE-12, TILE_SIZE-12))
                    
                    # Hat
                    pygame.draw.rect(surf, (255, 0, 0), (2, 2, TILE_SIZE-8, 8))
                    
                    # Eyes
                    pygame.draw.rect(surf, (0, 0, 0), (8, 10, 4, 4))
                    
                    # Mustache
                    pygame.draw.rect(surf, (0, 0, 0), (6, 16, 12, 4))
                    
                    if state == "run":
                        # Running legs
                        leg_height = (TILE_SIZE-4) // 3
                        leg_offset = (frame % 2) * 4 - 2
                        pygame.draw.rect(surf, (0, 0, 255), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-leg_height+leg_offset, 8, leg_height))
                    
                    elif state == "jump":
                        # Jumping pose
                        pygame.draw.rect(surf, (0, 0, 255), ((TILE_SIZE-4)//4, (TILE_SIZE-4)-12, 8, 12))
                
                elif character_type == "ninja":
                    # Ninja character
                    # Body
                    pygame.draw.rect(surf, (50, 50, 50), (0, 0, TILE_SIZE-4, TILE_SIZE-4))
                    
                    # Mask
                    pygame.draw.rect(surf, (0, 0, 0), (4, 4, TILE_SIZE-12, 10))
                    
                    # Eyes
                    pygame.draw.rect(surf, (255, 255, 255), (8, 8, 4, 4))
                    pygame.draw.rect(surf, (255, 255, 255), (18, 8, 4, 4))
                    
                    if state == "run":
                        # Running animation
                        if frame % 2 == 0:
                            # Running pose 1
                            pygame.draw.line(surf, (100, 100, 100), (8, 20), (16, 30), 2)
                            pygame.draw.line(surf, (100, 100, 100), (24, 20), (16, 30), 2)
                        else:
                            # Running pose 2
                            pygame.draw.line(surf, (100, 100, 100), (8, 30), (16, 20), 2)
                            pygame.draw.line(surf, (100, 100, 100), (24, 30), (16, 20), 2)
                    
                    elif state == "jump":
                        # Jumping pose
                        pygame.draw.line(surf, (100, 100, 100), (8, 25), (16, 20), 2)
                        pygame.draw.line(surf, (100, 100, 100), (24, 25), (16, 20), 2)
                
                elif character_type == "robot":
                    # Robot character
                    # Body
                    pygame.draw.rect(surf, (192, 192, 192), (0, 0, TILE_SIZE-4, TILE_SIZE-4))
                    
                    # Face plate
                    pygame.draw.rect(surf, (100, 100, 100), (4, 4, TILE_SIZE-12, TILE_SIZE-12))
                    
                    # Eyes
                    if frame % 3 == 0:  # Blinking effect
                        pygame.draw.rect(surf, (255, 0, 0), (8, 8, 4, 2))
                        pygame.draw.rect(surf, (255, 0, 0), (18, 8, 4, 2))
                    else:
                        pygame.draw.rect(surf, (255, 0, 0), (8, 8, 4, 4))
                        pygame.draw.rect(surf, (255, 0, 0), (18, 8, 4, 4))
                    
                    # Mouth
                    pygame.draw.rect(surf, (50, 50, 50), (10, 18, 10, 2))
                    
                    if state == "run":
                        # Robot walking
                        leg_height = (TILE_SIZE-4) // 3
                        if frame % 2 == 0:
                            pygame.draw.rect(surf, (100, 100, 100), (8, (TILE_SIZE-4)-leg_height, 4, leg_height))
                            pygame.draw.rect(surf, (100, 100, 100), (20, (TILE_SIZE-4)-leg_height+4, 4, leg_height-4))
                        else:
                            pygame.draw.rect(surf, (100, 100, 100), (8, (TILE_SIZE-4)-leg_height+4, 4, leg_height-4))
                            pygame.draw.rect(surf, (100, 100, 100), (20, (TILE_SIZE-4)-leg_height, 4, leg_height))
                
                # Position in sprite sheet
                x = frame * TILE_SIZE
                y = (state_idx * len(dimensions) + dim_idx) * TILE_SIZE
                
                # Draw to sprite sheet
                sheet.blit(surf, (x + 2, y + 2))  # +2 for centering in tile
    
    return sheet

# Create character sprite sheets
print("Creating character sprite sheets...")
for character in character_types:
    sprite_sheet = create_character_sprite_sheet(character)
    pygame.image.save(sprite_sheet, f"assets/images/{character}.png")
    print(f"Created assets/images/{character}.png")

print("\nAll character sprite sheets have been created!")
print("You can now select these characters in the game.")
