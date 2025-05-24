import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)

# Simple function to display controls
def show_controls():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Controls")
    clock = pygame.time.Clock()
    
    # Set up fonts
    font_large = pygame.font.SysFont(None, 64)
    font_medium = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)
    
    # Create a back button
    back_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50)
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    print("Back button clicked!")
                    running = False
        
        # Draw background
        screen.fill((20, 20, 50))
        
        # Draw title
        title_text = "Game Controls"
        title_surf = font_large.render(title_text, True, WHITE)
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Draw controls information
        controls_info = [
            "Movement Controls:",
            "- Arrow Keys or WASD: Move left/right",
            "- Space or Up Arrow or W: Jump",
            "- ESC: Pause game",
            "",
            "Dimension Information:",
            "- Blue (Normal): Standard physics",
            "- Red (Inverse): Gravity is reversed",
            "- Purple (Ethereal): Pass through special walls",
            "- Yellow (Time): Slowed physics for precision",
            "- Cyan (Magnetic): Attracted to metal objects",
            "",
            "Game Objectives:",
            "- Collect all items in each level",
            "- Reach the exit portal",
            "- Use dimension portals to change your physics",
            "- Avoid hazards and obstacles"
        ]
        
        y_offset = 120
        for text in controls_info:
            if text == "":
                y_offset += 10
                continue
                
            if ":" in text and text[-1] == ":":
                # Section header
                text_surf = font_medium.render(text, True, (255, 255, 100))
            else:
                # Regular text
                text_surf = font_small.render(text, True, WHITE)
                
            screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_offset))
            y_offset += 30
        
        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 150, 255) if back_button.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, button_color, back_button)
        pygame.draw.rect(screen, WHITE, back_button, 2)
        
        back_text = font_medium.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

# Run this file directly to test the controls screen
if __name__ == "__main__":
    show_controls()
    pygame.quit()
    sys.exit()
