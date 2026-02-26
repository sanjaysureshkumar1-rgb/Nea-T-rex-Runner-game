import pygame
from settings import *


class StoryLevel:
    """Represents a single story mode level"""

    def __init__(self, level_num, name, description, objective_type, target, environment):
        self.level_num = level_num
        self.name = name
        self.description = description
        self.objective_type = objective_type  # "distance", "coins", "time", "score"
        self.target = target
        self.environment = environment
        self.completed = False
        self.best_score = 0
        self.stars_earned = 0  # 1-3 stars based on performance

    def check_completion(self, progress):
        """Check if objective is complete"""
        return progress >= self.target

    def calculate_stars(self, progress):
        """Calculate stars (1-3) based on performance"""
        if progress < self.target:
            return 0
        elif progress >= self.target * 1.5:
            return 3
        elif progress >= self.target * 1.25:
            return 2
        else:
            return 1


class StoryModeManager:
    """Manages the story mode progression"""

    def __init__(self):
        self.levels = self._create_levels()
        self.current_level = 1
        self.unlocked_levels = 1

    def _create_levels(self):
        """Create all story mode levels"""
        levels = {
            1: StoryLevel(
                level_num=1,
                name="Desert Dawn",
                description="Survive in the scorching desert",
                objective_type="distance",
                target=1000,
                environment="desert"
            ),
            2: StoryLevel(
                level_num=2,
                name="Jungle Rush",
                description="Collect coins in the dense jungle",
                objective_type="coins",
                target=20,
                environment="jungle"
            ),
            3: StoryLevel(
                level_num=3,
                name="Ice Age Survival",
                description="Survive the freezing conditions",
                objective_type="time",
                target=1800,  # 30 seconds at 60 FPS
                environment="ice"
            ),
            4: StoryLevel(
                level_num=4,
                name="Future City",
                description="Score high in the futuristic city",
                objective_type="score",
                target=2000,
                environment="future"
            ),
            5: StoryLevel(
                level_num=5,
                name="Master Challenge",
                description="Prove mastery across all environments",
                objective_type="distance",
                target=3000,
                environment="mixed"
            )
        }
        return levels

    def get_level(self, level_num):
        """Get a specific level"""
        return self.levels.get(level_num)

    def complete_level(self, level_num, progress):
        """Mark level as complete and unlock next"""
        level = self.levels.get(level_num)
        if level and not level.completed:
            level.completed = True
            level.stars_earned = level.calculate_stars(progress)

            # Update best score if better
            if progress > level.best_score:
                level.best_score = progress

            # Unlock next level
            if level_num < len(self.levels):
                self.unlocked_levels = max(self.unlocked_levels, level_num + 1)

            return True
        return False

    def is_level_unlocked(self, level_num):
        """Check if level is unlocked"""
        return level_num <= self.unlocked_levels

    def get_total_stars(self):
        """Get total stars earned across all levels"""
        return sum(level.stars_earned for level in self.levels.values())

    def get_completion_percentage(self):
        """Get overall completion percentage"""
        completed = sum(1 for level in self.levels.values() if level.completed)
        return (completed / len(self.levels)) * 100

    def save_data(self):
        """Save story mode progress"""
        return {
            "current_level": self.current_level,
            "unlocked_levels": self.unlocked_levels,
            "levels": {
                num: {
                    "completed": level.completed,
                    "best_score": level.best_score,
                    "stars_earned": level.stars_earned
                }
                for num, level in self.levels.items()
            }
        }

    def load_data(self, data):
        """Load story mode progress"""
        if "current_level" in data:
            self.current_level = data["current_level"]
        if "unlocked_levels" in data:
            self.unlocked_levels = data["unlocked_levels"]
        if "levels" in data:
            for num, level_data in data["levels"].items():
                num = int(num)
                if num in self.levels:
                    self.levels[num].completed = level_data.get("completed", False)
                    self.levels[num].best_score = level_data.get("best_score", 0)
                    self.levels[num].stars_earned = level_data.get("stars_earned", 0)


class StoryLevelDisplay:
    """Displays story level information during gameplay"""

    def __init__(self, level):
        self.level = level
        self.progress = 0
        self.show_tutorial = True
        self.tutorial_timer = 180  # 3 seconds

    def update(self, progress):
        """Update progress"""
        self.progress = progress

        if self.tutorial_timer > 0:
            self.tutorial_timer -= 1
        else:
            self.show_tutorial = False

    def draw(self, screen):
        """Draw level information"""
        # Draw level name and description
        title_font = pygame.font.Font(None, 36)
        desc_font = pygame.font.Font(None, 28)

        # Level name
        name_text = title_font.render(self.level.name, True, WHITE)
        name_shadow = title_font.render(self.level.name, True, TEXT_SHADOW)
        screen.blit(name_shadow, (SCREEN_WIDTH // 2 - name_text.get_width() // 2 + 2, 12))
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 10))

        # Objective
        objective_text = desc_font.render(self.level.description, True, WHITE)
        screen.blit(objective_text, (SCREEN_WIDTH // 2 - objective_text.get_width() // 2, 45))

        # Progress bar
        self._draw_progress_bar(screen)

        # Tutorial overlay (if active)
        if self.show_tutorial:
            self._draw_tutorial(screen)

    def _draw_progress_bar(self, screen):
        """Draw progress bar for objective"""
        bar_width = 300
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 80

        # Background
        pygame.draw.rect(screen, (50, 50, 50),
                         (bar_x, bar_y, bar_width, bar_height),
                         border_radius=5)

        # Progress fill
        progress_percentage = min(1.0, self.progress / self.level.target)
        fill_width = int(bar_width * progress_percentage)

        # Colour based on progress
        if progress_percentage >= 1.0:
            fill_colour = GREEN
        elif progress_percentage >= 0.75:
            fill_colour = YELLOW
        elif progress_percentage >= 0.5:
            fill_colour = ORANGE
        else:
            fill_colour = RED

        if fill_width > 0:
            pygame.draw.rect(screen, fill_colour,
                             (bar_x, bar_y, fill_width, bar_height),
                             border_radius=5)

        # Border
        pygame.draw.rect(screen, WHITE,
                         (bar_x, bar_y, bar_width, bar_height),
                         3, border_radius=5)

        # Progress text
        progress_font = pygame.font.Font(None, 24)
        progress_text = progress_font.render(
            f"{int(self.progress)}/{self.level.target}",
            True, WHITE
        )
        screen.blit(progress_text,
                    (bar_x + bar_width // 2 - progress_text.get_width() // 2,
                     bar_y + bar_height // 2 - progress_text.get_height() // 2))

    def _draw_tutorial(self, screen):
        """Draw tutorial overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, 150))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, SCREEN_HEIGHT - 150))

        # Tutorial text
        tutorial_font = pygame.font.Font(None, 28)

        tutorials = {
            "distance": "Jump and duck to avoid obstacles!",
            "coins": "Collect as many coins as you can!",
            "time": "Survive as long as possible!",
            "score": "Get the highest score you can!"
        }

        tutorial_text = tutorials.get(self.level.objective_type, "Complete the objective!")
        text_surface = tutorial_font.render(tutorial_text, True, WHITE)
        screen.blit(text_surface,
                    (SCREEN_WIDTH // 2 - text_surface.get_width() // 2,
                     SCREEN_HEIGHT - 100))

        # Controls reminder
        controls_font = pygame.font.Font(None, 24)
        controls_text = controls_font.render("SPACE/UP: Jump | DOWN: Duck | ESC: Pause", True, GRAY)
        screen.blit(controls_text,
                    (SCREEN_WIDTH // 2 - controls_text.get_width() // 2,
                     SCREEN_HEIGHT - 60))


class StoryVictoryScreen:
    """Victory screen shown when level is completed"""

    def __init__(self, level, final_progress, coins_earned):
        self.level = level
        self.final_progress = final_progress
        self.coins_earned = coins_earned
        self.stars = level.calculate_stars(final_progress)
        self.star_animation_frame = 0
        self.bonus_coins = 100 + (self.stars * 50)  # Bonus based on stars

    def update(self):
        """Update animations"""
        self.star_animation_frame += 1

    def draw(self, screen):
        """Draw victory screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Victory title
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("LEVEL COMPLETE!", True, GOLD)
        title_shadow = title_font.render("LEVEL COMPLETE!", True, TEXT_SHADOW)
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 103))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Level name
        name_font = pygame.font.Font(None, 50)
        name_text = name_font.render(self.level.name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 180))

        # Stars
        self._draw_stars(screen)

        # Stats
        self._draw_stats(screen)

        # Continue prompt
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press SPACE to continue", True, WHITE)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 520))

    def _draw_stars(self, screen):
        """Draw star rating"""
        star_size = 60
        star_spacing = 80
        start_x = SCREEN_WIDTH // 2 - star_spacing
        star_y = 260

        for i in range(3):
            x = start_x + i * star_spacing

            # Determine if this star is earned
            is_earned = i < self.stars

            # Animated scale for earned stars
            if is_earned and self.star_animation_frame < 60:
                scale = 1.0 + 0.2 * abs((self.star_animation_frame - i * 10) % 20 - 10) / 10
            else:
                scale = 1.0

            # Draw star
            colour = GOLD if is_earned else GRAY
            points = self._get_star_points(x, star_y, star_size * scale)
            pygame.draw.polygon(screen, colour, points)
            pygame.draw.polygon(screen, WHITE, points, 3)

    def _get_star_points(self, x, y, size):
        """Get points for drawing a star"""
        import math
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            radius = size if i % 2 == 0 else size / 2
            points.append((
                x + radius * math.cos(angle),
                y + radius * math.sin(angle)
            ))
        return points

    def _draw_stats(self, screen):
        """Draw statistics"""
        stats_font = pygame.font.Font(None, 32)
        y_pos = 360

        stats = [
            f"Final Score: {int(self.final_progress)}",
            f"Coins Collected: {self.coins_earned}",
            f"Star Bonus: +{self.bonus_coins} coins",
            f"Total Earned: {self.coins_earned + self.bonus_coins} coins"
        ]

        for stat in stats:
            text = stats_font.render(stat, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 40