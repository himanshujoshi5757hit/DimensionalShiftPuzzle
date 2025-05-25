import pygame
import math
import random
import os
from enum import Enum
from game_engine import Dimension, load_image, load_sound, Animation, ParticleSystem, TILE_SIZE

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE - 4
        self.height = TILE_SIZE - 4
        self.vel_x = 0
        self.vel_y = 0
        self.max_vel_x = 6
        self.max_vel_y = 10
        self.acceleration = 0.5
        self.friction = 0.85
        self.can_jump = False
        self.dimension = Dimension.NORMAL
        self.ethereal_objects = []  # Objects player can pass through in ethereal dimension
        self.metal_objects = []     # Objects player is attracted to in magnetic dimension
        self.shift_cooldown = 0
        self.health = 100
        self.max_health = 100
        self.invincible = 0
        self.score = 0
        self.facing_right = True
        self.is_jumping = False
        self.is_falling = False
        self.is_idle = True
        self.particle_system = ParticleSystem()
        self.character_type = "default"  # Can be "default", "mario", "ninja", "robot"
        # Load sounds
        self.jump_sound = load_sound("jump.wav")
        self.collect_sound = load_sound("collect.wav")
        self.hurt_sound = load_sound("hurt.wav")
        self.dimension_shift_sound = load_sound("dimension_shift.wav")
        # Load animations
        self.animations = {}
        self.load_animations()
        self.current_animation = "idle_normal"
    
    def load_animations(self):
        dimensions = ["normal", "inverse", "ethereal", "time", "magnetic"]
        states = ["idle", "run", "jump", "fall"]
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            character_file = f"{self.character_type}.png"
            character_path = os.path.join(base_path, "assets", "images", character_file)
            if os.path.exists(character_path):
                print(f"Loading character sprite: {character_path}")
                character_sheet = load_image(character_file)
                for dimension_idx, dimension in enumerate(dimensions):
                    for state_idx, state in enumerate(states):
                        key = f"{state}_{dimension}"
                        frames = []
                        for i in range(4):
                            x = i * 40
                            y = (state_idx * len(dimensions) + dimension_idx) * 40
                            frame = pygame.Surface((40, 40), pygame.SRCALPHA)
                            frame.blit(character_sheet, (0, 0), (x, y, 40, 40))
                            frames.append(frame)
                        self.animations[key] = Animation(frames, 8)
                print(f"Successfully loaded {self.character_type} animations")
                return
        except Exception as e:
            print(f"Failed to load character sprite sheet: {e}")
        # Fallback: try to load individual animation files or use colored rectangles
        for dimension in dimensions:
            for state in states:
                key = f"{state}_{dimension}"
                try:
                    frames = []
                    for i in range(1, 5):
                        frame_path = f"player/{self.character_type}_{key}_{i}.png"
                        frames.append(load_image(frame_path))
                    if frames:
                        self.animations[key] = Animation(frames, 8)
                        continue
                except Exception as e:
                    print(f"Failed to load animation {frame_path}: {e}")
                try:
                    frames = []
                    for i in range(1, 5):
                        frame_path = f"player/{key}_{i}.png"
                        frames.append(load_image(frame_path))
                    if frames:
                        self.animations[key] = Animation(frames, 8)
                        continue
                except Exception as e:
                    print(f"Failed to load animation {frame_path}: {e}")
                # Placeholder colored rectangles
                color = self.get_dimension_color(dimension)
                frames = []
                for i in range(4):
                    surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.rect(surf, color, (0, 0, self.width, self.height))
                    if state == "idle" and i == 2:
                        pygame.draw.rect(surf, (255, 255, 255), (self.width//4, self.height//4, 2, 2))
                        pygame.draw.rect(surf, (255, 255, 255), (3*self.width//4, self.height//4, 2, 2))
                    elif state == "run":
                        leg_height = self.height // 3
                        leg_offset = (i % 2) * 4 - 2
                        pygame.draw.rect(surf, (0, 0, 0), (self.width//4, self.height-leg_height+leg_offset, 4, leg_height))
                        pygame.draw.rect(surf, (0, 0, 0), (3*self.width//4, self.height-leg_height-leg_offset, 4, leg_height))
                    elif state == "jump":
                        pygame.draw.ellipse(surf, (0, 0, 0), (self.width//4, self.height-10, self.width//2, 8))
                    elif state == "fall":
                        pygame.draw.ellipse(surf, (0, 0, 0), (self.width//4, self.height-6, self.width//2, 4))
                    frames.append(surf)
                self.animations[key] = Animation(frames, 8)
    
    def change_character(self, character_type):
        self.character_type = character_type
        self.animations = {}
        self.load_animations()
    
    def get_dimension_color(self, dimension_name):
        if dimension_name == "normal":
            return (0, 0, 255)
        elif dimension_name == "inverse":
            return (255, 0, 0)
        elif dimension_name == "ethereal":
            return (128, 0, 128)
        elif dimension_name == "time":
            return (255, 255, 0)
        elif dimension_name == "magnetic":
            return (0, 255, 255)
        return (255, 255, 255)
    
    def update_animation_state(self):
        dimension_name = self.dimension.name.lower()
        if abs(self.vel_x) > 0.5:
            self.is_idle = False
            state = "run"
        elif self.is_jumping:
            self.is_idle = False
            state = "jump"
        elif self.is_falling:
            self.is_idle = False
            state = "fall"
        else:
            self.is_idle = True
            state = "idle"
        self.current_animation = f"{state}_{dimension_name}"
        if self.current_animation not in self.animations:
            self.current_animation = f"{state}_normal"
    
    def update(self, walls, platforms, dimension_portals, collectibles, hazards=None, powerups=None):
        if hazards is None:
            hazards = []
        if powerups is None:
            powerups = []
        if self.dimension == Dimension.NORMAL:
            gravity = 0.5
            self.max_vel_x = 6
        elif self.dimension == Dimension.INVERSE:
            gravity = -0.5
            self.max_vel_x = 6
        elif self.dimension == Dimension.ETHEREAL:
            gravity = 0.5
            self.max_vel_x = 5
        elif self.dimension == Dimension.TIME:
            gravity = 0.25
            self.max_vel_x = 3
        elif self.dimension == Dimension.MAGNETIC:
            gravity = 0.5
            self.max_vel_x = 5
            self.apply_magnetic_attraction()
        self.vel_y += gravity
        if self.vel_y > self.max_vel_y:
            self.vel_y = self.max_vel_y
        elif self.vel_y < -self.max_vel_y:
            self.vel_y = -self.max_vel_y
        self.vel_x *= self.friction
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        self.x += self.vel_x
        self.check_collision_x(walls, platforms)
        self.y += self.vel_y
        self.check_collision_y(walls, platforms)
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False
        if self.vel_y < 0:
            self.is_jumping = True
            self.is_falling = False
        elif self.vel_y > 0:
            self.is_jumping = False
            self.is_falling = True
        else:
            self.is_jumping = False
            self.is_falling = False
        for portal in dimension_portals:
            if self.collides_with(portal) and self.shift_cooldown <= 0:
                old_dimension = self.dimension
                self.dimension = portal.target_dimension
                self.shift_cooldown = 30
                self.dimension_shift_sound.play()
                self.particle_system.create_explosion(
                    self.x + self.width // 2,
                    self.y + self.height // 2,
                    self.get_dimension_color(self.dimension.name.lower()),
                    30, 4
                )
        for collectible in collectibles[:]:
            if self.collides_with(collectible):
                collectibles.remove(collectible)
                self.score += collectible.value
                self.collect_sound.play()
                self.particle_system.create_explosion(
                    collectible.rect.centerx,
                    collectible.rect.centery,
                    collectible.color,
                    15, 3
                )
        if self.invincible <= 0:
            for hazard in hazards:
                if self.collides_with(hazard):
                    self.take_damage(hazard.damage)
                    if self.x < hazard.rect.centerx:
                        self.vel_x = -5
                    else:
                        self.vel_x = 5
                    self.vel_y = -5
        for powerup in powerups[:]:
            if self.collides_with(powerup):
                powerups.remove(powerup)
                powerup.apply_effect(self)
        if self.shift_cooldown > 0:
            self.shift_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
        self.update_animation_state()
        self.particle_system.update()
    
    def apply_magnetic_attraction(self):
        for obj in self.metal_objects:
            dx = obj.rect.centerx - (self.x + self.width // 2)
            dy = obj.rect.centery - (self.y + self.height // 2)
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 20:
                force = 100 / (distance * distance)
                self.vel_x += (dx / distance) * force
                self.vel_y += (dy / distance) * force
    
    def check_collision_x(self, walls, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if self.dimension == Dimension.ETHEREAL and wall in self.ethereal_objects:
                continue
            if player_rect.colliderect(wall.rect):
                if self.vel_x > 0:
                    self.x = wall.rect.left - self.width
                elif self.vel_x < 0:
                    self.x = wall.rect.right
                self.vel_x = 0
    
    def check_collision_y(self, walls, platforms):
        self.can_jump = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if self.dimension == Dimension.ETHEREAL and wall in self.ethereal_objects:
                continue
            if player_rect.colliderect(wall.rect):
                if self.vel_y > 0:
                    self.y = wall.rect.top - self.height
                    self.can_jump = True
                    self.is_falling = False
                elif self.vel_y < 0:
                    self.y = wall.rect.bottom
                self.vel_y = 0
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.dimension == Dimension.NORMAL and self.vel_y > 0:
                    self.y = platform.rect.top - self.height
                    self.can_jump = True
                    self.is_falling = False
                    self.vel_y = 0
                elif self.dimension == Dimension.INVERSE and self.vel_y < 0:
                    self.y = platform.rect.bottom
                    self.can_jump = True
                    self.is_falling = False
                    self.vel_y = 0
    
    def jump(self):
        if self.can_jump:
            if self.dimension == Dimension.NORMAL:
                self.vel_y = -32
            elif self.dimension == Dimension.INVERSE:
                self.vel_y = 28
            elif self.dimension == Dimension.ETHEREAL:
                self.vel_y = -36
            elif self.dimension == Dimension.TIME:
                self.vel_y = -18
            elif self.dimension == Dimension.MAGNETIC:
                self.vel_y = -34
            self.jump_sound.play()
            self.is_jumping = True
            self.can_jump = False
    
    def move_left(self):
        if self.vel_x > -self.max_vel_x:
            self.vel_x -= self.acceleration
            if self.vel_x < -self.max_vel_x:
                self.vel_x = -self.max_vel_x
    
    def move_right(self):
        if self.vel_x < self.max_vel_x:
            self.vel_x += self.acceleration
            if self.vel_x > self.max_vel_x:
                self.vel_x = self.max_vel_x
    
    def take_damage(self, amount):
        if self.invincible <= 0:
            self.health -= amount
            self.invincible = 60
            self.hurt_sound.play()
            self.particle_system.create_explosion(
                self.x + self.width // 2,
                self.y + self.height // 2,
                (255, 0, 0, 128),
                20, 3
            )
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
    
    def collides_with(self, obj):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(obj.rect)
    
    def draw(self, screen, camera=None):
        # Get current animation frame
        if self.current_animation in self.animations:
            current_frame = self.animations[self.current_animation].update()
        else:
            # Fallback if animation not found
            current_frame = self.animations["idle_normal"].update()
        
        # Flip if facing left
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)
        
        # Draw with or without camera
        if camera:
            rect = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
            screen.blit(current_frame, rect)
            
            # Draw particles with camera offset
            for particle in self.particle_system.particles:
                pos = (int(particle['x'] - camera.rect.x), int(particle['y'] - camera.rect.y))
                pygame.draw.circle(screen, particle['color'], pos, particle['size'])
        else:
            screen.blit(current_frame, (self.x, self.y))
            self.particle_system.draw(screen)
        
        # Flash when invincible
        if self.invincible > 0 and self.invincible % 6 < 3:
            if camera:
                rect = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, (255, 255, 255, 128), rect, 2)
            else:
                pygame.draw.rect(screen, (255, 255, 255, 128), (self.x, self.y, self.width, self.height), 2)

# Wall class
class Wall:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_ethereal = False
        self.is_metal = False
        try:
            self.image = load_image("wall.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = None
    def draw(self, screen, camera=None):
        if camera:
            rect = camera.apply(self.rect)
        else:
            rect = self.rect
        if self.image:
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)

# Platform class
class Platform(Wall):
    def __init__(self, x, y, width, height=10):
        super().__init__(x, y, width, height, (0, 255, 0))
        try:
            self.image = load_image("platform.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = None

# Dimension Portal class
class DimensionPortal:
    def __init__(self, x, y, target_dimension):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.target_dimension = target_dimension
        self.animation_timer = 0
        if target_dimension == Dimension.NORMAL:
            self.color = (0, 0, 255)
        elif target_dimension == Dimension.INVERSE:
            self.color = (255, 0, 0)
        elif target_dimension == Dimension.ETHEREAL:
            self.color = (128, 0, 128)
        elif target_dimension == Dimension.TIME:
            self.color = (255, 255, 0)
        elif target_dimension == Dimension.MAGNETIC:
            self.color = (0, 255, 255)
        try:
            self.image = load_image(f"portal_{target_dimension.name.lower()}.png")
        except:
            self.image = None
        if not self.image:
            self.frames = []
            for i in range(8):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                size = TILE_SIZE - 4 + math.sin(i / 4 * math.pi) * 4
                pygame.draw.circle(surf, self.color, (TILE_SIZE // 2, TILE_SIZE // 2), int(size // 2))
                pygame.draw.circle(surf, (255, 255, 255), (TILE_SIZE // 2, TILE_SIZE // 2), int(size // 4))
                self.frames.append(surf)
            self.animation = Animation(self.frames, 5)
    def update(self):
        self.animation_timer = (self.animation_timer + 1) % 360
    def draw(self, screen, camera=None):
        if camera:
            rect = camera.apply(self.rect)
        else:
            rect = self.rect
        if self.image:
            angle = self.animation_timer
            rotated_image = pygame.transform.rotate(self.image, angle)
            new_rect = rotated_image.get_rect(center=rect.center)
            screen.blit(rotated_image, new_rect)
        else:
            current_frame = self.animation.update()
            screen.blit(current_frame, rect)

# Collectible class
class Collectible:
    def __init__(self, x, y, value=10):
        self.rect = pygame.Rect(x + TILE_SIZE//4, y + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
        self.color = (255, 215, 0)
        self.value = value
        self.animation_timer = random.randint(0, 360)
        try:
            self.image = load_image("collectible.png")
        except:
            self.image = None
    def update(self):
        self.animation_timer = (self.animation_timer + 1) % 360
    def draw(self, screen, camera=None):
        offset_y = math.sin(self.animation_timer / 30) * 3
        if camera:
            rect = camera.apply(self.rect)
            rect.y += offset_y
        else:
            rect = pygame.Rect(self.rect.x, self.rect.y + offset_y, self.rect.width, self.rect.height)
        if self.image:
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)
            shine_pos = (rect.x + rect.width * 0.7, rect.y + rect.height * 0.3)
            pygame.draw.circle(screen, (255, 255, 255), shine_pos, 2)

# Hazard class
class Hazard:
    def __init__(self, x, y, width, height, damage=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 50, 50)
        self.damage = damage
        self.animation_timer = 0
        try:
            self.image = load_image("hazard.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = None
    def update(self):
        self.animation_timer = (self.animation_timer + 1) % 60
    def draw(self, screen, camera=None):
        if camera:
            rect = camera.apply(self.rect)
        else:
            rect = self.rect
        if self.image:
            screen.blit(self.image, rect)
        else:
            pulse = abs(math.sin(self.animation_timer / 10)) * 50
            color = (255, 50 + pulse, 50)
            pygame.draw.rect(screen, color, rect)
            for i in range(0, rect.width, 10):
                pygame.draw.line(screen, (0, 0, 0), (rect.x + i, rect.y), (rect.x + i + 5, rect.y + rect.height), 2)

# Powerup class
class Powerup:
    def __init__(self, x, y, powerup_type="health"):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.powerup_type = powerup_type
        self.animation_timer = random.randint(0, 360)
        if powerup_type == "health":
            self.color = (0, 255, 0)
        elif powerup_type == "speed":
            self.color = (0, 255, 255)
        elif powerup_type == "jump":
            self.color = (255, 255, 0)
        elif powerup_type == "invincibility":
            self.color = (255, 255, 255)
        try:
            self.image = load_image(f"powerup_{powerup_type}.png")
        except:
            self.image = None
    def update(self):
        self.animation_timer = (self.animation_timer + 1) % 360
    def draw(self, screen, camera=None):
        offset_y = math.sin(self.animation_timer / 30) * 3
        scale = 1.0 + math.sin(self.animation_timer / 15) * 0.1
        if camera:
            base_rect = camera.apply(self.rect)
        else:
            base_rect = self.rect.copy()
        rect = pygame.Rect(base_rect.x, base_rect.y + offset_y, base_rect.width, base_rect.height)
        if self.image:
            scaled_size = (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
            scaled_image = pygame.transform.scale(self.image, scaled_size)
            scaled_rect = scaled_image.get_rect(center=rect.center)
            screen.blit(scaled_image, scaled_rect)
        else:
            pygame.draw.circle(screen, self.color, rect.center, int(rect.width // 2 * scale))
            pygame.draw.circle(screen, (255, 255, 255), rect.center, int(rect.width // 4 * scale))
    def apply_effect(self, player):
        if self.powerup_type == "health":
            player.heal(25)
        elif self.powerup_type == "speed":
            player.max_vel_x *= 1.5
        elif self.powerup_type == "jump":
            pass  # Implement jump boost if needed
        elif self.powerup_type == "invincibility":
            player.invincible = 300

# Moving Platform class
class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, x_range=0, y_range=100, speed=1):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.x_range = x_range
        self.y_range = y_range
        self.speed = speed
        self.progress = 0
    def update(self):
        self.progress = (self.progress + self.speed) % 360
        if self.x_range > 0:
            self.rect.x = self.start_x + math.sin(math.radians(self.progress)) * self.x_range
        if self.y_range > 0:
            self.rect.y = self.start_y + math.sin(math.radians(self.progress)) * self.y_range

# Metal Wall class for magnetic dimension
class MetalWall(Wall):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (192, 192, 192))
        self.is_metal = True
        try:
            self.image = load_image("metal_wall.png")
            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = None
