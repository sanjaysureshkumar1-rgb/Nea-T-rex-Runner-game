import pygame
class Tile:
    """Represents a single tile in the level"""

    def __init__(self, tile_type, x, y, size=40):
        self.type = tile_type
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = self.get_color()

    def get_color(self):
        """Return color based on tile type"""
        colors = {
            0: None,  # Empty space
            1: (101, 67, 33),  # Ground/Platform (brown)
            2: (255, 0, 0),  # Obstacle/Danger (red)
            3: (255, 215, 0),  # Coin (gold)
            4: (0, 191, 255),  # Power-up (blue)
            5: (34, 139, 34),  # Moving platform (green)
            6: (128, 128, 128)  # Wall (gray)
        }
        return colors.get(self.type)

    def draw(self, screen):
        """Draw the tile on screen"""
        if self.color:
            pygame.draw.rect(screen, self.color, self.rect)
            # Add border for visibility
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)


class Level:
    """Manages the entire level using 2D arrays"""

    def __init__(self, level_data, tile_size=40):
        self.tile_size = tile_size
        self.level_data = level_data
        self.tiles = []
        self.platforms = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.create_level()

    def create_level(self):
        """Create tiles from 2D array"""
        for row_index, row in enumerate(self.level_data):
            for col_index, tile_type in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                if tile_type != 0:  # Not empty space
                    tile = Tile(tile_type, x, y, self.tile_size)
                    self.tiles.append(tile)

                    # Categorize tiles
                    if tile_type == 1:
                        self.platforms.append(tile)
                    elif tile_type == 2:
                        self.obstacles.append(tile)
                    elif tile_type == 3:
                        self.coins.append(tile)
                    elif tile_type == 4:
                        self.powerups.append(tile)

    def draw(self, screen):
        """Draw all tiles"""
        for tile in self.tiles:
            tile.draw(screen)

    def get_platforms(self):
        """Return list of platform rectangles for collision"""
        return [tile.rect for tile in self.platforms]

    def get_obstacles(self):
        """Return list of obstacle rectangles for collision"""
        return [tile.rect for tile in self.obstacles]

    def remove_coin(self, coin_rect):
        """Remove collected coin"""
        self.coins = [c for c in self.coins if c.rect != coin_rect]
        self.tiles = [t for t in self.tiles if t.rect != coin_rect]

    def remove_powerup(self, powerup_rect):
        """Remove collected power-up"""
        self.powerups = [p for p in self.powerups if p.rect != powerup_rect]
        self.tiles = [t for t in self.tiles if t.rect != powerup_rect]


# EXAMPLE LEVEL DESIGNS
# 0 = Empty, 1 = Platform, 2 = Obstacle, 3 = Coin, 4 = Power-up, 5 = Moving Platform

LEVEL_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

LEVEL_2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 4, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

LEVEL_3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 3, 0, 0, 2, 0, 0, 4, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 1, 0, 3, 0, 1, 0, 3, 0, 1, 0, 3, 0, 1, 0, 3, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# Level Manager to switch between levels
class LevelManager:
    """Manages multiple levels and progression"""

    def __init__(self):
        self.levels = [LEVEL_1, LEVEL_2, LEVEL_3]
        self.current_level_index = 0
        self.current_level = None
        self.load_level(0)

    def load_level(self, level_index):
        """Load a specific level"""
        if 0 <= level_index < len(self.levels):
            self.current_level_index = level_index
            self.current_level = Level(self.levels[level_index])
            return True
        return False

    def next_level(self):
        """Progress to next level"""
        next_index = self.current_level_index + 1
        if next_index < len(self.levels):
            return self.load_level(next_index)
        return False  # No more levels

    def restart_level(self):
        """Restart current level"""
        return self.load_level(self.current_level_index)

    def get_current_level(self):
        """Get current level object"""
        return self.current_level
