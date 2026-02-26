import pygame
import time


class AchievementManager:
    """Manages game achievements and tracks player progress"""

    def __init__(self):
        self.achievements = {
            'first_jump': {
                'name': 'First Jump',
                'description': 'Make your first jump',
                'unlocked': False,
                'progress': 0,
                'target': 1,
                'type': 'action'
            },
            'distance_100': {
                'name': 'Century Runner',
                'description': 'Travel 100 metres',
                'unlocked': False,
                'progress': 0,
                'target': 100,
                'type': 'distance'
            },
            'distance_500': {
                'name': 'Marathon Runner',
                'description': 'Travel 500 metres',
                'unlocked': False,
                'progress': 0,
                'target': 500,
                'type': 'distance'
            },
            'distance_1000': {
                'name': 'Ultra Runner',
                'description': 'Travel 1000 metres',
                'unlocked': False,
                'progress': 0,
                'target': 1000,
                'type': 'distance'
            },
            'score_500': {
                'name': 'Scorer',
                'description': 'Score 500 points',
                'unlocked': False,
                'progress': 0,
                'target': 500,
                'type': 'score'
            },
            'score_1000': {
                'name': 'High Scorer',
                'description': 'Score 1000 points',
                'unlocked': False,
                'progress': 0,
                'target': 1000,
                'type': 'score'
            },
            'score_2000': {
                'name': 'Master Scorer',
                'description': 'Score 2000 points',
                'unlocked': False,
                'progress': 0,
                'target': 2000,
                'type': 'score'
            },
            'coins_50': {
                'name': 'Coin Collector',
                'description': 'Collect 50 coins in one game',
                'unlocked': False,
                'progress': 0,
                'target': 50,
                'type': 'coins_game'
            },
            'coins_100': {
                'name': 'Coin Master',
                'description': 'Collect 100 coins in one game',
                'unlocked': False,
                'progress': 0,
                'target': 100,
                'type': 'coins_game'
            },
            'coins_total_500': {
                'name': 'Treasure Hunter',
                'description': 'Collect 500 total coins',
                'unlocked': False,
                'progress': 0,
                'target': 500,
                'type': 'coins_total'
            },
            'level_5': {
                'name': 'Leveller',
                'description': 'Reach level 5',
                'unlocked': False,
                'progress': 0,
                'target': 5,
                'type': 'level'
            },
            'level_10': {
                'name': 'Expert',
                'description': 'Reach level 10',
                'unlocked': False,
                'progress': 0,
                'target': 10,
                'type': 'level'
            },
            'time_60': {
                'name': 'Survivor',
                'description': 'Survive for 60 seconds',
                'unlocked': False,
                'progress': 0,
                'target': 3600,  # 60 seconds * 60 FPS
                'type': 'time'
            },
            'time_180': {
                'name': 'Endurance',
                'description': 'Survive for 3 minutes',
                'unlocked': False,
                'progress': 0,
                'target': 10800,  # 180 seconds * 60 FPS
                'type': 'time'
            },
            'powerups_10': {
                'name': 'Power User',
                'description': 'Collect 10 power-ups in one game',
                'unlocked': False,
                'progress': 0,
                'target': 10,
                'type': 'powerups_game'
            }
        }

        self.notification_queue = []
        self.current_notification = None
        self.notification_timer = 0
        self.notification_duration = 180  # 3 seconds at 60 FPS

    def update_progress(self, achievement_type, value):
        """Update progress for achievements of a specific type"""
        for key, achievement in self.achievements.items():
            if achievement['type'] == achievement_type and not achievement['unlocked']:
                achievement['progress'] = value

                if achievement['progress'] >= achievement['target']:
                    self.unlock_achievement(key)

    def unlock_achievement(self, achievement_key):
        """Unlock an achievement and add it to the notification queue"""
        if achievement_key in self.achievements:
            achievement = self.achievements[achievement_key]
            if not achievement['unlocked']:
                achievement['unlocked'] = True
                self.notification_queue.append(achievement)

    def draw_notification(self, screen):
        """Draw achievement notification popup"""
        # Check if we should show a new notification
        if self.current_notification is None and len(self.notification_queue) > 0:
            self.current_notification = self.notification_queue.pop(0)
            self.notification_timer = self.notification_duration

        # Draw current notification
        if self.current_notification is not None:
            self.notification_timer -= 1

            # Calculate alpha based on timer (fade in/out)
            if self.notification_timer > self.notification_duration - 20:
                alpha = int(255 * (self.notification_duration - self.notification_timer) / 20)
            elif self.notification_timer < 20:
                alpha = int(255 * self.notification_timer / 20)
            else:
                alpha = 255

            # Create notification surface
            notification_width = 400
            notification_height = 100
            notification_x = screen.get_width() // 2 - notification_width // 2
            notification_y = 100

            # Background
            notification_surface = pygame.Surface((notification_width, notification_height))
            notification_surface.set_alpha(alpha)
            notification_surface.fill((50, 50, 50))
            pygame.draw.rect(notification_surface, (255, 215, 0),
                             (0, 0, notification_width, notification_height), 3)

            # Text
            font_title = pygame.font.Font(None, 36)
            font_desc = pygame.font.Font(None, 24)

            title_text = font_title.render("Achievement Unlocked!", True, (255, 215, 0))
            name_text = font_title.render(self.current_notification['name'], True, (255, 255, 255))
            desc_text = font_desc.render(self.current_notification['description'], True, (200, 200, 200))

            notification_surface.blit(title_text,
                                      (notification_width // 2 - title_text.get_width() // 2, 10))
            notification_surface.blit(name_text,
                                      (notification_width // 2 - name_text.get_width() // 2, 40))
            notification_surface.blit(desc_text,
                                      (notification_width // 2 - desc_text.get_width() // 2, 70))

            screen.blit(notification_surface, (notification_x, notification_y))

            # Remove notification when timer expires
            if self.notification_timer <= 0:
                self.current_notification = None

    def get_unlocked_achievements(self):
        """Return list of unlocked achievements"""
        return [ach for ach in self.achievements.values() if ach['unlocked']]

    def get_achievement_progress(self):
        """Get overall achievement progress percentage"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return (unlocked / total) * 100 if total > 0 else 0

    def save_data(self):
        """Return achievement data for saving"""
        return {
            'achievements': {
                key: {
                    'unlocked': ach['unlocked'],
                    'progress': ach['progress']
                }
                for key, ach in self.achievements.items()
            }
        }

    def load_data(self, data):
        """Load achievement data from saved file"""
        if 'achievements' in data:
            for key, saved_ach in data['achievements'].items():
                if key in self.achievements:
                    self.achievements[key]['unlocked'] = saved_ach.get('unlocked', False)
                    self.achievements[key]['progress'] = saved_ach.get('progress', 0)


class AchievementDisplay:
    """Displays the achievements screen"""

    def __init__(self, achievement_manager):
        self.achievement_manager = achievement_manager
        self.scroll_offset = 0
        self.max_scroll = 0

    def draw(self, screen):
        """Draw the achievements screen"""
        # Background
        screen.fill((230, 230, 250))

        # Title
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Achievements", True, (0, 0, 0))
        title_shadow = title_font.render("Achievements", True, (100, 100, 100))
        screen.blit(title_shadow, (screen.get_width() // 2 - title_text.get_width() // 2 + 2, 22))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Progress bar
        progress = self.achievement_manager.get_achievement_progress()
        progress_text = pygame.font.Font(None, 30).render(
            f"Progress: {len(self.achievement_manager.get_unlocked_achievements())}/{len(self.achievement_manager.achievements)} ({progress:.1f}%)",
            True, (0, 0, 0)
        )
        screen.blit(progress_text, (screen.get_width() // 2 - progress_text.get_width() // 2, 80))

        # Progress bar visual
        bar_width = 600
        bar_height = 30
        bar_x = screen.get_width() // 2 - bar_width // 2
        bar_y = 120

        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 3)
        if progress > 0:
            fill_width = int(bar_width * (progress / 100))
            pygame.draw.rect(screen, (0, 200, 0), (bar_x + 3, bar_y + 3, fill_width - 6, bar_height - 6))

        # Draw achievements in a grid
        start_y = 180
        achievement_width = 350
        achievement_height = 80
        spacing = 20
        achievements_per_row = 2

        y_pos = start_y
        x_pos = screen.get_width() // 2 - (achievement_width * achievements_per_row + spacing) // 2

        for i, (key, achievement) in enumerate(self.achievement_manager.achievements.items()):
            row = i // achievements_per_row
            col = i % achievements_per_row

            x = x_pos + col * (achievement_width + spacing)
            y = y_pos + row * (achievement_height + spacing)

            # Skip if off screen
            if y > screen.get_height():
                continue

            # Background colour based on unlock status
            if achievement['unlocked']:
                bg_colour = (50, 150, 50)
                border_colour = (0, 255, 0)
            else:
                bg_colour = (100, 100, 100)
                border_colour = (150, 150, 150)

            # Draw achievement box
            pygame.draw.rect(screen, bg_colour, (x, y, achievement_width, achievement_height))
            pygame.draw.rect(screen, border_colour, (x, y, achievement_width, achievement_height), 3)

            # Draw text
            name_font = pygame.font.Font(None, 28)
            desc_font = pygame.font.Font(None, 20)
            progress_font = pygame.font.Font(None, 18)

            name_text = name_font.render(achievement['name'], True, (255, 255, 255))
            desc_text = desc_font.render(achievement['description'], True, (220, 220, 220))

            screen.blit(name_text, (x + 10, y + 10))
            screen.blit(desc_text, (x + 10, y + 35))

            # Progress indicator
            if not achievement['unlocked']:
                progress_str = f"{achievement['progress']}/{achievement['target']}"
                progress_text = progress_font.render(progress_str, True, (200, 200, 200))
                screen.blit(progress_text, (x + 10, y + 55))