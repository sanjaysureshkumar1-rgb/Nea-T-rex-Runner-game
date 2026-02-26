import pygame
# ====================
# SCREEN SETTINGS
# ====================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Frame rate
FPS = 60

# ====================
# COLOURS (UK SPELLING!)
# ====================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREY = (128, 128, 128)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (147, 112, 219)
PINK = (255, 105, 180)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235)

# UI Colours
BG_COLOR = (135, 206, 235)  # Sky blue background
BUTTON_SHADOW = (50, 50, 50)
TEXT_SHADOW = (100, 100, 100)

# ====================
# GAME MECHANICS
# ====================
GROUND_LEVEL = 450
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ANIMATION_SPEED = 10

# ====================
# POWER-UP SETTINGS
# ====================
SHIELD_DURATION = 300      # 5 seconds at 60 FPS
SPEED_DURATION = 180       # 3 seconds at 60 FPS
DOUBLE_JUMP_DURATION = 240 # 4 seconds at 60 FPS
MAGNET_DURATION = 360      # 6 seconds at 60 FPS

# ====================
# SPAWN RATES
# ====================
OBSTACLE_SPAWN_RATE = 90   # Frames between obstacles
COIN_SPAWN_RATE = 120      # Frames between coins
POWERUP_SPAWN_RATE = 400   # Frames between power-ups

# ====================
# SCORING
# ====================
OBSTACLE_DODGE_POINTS = 10
COIN_COLLECT_POINTS = 50
POWERUP_COLLECT_POINTS = 25
SHIELD_BLOCK_POINTS = 50

# ====================
# LEVEL PROGRESSION
# ====================
POINTS_PER_LEVEL = 500

# ====================
# SKIN SYSTEM
# ====================
AVAILABLE_SKINS = {
    "Classic": {
        "color": (34, 139, 34),      # Green
        "unlocked": True,
        "cost": 0,
        "description": "Original dinosaur"
    },
    "Red Rex": {
        "color": (220, 20, 60),       # Crimson
        "unlocked": False,
        "cost": 100,
        "description": "Fiery red dinosaur"
    },
    "Blue": {
        "color": (30, 144, 255),      # Dodger blue
        "unlocked": False,
        "cost": 150,
        "description": "Cool blue dinosaur"
    },
    "Golden": {
        "color": (255, 215, 0),       # Gold
        "unlocked": False,
        "cost": 200,
        "description": "Shiny golden dinosaur"
    },
    "Purple": {
        "color": (138, 43, 226),      # Blue violet
        "unlocked": False,
        "cost": 250,
        "description": "Purple dinosaur"
    },
    "Pink": {
        "color": (255, 105, 180),     # Hot pink
        "unlocked": False,
        "cost": 300,
        "description": "pink dinosaur"
    },
    "Orange": {
        "color": (255, 140, 0),       # Dark orange
        "unlocked": False,
        "cost": 350,
        "description": "Sunset orange dinosaur"
    },
    "Aqua": {
        "color": (0, 255, 255),       # Cyan
        "unlocked": False,
        "cost": 400,
        "description": "Ocean aqua dinosaur"
    },
    "Shadow": {
        "color": (50, 50, 50),        # Dark grey
        "unlocked": False,
        "cost": 500,
        "description": "Shadow dinosaur"
    },
    "Rainbow": {
        "color": (255, 0, 255),       # Magenta (will animate)
        "unlocked": False,
        "cost": 1000,
        "description": "Legendary rainbow dinosaur"
    }
}