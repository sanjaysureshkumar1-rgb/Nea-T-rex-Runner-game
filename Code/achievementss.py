import pygame
from settings import *


class Achievement:
    """Represents a single achievement"""

    def __init__(self, id, name, description, requirement_type, requirement_value, reward_coins):
        self.id = id
        self.name = name
        self.description = description
        self.requirement_type = requirement_type  # "distance", "score", "coins_total", "coins_game", "time", "level", "powerups_game"
        self.requirement_value = requirement_value
        self.reward_coins = reward_coins
        self.unlocked = False
        self.progress = 0
        self.unlock_time = 0


class AchievementManager:
    """Manages all achievements and tracks progress"""

    def __init__(self):
        self.achievements = self._create_achievements()
        self.notification_queue = []
        self.current_notification = None
        self.notification_timer = 0

    def _create_achievements(self):
        """Create all achievements"""
        achievements = {
            "first_steps": Achievement(
                "first_steps",
                "First Steps",
                "Travel 500 distance",
                "distance",
                500,
                50
            ),
            "marathon_runner": Achievement(
                "marathon_runner",
                "Marathon Runner",
                "Travel 5000 distance",
                "distance",
                5000,
                200
            ),
            "coin_collector": Achievement(
                "coin_collector",
                "Coin Collector",
                "Collect 100 total coins",
                "coins_total",
                100,
                100
            ),
            "treasure_hunter": Achievement(
                "treasure_hunter",
                "Treasure Hunter",
                "Collect 500 total coins",
                "coins_total",
                500,
                300
            ),
            "high_scorer": Achievement(
                "high_scorer",
                "High Scorer",
                "Score 1000 points in one game",
                "score",
                1000,
                150
            ),
            "master_player": Achievement(
                "master_player",
                "Master Player",
                "Score 5000 points in one game",
                "score",
                5000,
                500
            ),
            "survivor": Achievement(
                "survivor",
                "Survivor",
                "Survive for 3 minutes",
                "time",
                10800,  # 3 minutes at 60 FPS
                200
            ),
            "endurance_king": Achievement(
                "endurance_king",
                "Endurance King",
                "Survive for 10 minutes",
                "time",
                36000,  # 10 minutes at 60 FPS
                500
            ),
            "level_master": Achievement(
                "level_master",
                "Level Master",
                "Reach level 5",
                "level",
                5,
                100
            ),
            "coin_rush": Achievement(
                "coin_rush",
                "Coin Rush",
                "Collect 30 coins in one game",
                "coins_game",
                30,
                150
            ),
            "powerup_fan": Achievement(
                "powerup_fan",
                "Power-up Fan",
                "Collect 10 power-ups in one game",
                "powerups_game",
                10,
                100
            )
        }
        return achievements

    def update_progress(self, requirement_type, value):
        """Update progress for achievements of a given type"""
        for achievement in self.achievements.values():
            if achievement.requirement_type == requirement_type and not achievement.unlocked:
                achievement.progress = value

                # Check if unlocked
                if achievement.progress >= achievement.requirement_value:
                    self.unlock_achievement(achievement.id)

    def unlock_achievement(self, achievement_id):
        """Unlock an achievement"""
        achievement = self.achievements.get(achievement_id)
        if achievement and not achievement.unlocked:
            achievement.unlocked = True
            achievement.unlock_time = pygame.time.get_ticks()

            # Add to notification queue
            self.notification_queue.append(achievement)

            return achievement.reward_coins
        return 0

    def update_notifications(self):
        """Update achievement notifications"""
        # Start new notification if none active
        if self.current_notification is None and len(self.notification_queue) > 0:
            self.current_notification = self.notification_queue.pop(0)
            self.notification_timer = 180  # 3 seconds at 60 FPS

        # Update timer
        if self.current_notification is not None:
            self.notification_timer -= 1
            if self.notification_timer <= 0:
                self.current_notification = None

    def draw_notification(self, screen):
        """Draw achievement notification"""
        self.update_notifications()

        if self.current_notification is None:
            return

        # Notification box
        box_width = 400
        box_height = 100
        box_x = SCREEN_WIDTH - box_width - 20
        box_y = 20

        # Slide in animation
        if self.notification_timer > 150:
            offset = (180 - self.notification_timer) * 20
            box_x = SCREEN_WIDTH - offset
        elif self.notification_timer < 30:
            offset = (30 - self.notification_timer) * 20
            box_x = SCREEN_WIDTH - box_width - 20 + offset

        # Shadow
        shadow_rect = pygame.Rect(box_x + 5, box_y + 5, box_width, box_height)
        shadow_surface = pygame.Surface((box_width, box_height))
        shadow_surface.set_alpha(100)
        shadow_surface.fill(BLACK)
        screen.blit(shadow_surface, shadow_rect)

        # Background
        pygame.draw.rect(screen, (50, 50, 50),
                         (box_x, box_y, box_width, box_height),
                         border_radius=10)
        pygame.draw.rect(screen, GOLD,
                         (box_x, box_y, box_width, box_height),
                         3, border_radius=10)

        # Title
        title_font = pygame.font.Font(None, 28)
        title_text = title_font.render("ACHIEVEMENT UNLOCKED!", True, GOLD)
        screen.blit(title_text, (box_x + box_width // 2 - title_text.get_width() // 2, box_y + 15))

        # Achievement name
        name_font = pygame.font.Font(None, 32)
        name_text = name_font.render(self.current_notification.name, True, WHITE)
        screen.blit(name_text, (box_x + box_width // 2 - name_text.get_width() // 2, box_y + 45))

        # Reward
        reward_font = pygame.font.Font(None, 24)
        reward_text = reward_font.render(f"+{self.current_notification.reward_coins} coins", True, GOLD)
        screen.blit(reward_text, (box_x + box_width // 2 - reward_text.get_width() // 2, box_y + 75))

    def get_unlocked_achievements(self):
        """Get list of unlocked achievements"""
        return [ach for ach in self.achievements.values() if ach.unlocked]

    def get_total_coins_earned(self):
        """Get total coins from achievements"""
        return sum(ach.reward_coins for ach in self.achievements.values() if ach.unlocked)

    def save_data(self):
        """Save achievement data"""
        return {
            "achievements": {
                ach_id: {
                    "unlocked": ach.unlocked,
                    "progress": ach.progress
                }
                for ach_id, ach in self.achievements.items()
            }
        }

    def load_data(self, data):
        """Load achievement data"""
        if "achievements" in data:
            for ach_id, ach_data in data["achievements"].items():
                if ach_id in self.achievements:
                    self.achievements[ach_id].unlocked = ach_data.get("unlocked", False)
                    self.achievements[ach_id].progress = ach_data.get("progress", 0)


class AchievementDisplay:
    """Displays achievement list screen"""

    def __init__(self, achievement_manager):
        self.achievement_manager = achievement_manager
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 30

    def handle_scroll(self, scroll_y):
        """Handle mouse wheel scrolling"""
        self.scroll_offset -= scroll_y * self.scroll_speed
        # Clamp scroll to valid range
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    def draw(self, screen):
        """Draw achievements screen"""
        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("ACHIEVEMENTS", True, WHITE)
        title_shadow = title_font.render("ACHIEVEMENTS", True, TEXT_SHADOW)
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 53))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Stats
        stats_font = pygame.font.Font(None, 32)
        unlocked_count = len(self.achievement_manager.get_unlocked_achievements())
        total_count = len(self.achievement_manager.achievements)
        stats_text = stats_font.render(
            f"Unlocked: {unlocked_count}/{total_count}",
            True, WHITE
        )
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 120))

        coins_text = stats_font.render(
            f"Coins Earned: {self.achievement_manager.get_total_coins_earned()}",
            True, GOLD
        )
        screen.blit(coins_text, (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, 155))

        # Calculate max scroll
        achievement_count = len(self.achievement_manager.achievements)
        total_content_height = achievement_count * 110
        visible_area_start = 200
        visible_area_height = screen.get_height() - visible_area_start - 20
        self.max_scroll = max(0, total_content_height - visible_area_height)

        # Draw achievements with scroll offset
        y_pos = 200 - self.scroll_offset
        for achievement in self.achievement_manager.achievements.values():
            # Only draw if visible
            if -110 < y_pos < screen.get_height():
                self._draw_achievement_card(screen, achievement, y_pos)
            y_pos += 110

        # Scroll indicator
        if self.max_scroll > 0:
            indicator_font = pygame.font.Font(None, 24)
            if self.scroll_offset < self.max_scroll:
                scroll_text = indicator_font.render("↓ Scroll for more ↓", True, WHITE)
                screen.blit(scroll_text, (SCREEN_WIDTH // 2 - scroll_text.get_width() // 2,
                                          screen.get_height() - 30))

    def _draw_achievement_card(self, screen, achievement, y):
        """Draw individual achievement card"""
        x = 50
        width = SCREEN_WIDTH - 100
        height = 100

        # Colour based on unlock status
        if achievement.unlocked:
            bg_colour = (40, 100, 40)  # Dark green
            border_colour = GOLD
        else:
            bg_colour = (50, 50, 50)
            border_colour = GRAY

        # Shadow
        shadow_rect = pygame.Rect(x + 4, y + 4, width, height)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=10)

        # Background
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, bg_colour, card_rect, border_radius=10)
        pygame.draw.rect(screen, border_colour, card_rect, 3, border_radius=10)

        # Icon/Trophy
        icon_x = x + 30
        icon_y = y + height // 2
        if achievement.unlocked:
            # Draw trophy
            pygame.draw.rect(screen, GOLD, (icon_x - 10, icon_y - 5, 20, 10))
            pygame.draw.polygon(screen, GOLD, [
                (icon_x - 15, icon_y - 15),
                (icon_x + 15, icon_y - 15),
                (icon_x + 10, icon_y - 5),
                (icon_x - 10, icon_y - 5)
            ])
        else:
            # Draw lock
            pygame.draw.circle(screen, GRAY, (icon_x, icon_y - 5), 8, 3)
            pygame.draw.rect(screen, GRAY, (icon_x - 8, icon_y - 5, 16, 15))

        # Text
        name_font = pygame.font.Font(None, 36)
        desc_font = pygame.font.Font(None, 24)

        name_text = name_font.render(achievement.name, True, WHITE)
        screen.blit(name_text, (x + 80, y + 15))

        desc_text = desc_font.render(achievement.description, True, GRAY if not achievement.unlocked else WHITE)
        screen.blit(desc_text, (x + 80, y + 50))

        # Progress or reward
        if achievement.unlocked:
            reward_text = desc_font.render(f"✓ +{achievement.reward_coins} coins", True, GOLD)
            screen.blit(reward_text, (x + 80, y + 75))
        else:
            # Progress bar
            progress_percentage = min(1.0, achievement.progress / achievement.requirement_value)
            progress_text = desc_font.render(
                f"Progress: {int(achievement.progress)}/{achievement.requirement_value}",
                True, WHITE
            )
            screen.blit(progress_text, (x + 80, y + 75))

            # Small progress bar
            bar_x = x + width - 150
            bar_y = y + 78
            bar_width = 120
            bar_height = 10

            pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=3)

            if progress_percentage > 0:
                fill_width = int(bar_width * progress_percentage)
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height), border_radius=3)

            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1, border_radius=3)