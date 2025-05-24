import pygame
import sys
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

# Simple test app to verify button functionality
def main():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Button Test")
    clock = pygame.time.Clock()
    
    # Create buttons
    buttons = [
        Button(SCREEN_WIDTH//2 - 100, 100, 200, 50, "Button 1", (100, 100, 200)),
        Button(SCREEN_WIDTH//2 - 100, 200, 200, 50, "Button 2", (100, 200, 100)),
        Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Button 3", (200, 100, 100)),
        Button(SCREEN_WIDTH//2 - 100, 400, 200, 50, "Quit", (200, 50, 50))
    ]
    
    # Create a sound for button clicks
    try:
        click_sound = pygame.mixer.Sound("assets/sounds/menu_select.wav")
    except:
        # Create a simple beep sound if file not found
        click_sound = pygame.mixer.Sound.from_buffer(bytes([128] * 1000), 1000)
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_clicked(event):
                        click_sound.play()
                        print(f"Button {i+1} action triggered")
                        if i == 3:  # Quit button
                            running = False
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
        
        # Draw
        screen.fill((30, 30, 50))
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        # Draw instructions
        font = pygame.font.SysFont(None, 24)
        instructions = [
            "Click on the buttons to test if they work correctly.",
            "You should see messages in the console when buttons are clicked.",
            "If buttons work here but not in the main game, there's an issue with the game's event handling."
        ]
        
        for i, text in enumerate(instructions):
            text_surf = font.render(text, True, WHITE)
            screen.blit(text_surf, (20, 500 + i * 30))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
