# Asset Guide for Dimensional Shift Puzzle

This guide explains how to add images and sounds to your game.

## Image Assets

### Required Folder Structure
```
DimensionalShiftPuzzle/
└── assets/
    ├── images/
    │   ├── player/
    │   │   ├── idle_normal_1.png
    │   │   ├── idle_normal_2.png
    │   │   └── ...
    │   ├── background_1.png
    │   ├── background_2.png
    │   ├── ...
    │   ├── wall.png
    │   ├── platform.png
    │   └── ...
    └── sounds/
        ├── jump.wav
        ├── collect.wav
        └── ...
```

### Option 1: Individual Player Animation Frames
Place individual animation frames in the `assets/images/player/` folder with these naming conventions:
- `idle_normal_1.png`, `idle_normal_2.png`, etc. (4 frames)
- `run_normal_1.png`, `run_normal_2.png`, etc. (4 frames)
- `jump_normal_1.png`, etc.
- `fall_normal_1.png`, etc.

Repeat for each dimension: normal, inverse, ethereal, time, magnetic

### Option 2: Mario Sprite Sheet
Place a single sprite sheet named `mario.png` in the `assets/images/` folder.
The code will automatically detect and use this sprite sheet if available.

### Background Images
- Level backgrounds: `background_1.png` through `background_10.png` in `assets/images/`
- Parallax backgrounds: `bg_layer1.png`, `bg_layer2.png`, `bg_layer3.png` in `assets/images/`

### Game Object Images
- `wall.png` - Basic wall texture
- `platform.png` - Platform texture
- `metal_wall.png` - Metal wall for magnetic dimension
- `collectible.png` - Collectible item
- `hazard.png` - Hazard/danger object
- `portal_normal.png`, `portal_inverse.png`, etc. - Dimension portals

## Sound Assets

Place sound files in the `assets/sounds/` folder:
- `jump.wav` - Player jump sound
- `collect.wav` - Collectible pickup sound
- `hurt.wav` - Player damage sound
- `dimension_shift.wav` - Dimension change sound
- `menu_select.wav` - Menu selection sound
- `level_complete.wav` - Level completion sound
- `game_over.wav` - Game over sound
- `game_complete.wav` - Game completion sound
- `menu_music.mp3` - Menu background music
- `level_1.mp3` through `level_10.mp3` - Level background music

## Image Sizes

- **Background images**: 800x600 pixels
- **Player character**: Approximately 36x36 pixels
- **Game objects**: 40x40 pixels (matching TILE_SIZE)
- **Collectibles**: 20x20 pixels (half of TILE_SIZE)

## File Formats

- Images: PNG format with transparency where needed
- Sounds: WAV or MP3 format

## Troubleshooting

If your images aren't showing up:
1. Check the console output for loading errors
2. Verify file names and paths match exactly what's expected
3. Make sure images are in the correct format (PNG recommended)
4. Check image dimensions - too large images may cause performance issues
