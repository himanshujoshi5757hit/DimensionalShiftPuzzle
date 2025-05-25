import pygame
import os
from game_engine import TILE_SIZE, Dimension, load_image
from game_objects import (
    Wall, Platform, DimensionPortal, Collectible, 
    Hazard, Powerup, MovingPlatform, MetalWall
)

class Level:
    def __init__(self, layout, start_pos, end_pos, level_index=1, background_path=None, music_path=None):
        self.walls = []
        self.platforms = []
        self.moving_platforms = []
        self.dimension_portals = []
        self.collectibles = []
        self.hazards = []
        self.powerups = []
        self.metal_walls = []
        self.ethereal_walls = []
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.end_rect = pygame.Rect(end_pos[0], end_pos[1], TILE_SIZE, TILE_SIZE)
        self.width = len(layout[0]) * TILE_SIZE
        self.height = len(layout) * TILE_SIZE
        self.background_path = background_path
        self.music_path = music_path

        # Auto-load level-specific end portal image if it exists, else fallback
        img_folder = "assets/images"
        portal_png = f"end_portal_{level_index+1}.png"
        portal_jpg = f"end_portal_{level_index+1}.jpg"
        default_png = "end_portal.png"
        default_jpg = "end_portal.jpg"
        portal_path_png = os.path.join(img_folder, portal_png)
        portal_path_jpg = os.path.join(img_folder, portal_jpg)
        default_path_png = os.path.join(img_folder, default_png)
        default_path_jpg = os.path.join(img_folder, default_jpg)

        portal_img_name = None
        if os.path.exists(portal_path_png):
            portal_img_name = portal_png
        elif os.path.exists(portal_path_jpg):
            portal_img_name = portal_jpg
        elif os.path.exists(default_path_png):
            portal_img_name = default_png
        elif os.path.exists(default_path_jpg):
            portal_img_name = default_jpg

        if portal_img_name:
            try:
                self.end_portal_image = load_image(portal_img_name)
                self.end_portal_image = pygame.transform.scale(self.end_portal_image, (TILE_SIZE, TILE_SIZE))
            except Exception:
                self.end_portal_image = None
        else:
            self.end_portal_image = None

        # Parse level layout
        self.parse_layout(layout)
    
    def parse_layout(self, layout):
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                pos_x = x * TILE_SIZE
                pos_y = y * TILE_SIZE
                
                if cell == '#':  # Wall
                    self.walls.append(Wall(pos_x, pos_y, TILE_SIZE, TILE_SIZE))
                elif cell == 'P':  # Platform
                    self.platforms.append(Platform(pos_x, pos_y, TILE_SIZE))
                elif cell == 'M':  # Moving platform
                    self.moving_platforms.append(MovingPlatform(pos_x, pos_y, TILE_SIZE * 3, 10, 0, 100, 1))
                elif cell == 'H':  # Health powerup
                    self.powerups.append(Powerup(pos_x, pos_y, "health"))
                elif cell == 'N':  # Normal dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.NORMAL))
                elif cell == 'I':  # Inverse dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.INVERSE))
                elif cell == 'E':  # Ethereal dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.ETHEREAL))
                elif cell == 'T':  # Time dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.TIME))
                elif cell == 'G':  # Magnetic dimension portal
                    self.dimension_portals.append(DimensionPortal(pos_x, pos_y, Dimension.MAGNETIC))
                elif cell == 'C':  # Collectible
                    self.collectibles.append(Collectible(pos_x, pos_y))
                elif cell == 'X':  # Ethereal wall
                    wall = Wall(pos_x, pos_y, TILE_SIZE, TILE_SIZE, (200, 200, 200))
                    wall.is_ethereal = True
                    self.walls.append(wall)
                    self.ethereal_walls.append(wall)
                elif cell == 'D':  # Hazard/Danger
                    self.hazards.append(Hazard(pos_x, pos_y, TILE_SIZE, TILE_SIZE))
                elif cell == 'W':  # Metal wall for magnetic dimension
                    wall = MetalWall(pos_x, pos_y, TILE_SIZE, TILE_SIZE)
                    self.walls.append(wall)
                    self.metal_walls.append(wall)
                elif cell == 'S':  # Speed powerup
                    self.powerups.append(Powerup(pos_x, pos_y, "speed"))
                elif cell == 'J':  # Jump powerup
                    self.powerups.append(Powerup(pos_x, pos_y, "jump"))
                elif cell == 'V':  # Invincibility powerup
                    self.powerups.append(Powerup(pos_x, pos_y, "invincibility"))
                # Add more cell types as needed
    
    def update(self):
        for platform in self.moving_platforms:
            platform.update()
        for collectible in self.collectibles:
            collectible.update()
        for hazard in self.hazards:
            hazard.update()
        for powerup in self.powerups:
            powerup.update()
        for portal in self.dimension_portals:
            portal.update()
    
    def draw(self, screen, camera=None):
        # Draw end point (exit portal)
        if camera:
            end_rect = camera.apply(self.end_rect)
        else:
            end_rect = self.end_rect
        if self.end_portal_image:
            screen.blit(self.end_portal_image, end_rect)
        else:
            pygame.draw.rect(screen, (0, 255, 0), end_rect)
        
        # Draw level elements
        for wall in self.walls:
            wall.draw(screen, camera)
        for platform in self.platforms:
            platform.draw(screen, camera)
        for platform in self.moving_platforms:
            platform.draw(screen, camera)
        for portal in self.dimension_portals:
            portal.draw(screen, camera)
        for collectible in self.collectibles:
            collectible.draw(screen, camera)
        for hazard in self.hazards:
            hazard.draw(screen, camera)
        for powerup in self.powerups:
            powerup.draw(screen, camera)

class LevelManager:
    def __init__(self):
        self.levels = self.create_levels()
        self.current_level = 0
    
    def create_levels(self):
        levels = []
        
        # Level 1: Introduction to basic movement and normal dimension
        level1_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S  D            #",
            "#  ####            #",
            "#                  #",
            "#         C  D      #",
            "#         ###      #",
            "#                  #",
            "#                  #",
            "#                  #",
            "#              D E  #",
            "#             ##### #",
            "#     D            #",
            "########PPP#########",
        ]
        
        # Level 2: Introduction to inverse gravity
        level2_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ###             #",
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
            "#  ###             #",
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
            "#  ###             #",
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
        
        # Level 5: Introduction to magnetic dimension
        level5_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ###             #",
            "#                  #",
            "#         G        #",
            "#        ###       #",
            "#                  #",
            "#                  #",
            "#        W    N    #",
            "#        W   ##### #",
            "#                  #",
            "#                  #",
            "####################",
        ]
        
        # Level 6: Combining dimensions with hazards
        level6_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ###             #",
            "#                  #",
            "#         E        #",
            "#        ###       #",
            "#                  #",
            "#        X         #",
            "#        X    I    #",
            "#        X   ##### #",
            "#        XDDDDDDDDD#",
            "#                  #",
            "####################",
        ]
        
        # Level 7: Moving platforms and collectibles
        level7_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ####            #",
            "#         C        #",
            "#                  #",
            "#        M         #",
            "#                  #",
            "#                C #",
            "#              N   #",
            "#             #### #",
            "#                  #",
            "#         H        #",
            "####################",
        ]
        
        # Level 8: Complex ethereal maze
        level8_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ##              #",
            "#         E        #",
            "#        ###       #",
            "#        X#X       #",
            "#        X#X       #",
            "#        X#X       #",
            "#        X#X  N    #",
            "#        X#X ##### #",
            "#        X         #",
            "#        X         #",
            "####################",
        ]
        
        # Level 9: Time-based precision jumping
        level9_layout = [
            "####################",
            "#                  #",
            "#                  #",
            "#  S               #",
            "#  ###             #",
            "#                  #",
            "#         T        #",
            "#        ###       #",
            "#                  #",
            "#   P   P   P      #",
            "#                  #",
            "#                  #",
            "#DDDDDDDDDDDDDDDDD #",
            "#                  #",
            "####################",
        ]
        
        # Level 10: Master level combining all dimensions
        level10_layout = [
            "####################",
            "#        C         #",
            "#        #         #",
            "#  S     #         #",
            "#  ###   #         #",
            "#        #    I    #",
            "#        #   ##### #",
            "#        #         #",
            "#        #         #",
            "#        X    W    #",
            "#        X    E    #",
            "#        X   ##### #",
            "#        X         #",
            "#        X    T    #",
            "####################",
        ]
        
        # Convert layouts to actual levels
        layouts = [level1_layout, level2_layout, level3_layout, level4_layout, level5_layout,
                  level6_layout, level7_layout, level8_layout, level9_layout, level10_layout]
        
        for i, layout in enumerate(layouts):
            # Find start and end positions
            start_pos = (0, 0)
            end_pos = (0, 0)
            for y, row in enumerate(layout):
                for x, cell in enumerate(row):
                    if cell == 'S':
                        start_pos = (x * TILE_SIZE, y * TILE_SIZE)
                    if cell == 'E':
                        end_pos = (x * TILE_SIZE, y * TILE_SIZE)

            # Replace 'S' and 'E' with empty space in the layout
            layout = [row.replace('S', ' ').replace('E', ' ') for row in layout]
            
            # --- Background selection logic ---
            bg_folder = "assets/images"
            bg_png = f"background_{i+1}.png"
            bg_jpg = f"background_{i+1}.jpg"
            bg_path_png = os.path.join(bg_folder, bg_png)
            bg_path_jpg = os.path.join(bg_folder, bg_jpg)
            if os.path.exists(bg_path_png):
                background_path = bg_path_png
            elif os.path.exists(bg_path_jpg):
                background_path = bg_path_jpg
            else:
                background_path = None

            music_path = f"assets/sounds/level_{i+1}.mp3"
            
            levels.append(Level(layout, start_pos, end_pos, i, background_path, music_path))
        
        return levels
    
    def get_current_level(self):
        return self.levels[self.current_level]
    
    def next_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            return True
        return False
    
    def reset_level(self):
        # Recreate the current level to reset it
        self.levels[self.current_level] = self.create_levels()[self.current_level]
