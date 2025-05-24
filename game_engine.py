import pygame
import sys
import math
import random
from enum import Enum
import os

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
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Dimension types
class Dimension(Enum):
    NORMAL = 0    # Regular physics
    INVERSE = 1   # Inverted gravity
    ETHEREAL = 2  # Pass through certain objects
    TIME = 3      # Time slows down
    MAGNETIC = 4  # Attracts to metal objects

# Game states
class GameState(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    LEVEL_COMPLETE = 2
    GAME_OVER = 3
    GAME_COMPLETE = 4
    TUTORIAL = 5
    PAUSED = 6
    CONTROLS = 7
    SETTINGS = 8
    CREDITS = 9

# Asset loading functions
def load_image(name, scale=1.0, convert_alpha=True):
    try:
        # Use absolute path for more reliable loading
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "assets", "images", name)
        print(f"Loading image: {path}")
        
        image = pygame.image.load(path)
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        print(f"Successfully loaded image: {name}")
        return image
    except pygame.error as e:
        print(f"Failed to load image: {name}, Error: {e}")
        # Create a placeholder image if file not found
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 255), (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.line(surf, BLACK, (0, 0), (TILE_SIZE, TILE_SIZE), 2)
        pygame.draw.line(surf, BLACK, (TILE_SIZE, 0), (0, TILE_SIZE), 2)
        return surf

def load_sound(name):
    try:
        import os
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "assets", "sounds", name)
        print(f"Loading sound: {path}")
        
        sound = pygame.mixer.Sound(path)
        print(f"Successfully loaded sound: {name}")
        return sound
    except pygame.error as e:
        print(f"Failed to load sound: {name}, Error: {e}")
        # Return a dummy sound if file not found
        return DummySound()

class DummySound:
    def play(self):
        pass
    
    def stop(self):
        pass

# Animation class
class Animation:
    def __init__(self, frames, frame_duration=5, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.frame_counter = 0
        self.finished = False
    
    def update(self):
        if self.finished:
            return self.frames[-1]
            
        self.frame_counter += 1
        if self.frame_counter >= self.frame_duration:
            self.frame_counter = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
        
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.frame_counter = 0
        self.finished = False

# Particle system
class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, color, velocity_x, velocity_y, lifetime, size=3, gravity=0.1):
        self.particles.append({
            'x': x,
            'y': y,
            'color': color,
            'velocity_x': velocity_x,
            'velocity_y': velocity_y,
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'size': size,
            'gravity': gravity
        })
    
    def create_explosion(self, x, y, color, count=20, speed=3):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed_val = random.uniform(1, speed)
            velocity_x = math.cos(angle) * speed_val
            velocity_y = math.sin(angle) * speed_val
            lifetime = random.randint(20, 40)
            size = random.randint(2, 5)
            self.add_particle(x, y, color, velocity_x, velocity_y, lifetime, size)
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            particle['velocity_y'] += particle['gravity']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            else:
                color[3] = alpha
            
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), particle['size'])

# Camera class for smooth following
class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.target_x = 0
        self.target_y = 0
        self.smoothness = 0.1  # Lower = smoother
    
    def update(self, target_x, target_y):
        self.target_x = target_x - self.width // 2
        self.target_y = target_y - self.height // 2
        
        # Smooth camera movement
        self.rect.x += (self.target_x - self.rect.x) * self.smoothness
        self.rect.y += (self.target_y - self.rect.y) * self.smoothness
        
        # Clamp camera to level bounds (would need level size)
        # self.rect.x = max(0, min(self.rect.x, level_width - self.width))
        # self.rect.y = max(0, min(self.rect.y, level_height - self.height))
    
    def apply(self, entity_rect):
        return pygame.Rect(entity_rect.x - self.rect.x, entity_rect.y - self.rect.y, entity_rect.width, entity_rect.height)

# Button class for UI
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

# Text effects
class TextEffect:
    def __init__(self, text, x, y, color=WHITE, size=36, duration=60, velocity_y=-1):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.duration = duration
        self.velocity_y = velocity_y
        self.alpha = 255
        self.font = pygame.font.SysFont(None, size)
    
    def update(self):
        self.y += self.velocity_y
        self.duration -= 1
        self.alpha = int(255 * (self.duration / 60))
        return self.duration > 0
    
    def draw(self, screen):
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(self.alpha)
        screen.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y))

# Background parallax effect
class ParallaxBackground:
    def __init__(self, image_paths, scroll_speeds):
        self.layers = []
        for path, speed in zip(image_paths, scroll_speeds):
            try:
                img = pygame.image.load(path).convert_alpha()
                self.layers.append({
                    'image': img,
                    'scroll': 0,
                    'speed': speed
                })
            except pygame.error:
                # Create a placeholder if image not found
                surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                surf.fill((random.randint(0, 50), random.randint(0, 50), random.randint(0, 100)))
                self.layers.append({
                    'image': surf,
                    'scroll': 0,
                    'speed': speed
                })
    
    def update(self, camera_x_change):
        for layer in self.layers:
            layer['scroll'] += camera_x_change * layer['speed']
            # Reset scroll if it goes too far
            layer['scroll'] = layer['scroll'] % SCREEN_WIDTH
    
    def draw(self, screen):
        for layer in self.layers:
            # Draw the layer twice side by side for seamless scrolling
            screen.blit(layer['image'], (-int(layer['scroll']), 0))
            screen.blit(layer['image'], (-int(layer['scroll']) + SCREEN_WIDTH, 0))

# Save/Load system
class SaveSystem:
    def __init__(self, filename="savegame.dat"):
        self.filename = filename
    
    def save_game(self, level, collectibles):
        try:
            with open(self.filename, 'w') as f:
                f.write(f"{level}\n")
                f.write(f"{collectibles}\n")
            return True
        except:
            return False
    
    def load_game(self):
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                level = int(lines[0].strip())
                collectibles = int(lines[1].strip())
                return level, collectibles
        except:
            return 0, 0  # Default values if file doesn't exist
def load_image(name, scale=1.0, convert_alpha=True):
    try:
        # Use absolute path
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "assets", "images", name)
        print(f"Attempting to load image: {path}")
        image = pygame.image.load(path)
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        print(f"Successfully loaded image: {path}")
        return image
    except pygame.error as e:
        print(f"Failed to load image: {path}, Error: {e}")
        # Create a placeholder image if file not found
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 255), (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.line(surf, (0, 0, 0), (0, 0), (TILE_SIZE, TILE_SIZE), 2)
        pygame.draw.line(surf, (0, 0, 0), (TILE_SIZE, 0), (0, TILE_SIZE), 2)
        return surf