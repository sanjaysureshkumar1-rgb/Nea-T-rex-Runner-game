import pygame
import random
from settings import *


class Background:
    """Base background class with pre-rendering"""

    def __init__(self, environment_type):
        self.environment_type = environment_type
        self.scroll_offset = 0

        self.sky_surface = pygame.Surface((SCREEN_WIDTH, GROUND_LEVEL))
        self.ground_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))

        self.create_static_elements()

    def create_static_elements(self):
        """Create surfaces that don't change - ONCE only"""
        pass

    def update(self, speed=5):
        """Update background scrolling"""
        self.scroll_offset += speed
        if self.scroll_offset >= SCREEN_WIDTH:
            self.scroll_offset = 0

    def draw(self, screen):
        """Draw background - override in subclasses"""
        pass


class DesertBackground(Background):
    """Optimised desert environment"""

    def __init__(self):
        # Define attributes BEFORE calling super().__init__()
        self.sand_color = (237, 201, 175)
        self.sun_position = (SCREEN_WIDTH - 100, 80)

        super().__init__("desert")

        # Background cacti (parallax)
        self.background_cacti = []
        for i in range(5):
            self.background_cacti.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': GROUND_LEVEL - random.randint(20, 40),
                'height': random.randint(15, 30),
                'offset': random.randint(0, 100)
            })

    def create_static_elements(self):
        """Pre-render sky and ground ONCE"""
        sky_color_top = (135, 206, 250)
        sky_color_bottom = (255, 228, 181)

        for y in range(GROUND_LEVEL):
            ratio = y / GROUND_LEVEL
            color = (
                int(sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * ratio),
                int(sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * ratio),
                int(sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (SCREEN_WIDTH, y))

        # Ground (pre-drawn)
        self.ground_surface.fill(self.sand_color)

    def draw(self, screen):
        """Draw desert - FAST VERSION"""
        # Blit pre-made sky
        screen.blit(self.sky_surface, (0, 0))

        # Sun
        pygame.draw.circle(screen, (255, 220, 100), self.sun_position, 40)
        pygame.draw.circle(screen, (255, 200, 50), self.sun_position, 35)

        # Simple distant mountains (just 2, not loads)
        mountain_x = (self.scroll_offset * 0.3) % (SCREEN_WIDTH + 200) - 100
        pygame.draw.polygon(screen, (180, 140, 100), [
            (mountain_x, GROUND_LEVEL),
            (mountain_x + 150, GROUND_LEVEL - 80),
            (mountain_x + 300, GROUND_LEVEL)
        ])

        # Background cacti (parallax) - simplified
        for cactus in self.background_cacti:
            x = int((cactus['x'] - self.scroll_offset * 0.5 + cactus['offset']) % (SCREEN_WIDTH + 100))
            y = cactus['y']
            h = cactus['height']

            cactus_color = (100, 140, 100)
            pygame.draw.rect(screen, cactus_color, (x, y, 4, h))
            pygame.draw.rect(screen, cactus_color, (x - 3, y + h // 3, 4, h // 4))

        # Blit pre-made ground
        screen.blit(self.ground_surface, (0, GROUND_LEVEL))

        # Simple ground dots (fewer of them)
        for i in range(10):  # Was 20, now 10
            dot_x = int((i * 80 + self.scroll_offset * 2) % SCREEN_WIDTH)
            dot_y = GROUND_LEVEL + 10 + (i % 3) * 15
            pygame.draw.circle(screen, (227, 191, 165), (dot_x, dot_y), 2)

        # Ground line
        pygame.draw.line(screen, (200, 170, 140), (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)


class JungleBackground(Background):
    """Optimised jungle environment"""

    def __init__(self):
        # Define attributes BEFORE calling super().__init__()
        self.grass_color = (34, 139, 34)

        super().__init__("jungle")

        # Generate trees
        self.trees = []
        for i in range(4):  # Reduced from 6 to 4
            self.trees.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'height': random.randint(80, 120),
                'offset': random.randint(0, 100)
            })

    def create_static_elements(self):
        """Pre-render sky and ground"""
        sky_color_top = (100, 180, 255)
        sky_color_bottom = (150, 220, 200)

        for y in range(GROUND_LEVEL):
            ratio = y / GROUND_LEVEL
            color = (
                int(sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * ratio),
                int(sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * ratio),
                int(sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (SCREEN_WIDTH, y))

        self.ground_surface.fill(self.grass_color)

    def draw(self, screen):
        """Draw jungle - FAST VERSION"""
        # Blit pre-made sky
        screen.blit(self.sky_surface, (0, 0))

        # Background trees (parallax) - simplified drawing
        for tree in self.trees:
            x = int((tree['x'] - self.scroll_offset * 0.5 + tree['offset']) % (SCREEN_WIDTH + 100))
            h = tree['height']

            # Tree trunk
            trunk_color = (101, 67, 33)
            pygame.draw.rect(screen, trunk_color, (x, GROUND_LEVEL - h, 15, h))

            # Simple foliage (one circle instead of three)
            foliage_color = (34, 139, 34)
            pygame.draw.circle(screen, foliage_color, (int(x + 7), int(GROUND_LEVEL - h - 10)), 25)

        # Blit pre-made ground
        screen.blit(self.ground_surface, (0, GROUND_LEVEL))

        # Grass blades (reduced amount)
        for i in range(15):  # Was 30, now 15
            grass_x = int((i * 60 + self.scroll_offset * 3) % SCREEN_WIDTH)
            grass_y = GROUND_LEVEL
            pygame.draw.line(screen, (0, 100, 0), (grass_x, grass_y), (grass_x + 2, grass_y - 8), 2)

        # Ground line
        pygame.draw.line(screen, (20, 100, 20), (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)


class IceBackground(Background):
    """Optimised ice environment"""

    def __init__(self):
        # Define attributes BEFORE calling super().__init__()
        self.ice_color = (240, 248, 255)

        super().__init__("ice")

        # Fewer snowflakes
        self.snowflakes = []
        for i in range(20):  # Was 30, now 20
            self.snowflakes.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(1, 2),
                'size': random.randint(2, 4)
            })

        # Ice crystals
        self.crystals = []
        for i in range(3):  # Was 5, now 3
            self.crystals.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': GROUND_LEVEL - random.randint(10, 30),
                'size': random.randint(15, 25),
                'offset': random.randint(0, 100)
            })

    def create_static_elements(self):
        """Pre-render sky and ground"""
        sky_color_top = (180, 200, 230)
        sky_color_bottom = (230, 240, 255)

        for y in range(GROUND_LEVEL):
            ratio = y / GROUND_LEVEL
            color = (
                int(sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * ratio),
                int(sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * ratio),
                int(sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (SCREEN_WIDTH, y))

        self.ground_surface.fill(self.ice_color)

    def update(self, speed=5):
        """Update with falling snow"""
        super().update(speed)

        # Update snowflakes
        for flake in self.snowflakes:
            flake['y'] += flake['speed']
            if flake['y'] > SCREEN_HEIGHT:
                flake['y'] = -10
                flake['x'] = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        """Draw ice - FAST VERSION"""
        # Blit pre-made sky
        screen.blit(self.sky_surface, (0, 0))

        # Ice crystals (simplified)
        for crystal in self.crystals:
            x = int((crystal['x'] - self.scroll_offset * 0.5 + crystal['offset']) % (SCREEN_WIDTH + 100))
            y = crystal['y']
            size = crystal['size']

            crystal_color = (200, 230, 255)
            points = [
                (x, y - size),
                (x + size // 2, y),
                (x, y + size),
                (x - size // 2, y)
            ]
            pygame.draw.polygon(screen, crystal_color, points)

        # Blit pre-made ground
        screen.blit(self.ground_surface, (0, GROUND_LEVEL))

        # Fewer ice shines
        for i in range(5):  # Was 10, now 5
            shine_x = int((i * 160 + self.scroll_offset) % SCREEN_WIDTH)
            pygame.draw.line(screen, (255, 255, 255),
                             (shine_x, GROUND_LEVEL + 10),
                             (shine_x + 20, GROUND_LEVEL + 15), 2)

        # Ground line
        pygame.draw.line(screen, (200, 220, 240), (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)

        # Snowflakes
        for flake in self.snowflakes:
            pygame.draw.circle(screen, WHITE, (int(flake['x']), int(flake['y'])), flake['size'])


class FutureBackground(Background):
    """Optimised futuristic city"""

    def __init__(self):
        # Define attributes BEFORE calling super().__init__()
        self.ground_color = (80, 80, 100)

        super().__init__("future")

        # Fewer buildings
        self.buildings = []
        for i in range(5):  # Was 8, now 5
            self.buildings.append({
                'x': i * 200,
                'width': random.randint(60, 100),
                'height': random.randint(150, 250),
                'windows': random.randint(3, 6)
            })

        # Fewer stars
        self.stars = []
        for i in range(30):  # Was 50, now 30
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, GROUND_LEVEL - 100),
                'brightness': random.randint(155, 255)
            })

    def create_static_elements(self):
        """Pre-render sky and ground"""
        sky_color_top = (20, 20, 40)
        sky_color_bottom = (60, 40, 80)

        for y in range(GROUND_LEVEL):
            ratio = y / GROUND_LEVEL
            color = (
                int(sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * ratio),
                int(sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * ratio),
                int(sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (SCREEN_WIDTH, y))

        self.ground_surface.fill(self.ground_color)

    def draw(self, screen):
        """Draw future - FAST VERSION"""
        # Blit pre-made sky
        screen.blit(self.sky_surface, (0, 0))

        # Stars (static, no twinkling for performance)
        for star in self.stars:
            pygame.draw.circle(screen, (star['brightness'], star['brightness'], 200),
                               (star['x'], star['y']), 2)

        # Buildings (simplified)
        for building in self.buildings:
            x = int((building['x'] - self.scroll_offset * 0.3) % (SCREEN_WIDTH + 200))
            w = building['width']
            h = building['height']

            # Building body
            pygame.draw.rect(screen, (60, 60, 80), (x, GROUND_LEVEL - h, w, h))

            # Fewer windows
            for row in range(building['windows']):
                for col in range(2):  # Was 3, now 2
                    wx = x + 15 + col * 30
                    wy = GROUND_LEVEL - h + 20 + row * 35

                    window_color = (255, 255, 100) if random.random() > 0.5 else (50, 50, 70)
                    pygame.draw.rect(screen, window_color, (wx, wy, 12, 18))

        # Blit pre-made ground
        screen.blit(self.ground_surface, (0, GROUND_LEVEL))

        # Fewer neon grid lines
        for i in range(10):  # Was 20, now 10
            line_x = int((i * 80 + self.scroll_offset * 2) % SCREEN_WIDTH)
            pygame.draw.line(screen, (0, 255, 255),
                             (line_x, GROUND_LEVEL),
                             (line_x - 10, GROUND_LEVEL + 30), 1)

        # Ground line with glow
        pygame.draw.line(screen, (0, 255, 255), (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)


class NightBackground(Background):
    """Optimised night environment"""

    def __init__(self):
        # Define attributes BEFORE calling super().__init__()
        self.ground_color = (40, 40, 60)
        self.moon_position = (SCREEN_WIDTH - 150, 100)

        super().__init__("night")

        # Fewer stars
        self.stars = []
        for i in range(50):  # Was 100, now 50
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, GROUND_LEVEL),
                'size': random.randint(1, 3),
                'brightness': random.randint(155, 255)
            })

        # Fewer trees
        self.trees = []
        for i in range(5):  # Was 8, now 5
            self.trees.append({
                'x': i * 160,
                'height': random.randint(60, 100),
                'offset': random.randint(0, 100)
            })

    def create_static_elements(self):
        """Pre-render sky and ground"""
        sky_color_top = (10, 10, 30)
        sky_color_bottom = (30, 20, 50)

        for y in range(GROUND_LEVEL):
            ratio = y / GROUND_LEVEL
            color = (
                int(sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * ratio),
                int(sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * ratio),
                int(sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * ratio)
            )
            pygame.draw.line(self.sky_surface, color, (0, y), (SCREEN_WIDTH, y))

        self.ground_surface.fill(self.ground_color)

    def draw(self, screen):
        """Draw night - FAST VERSION"""
        # Blit pre-made sky
        screen.blit(self.sky_surface, (0, 0))

        # Moon
        pygame.draw.circle(screen, (240, 240, 200), self.moon_position, 35)
        pygame.draw.circle(screen, (200, 200, 160),
                           (self.moon_position[0] - 10, self.moon_position[1] - 5), 8)

        # Stars (static)
        for star in self.stars:
            pygame.draw.circle(screen, (star['brightness'], star['brightness'], star['brightness'] + 50),
                               (star['x'], star['y']), star['size'])

        # Tree silhouettes
        for tree in self.trees:
            x = int((tree['x'] - self.scroll_offset * 0.5 + tree['offset']) % (SCREEN_WIDTH + 100))
            h = tree['height']

            tree_color = (20, 20, 40)
            pygame.draw.rect(screen, tree_color, (x, GROUND_LEVEL - h, 12, h))

            # Simple triangle top
            points = [
                (x - 15, GROUND_LEVEL - h),
                (x + 6, GROUND_LEVEL - h - 30),
                (x + 27, GROUND_LEVEL - h)
            ]
            pygame.draw.polygon(screen, tree_color, points)

        # Blit pre-made ground
        screen.blit(self.ground_surface, (0, GROUND_LEVEL))

        # Ground line
        pygame.draw.line(screen, (60, 60, 80), (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)


class BackgroundManager:
    """Manages backgrounds for different levels"""

    def __init__(self):
        self.backgrounds = {
            "desert": DesertBackground(),
            "jungle": JungleBackground(),
            "ice": IceBackground(),
            "future": FutureBackground(),
            "night": NightBackground()
        }
        self.current_background = self.backgrounds["desert"]

    def set_environment(self, environment_type):
        """Change environment"""
        if environment_type in self.backgrounds:
            self.current_background = self.backgrounds[environment_type]

    def set_level_environment(self, level):
        """Set environment based on level"""
        if level <= 2:
            self.set_environment("desert")
        elif level <= 4:
            self.set_environment("jungle")
        elif level <= 6:
            self.set_environment("ice")
        else:
            self.set_environment("future")

    def update(self, speed=5):
        """Update current background"""
        self.current_background.update(speed)

    def draw(self, screen):
        """Draw current background"""
        self.current_background.draw(screen)