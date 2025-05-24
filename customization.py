import pygame
import os
from game_engine import Button, SCREEN_WIDTH, SCREEN_HEIGHT

class CustomizationMenu:
    def __init__(self, screen, font_large, font_medium):
        self.screen = screen
        self.font_large = font_large
        self.font_medium = font_medium
        
        # Current selections
        self.current_character = "default"
        self.current_bg_style = "default"
        
        # Available options
        self.character_options = ["default", "mario", "ninja", "robot"]
        self.bg_options = ["default", "forest", "desert", "snow", "night"]
        
        # Create buttons
        self.main_buttons = [
            Button(SCREEN_WIDTH//2 - 150, 200, 300, 50, "Change Character"),
            Button(SCREEN_WIDTH//2 - 150, 270, 300, 50, "Change Background"),
            Button(SCREEN_WIDTH//2 - 150, 340, 300, 50, "Back")
        ]
        
        # Create character selection buttons
        self.character_buttons = []
        for i, character in enumerate(self.character_options):
            x = SCREEN_WIDTH//2 - 300 + (i * 150)
            self.character_buttons.append(Button(x, 200, 140, 50, character.title()))
        self.character_buttons.append(Button(SCREEN_WIDTH//2 - 100, 270, 200, 50, "Back"))
        
        # Create background selection buttons
        self.bg_buttons = []
        for i, bg in enumerate(self.bg_options):
            if i < 3:  # First row
                x = SCREEN_WIDTH//2 - 300 + (i * 150)
                y = 200
            else:  # Second row
                x = SCREEN_WIDTH//2 - 225 + ((i-3) * 150)
                y = 260
            self.bg_buttons.append(Button(x, y, 140, 50, bg.title()))
        self.bg_buttons.append(Button(SCREEN_WIDTH//2 - 100, 330, 200, 50, "Back"))
        
        # Menu state
        self.state = "main"  # "main", "character", "background"
        
        # Preview images
        self.character_previews = self.load_character_previews()
        self.bg_previews = self.load_bg_previews()
    
    def load_character_previews(self):
        previews = {}
        for character in self.character_options:
            try:
                # Try to load character preview
                path = f"assets/images/{character}.png"
                if os.path.exists(path):
                    img = pygame.image.load(path)
                    # Extract a single frame as preview
                    preview = pygame.Surface((40, 40), pygame.SRCALPHA)
                    preview.blit(img, (0, 0), (0, 0, 40, 40))
                    previews[character] = pygame.transform.scale(preview, (80, 80))
                else:
                    # Create placeholder
                    preview = pygame.Surface((80, 80), pygame.SRCALPHA)
                    if character == "default":
                        color = (0, 0, 255)
                    elif character == "mario":
                        color = (255, 0, 0)
                    elif character == "ninja":
                        color = (0, 0, 0)
                    elif character == "robot":
                        color = (192, 192, 192)
                    else:
                        color = (100, 100, 100)
                    pygame.draw.rect(preview, color, (0, 0, 80, 80))
                    previews[character] = preview
            except Exception as e:
                print(f"Failed to load character preview: {e}")
                # Create placeholder
                preview = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.rect(preview, (100, 100, 100), (0, 0, 80, 80))
                previews[character] = preview
        return previews
    
    def load_bg_previews(self):
        previews = {}
        for bg in self.bg_options:
            try:
                # Try to load background preview
                path = f"assets/images/bg_{bg}.png"
                if os.path.exists(path):
                    img = pygame.image.load(path)
                    previews[bg] = pygame.transform.scale(img, (200, 150))
                else:
                    # Create placeholder
                    preview = pygame.Surface((200, 150))
                    if bg == "default":
                        color = (0, 0, 50)
                    elif bg == "forest":
                        color = (0, 100, 0)
                    elif bg == "desert":
                        color = (200, 180, 50)
                    elif bg == "snow":
                        color = (220, 220, 255)
                    elif bg == "night":
                        color = (20, 20, 50)
                    else:
                        color = (100, 100, 100)
                    preview.fill(color)
                    previews[bg] = preview
            except Exception as e:
                print(f"Failed to load bg preview: {e}")
                # Create placeholder
                preview = pygame.Surface((200, 150))
                preview.fill((100, 100, 100))
                previews[bg] = preview
        return previews
    
    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "main":
            for i, button in enumerate(self.main_buttons):
                button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_clicked(event):
                    if i == 0:  # Change Character
                        self.state = "character"
                        return None, None
                    elif i == 1:  # Change Background
                        self.state = "background"
                        return None, None
                    elif i == 2:  # Back
                        return None, None, "back"
        
        elif self.state == "character":
            for i, button in enumerate(self.character_buttons):
                button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_clicked(event):
                    if i < len(self.character_options):  # Character selection
                        self.current_character = self.character_options[i]
                        return self.current_character, None, None
                    else:  # Back button
                        self.state = "main"
                        return None, None, None
        
        elif self.state == "background":
            for i, button in enumerate(self.bg_buttons):
                button.update(mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_clicked(event):
                    if i < len(self.bg_options):  # Background selection
                        self.current_bg_style = self.bg_options[i]
                        return None, self.current_bg_style, None
                    else:  # Back button
                        self.state = "main"
                        return None, None, None
        
        return None, None, None
    
    def draw(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = "Customize Your Game"
        title_surf = self.font_large.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
        
        if self.state == "main":
            # Draw main customization menu
            for button in self.main_buttons:
                button.draw(self.screen)
            
            # Draw current selections
            char_text = f"Current Character: {self.current_character.title()}"
            char_surf = self.font_medium.render(char_text, True, (255, 255, 255))
            self.screen.blit(char_surf, (SCREEN_WIDTH//2 - char_surf.get_width()//2, 400))
            
            bg_text = f"Current Background: {self.current_bg_style.title()}"
            bg_surf = self.font_medium.render(bg_text, True, (255, 255, 255))
            self.screen.blit(bg_surf, (SCREEN_WIDTH//2 - bg_surf.get_width()//2, 440))
            
            # Draw previews
            if self.current_character in self.character_previews:
                self.screen.blit(self.character_previews[self.current_character], (SCREEN_WIDTH//2 - 40, 480))
            
            if self.current_bg_style in self.bg_previews:
                preview_rect = self.bg_previews[self.current_bg_style].get_rect(center=(SCREEN_WIDTH//2, 550))
                self.screen.blit(self.bg_previews[self.current_bg_style], preview_rect)
        
        elif self.state == "character":
            # Draw character selection menu
            title_text = "Select Character"
            title_surf = self.font_medium.render(title_text, True, (255, 255, 255))
            self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 150))
            
            for button in self.character_buttons:
                button.draw(self.screen)
            
            # Draw character previews
            for i, character in enumerate(self.character_options):
                if character in self.character_previews:
                    x = SCREEN_WIDTH//2 - 300 + (i * 150) + 70
                    y = 140
                    self.screen.blit(self.character_previews[character], (x - 40, y - 80))
                    
                    # Highlight selected character
                    if character == self.current_character:
                        pygame.draw.rect(self.screen, (255, 255, 0), 
                                        (x - 42, y - 82, 84, 84), 2)
        
        elif self.state == "background":
            # Draw background selection menu
            title_text = "Select Background"
            title_surf = self.font_medium.render(title_text, True, (255, 255, 255))
            self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 150))
            
            for button in self.bg_buttons:
                button.draw(self.screen)
            
            # Draw background previews above buttons
            for i, bg in enumerate(self.bg_options):
                if bg in self.bg_previews:
                    if i < 3:  # First row
                        x = SCREEN_WIDTH//2 - 300 + (i * 150) + 70
                        y = 140
                    else:  # Second row
                        x = SCREEN_WIDTH//2 - 225 + ((i-3) * 150) + 70
                        y = 200
                    
                    preview = pygame.transform.scale(self.bg_previews[bg], (100, 75))
                    self.screen.blit(preview, (x - 50, y - 90))
                    
                    # Highlight selected background
                    if bg == self.current_bg_style:
                        pygame.draw.rect(self.screen, (255, 255, 0), 
                                        (x - 52, y - 92, 104, 79), 2)
