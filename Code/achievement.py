import pygame
import time

class Achievement:
    def __init__(self, title, requirement_type, target):
        self.title = title
        self.requirement_type = requirement_type
        self.target = target
        self.unlocked = False

class AchievementManager:
    def __init__(self):
        self.achievements = [
            Achievement("Travel 1000m", "distance", 1000),
            Achievement("Collect 50 coins", "coins_total", 50),
            Achievement("Score 500 points", "score", 500),
        ]
        self.notification = None
        self.notification_time = 0

    def update_progress(self, r_type, value):
        for ach in self.achievements:
            if ach.requirement_type == r_type and not ach.unlocked:
                if value >= ach.target:
                    ach.unlocked = True
                    self.show_notification(ach.title)

    def show_notification(self, text):
        self.notification = text
        self.notification_time = time.time()

    def draw_notification(self, screen):
        if self.notification and time.time() - self.notification_time < 3:
            font = pygame.font.Font(None, 40)
            render = font.render(f"Achievement Unlocked: {self.notification}", True, (255, 215, 0))
            screen.blit(render, (50, 50))
        else:
            self.notification = None

    def save_data(self):
        return {"unlocked": [ach.unlocked for ach in self.achievements]}

    def load_data(self, data):
        if "unlocked" in data:
            for i, unlocked in enumerate(data["unlocked"]):
                self.achievements[i].unlocked = unlocked

    def get_unlocked_achievements(self):
        return [ach for ach in self.achievements if ach.unlocked]


class AchievementDisplay:
    def __init__(self, manager):
        self.manager = manager

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        y = 100
        for ach in self.manager.achievements:
            color = (0, 200, 0) if ach.unlocked else (150, 150, 150)
            text = font.render(ach.title, True, color)
            screen.blit(text, (100, y))
            y += 40
