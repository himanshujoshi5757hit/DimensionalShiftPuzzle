# Dimensional Shift Puzzle

A unique puzzle platformer game where you shift between dimensions with different physics to solve puzzles.

## Unique Game Concept

This game features a dimensional shifting mechanic where players can switch between five different dimensions, each with unique physics:

1. **Normal Dimension** (Blue): Standard physics with normal gravity
2. **Inverse Dimension** (Red): Inverted gravity - you fall upward!
3. **Ethereal Dimension** (Purple): Allows you to pass through special walls marked with 'X'
4. **Time Dimension** (Yellow): Slows down gravity and movement, allowing for more precise jumps
5. **Magnetic Dimension** (Cyan): Attracts the player to metal objects

## Game Features

- **10 Challenging Levels**: Progressively more complex puzzles
- **Dimension Portals**: Special tiles that switch your dimension when touched
- **Collectibles**: Must be gathered before completing a level
- **Hazards**: Dangerous obstacles that damage the player
- **Powerups**: Special items that give temporary abilities
- **Moving Platforms**: Dynamic obstacles that require timing
- **Particle Effects**: Visual feedback for actions
- **Animations**: Character and object animations
- **Sound Effects**: Audio feedback for game events
- **Background Music**: Immersive audio experience
- **Save System**: Track your progress
- **Customization**: Change player character and background styles

## How to Play

1. Install Pygame if you don't have it already: `pip install pygame`
2. Run the game: `python main.py`

## Controls

- **Arrow Keys** or **WASD**: Move left/right
- **Space** or **Up Arrow** or **W**: Jump
- **ESC**: Pause game
- **Mouse**: Navigate menus

## Level Guide

1. **Level 1**: Introduction to basic movement and ethereal dimension
2. **Level 2**: Introduction to inverse gravity
3. **Level 3**: Introduction to ethereal walls
4. **Level 4**: Introduction to time dimension
5. **Level 5**: Introduction to magnetic dimension
6. **Level 6**: Combining dimensions with hazards
7. **Level 7**: Moving platforms and collectibles
8. **Level 8**: Complex ethereal maze
9. **Level 9**: Time-based precision jumping
10. **Level 10**: Master level combining all dimensions

## Customization Options

### Characters
- **Default**: Simple character with dimension-colored appearance
- **Mario**: Inspired by the classic platformer character
- **Ninja**: Stealthy character with unique animations
- **Robot**: Mechanical character with blinking lights

### Background Styles
- **Default**: Classic blue sky with mountains
- **Forest**: Lush green environment with trees
- **Desert**: Sandy landscape with cacti
- **Snow**: Winter wonderland with snowflakes
- **Night**: Dark setting with stars and moon

## Requirements

- Python 3.x
- Pygame library

## Installation

```bash
# Clone the repository or download the zip file
# Navigate to the game directory
cd DimensionalShiftPuzzle

# Install required packages
pip install -r requirements.txt

# Run the game
python main.py
```

## Creating Assets

If you want to generate placeholder assets for the game:

```bash
# Generate character sprites
python create_character_sprites.py

# Generate background styles
python create_background_styles.py

# Generate all game assets
python create_placeholder_assets.py
```

## Game Structure

- **main.py**: Main game loop and state management
- **game_engine.py**: Core game mechanics and utilities
- **game_objects.py**: Game object classes (Player, Walls, etc.)
- **level_manager.py**: Level creation and management
- **customization.py**: Character and background customization
- **assets/**: Directory containing images, sounds, and fonts

## Credits

Created as a unique puzzle platformer with dimensional shifting mechanics.

Enjoy the game!
