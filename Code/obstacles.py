import pygame
import random
from settings import *


class Obstacle:
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.obstacle_type = obstacle_type
        self.speed = 5
        self.animation_frame = 0
        self.animation_timer = 0

        if obstacle_type == "cactus":
            self.width = 30
            self.height = 50
            self.y = GROUND_LEVEL
        elif obstacle_type == "large_cactus":
            self.width = 35
            self.height = 70
            self.y = GROUND_LEVEL
        elif obstacle_type == "double_cactus":
            self.width = 60
            self.height = 50
            self.y = GROUND_LEVEL
        elif obstacle_type == "bird":
            self.width = 40
            self.height = 30
            self.y = GROUND_LEVEL - 80
        elif obstacle_type == "high_bird":
            self.width = 40
            self.height = 30
            self.y = GROUND_LEVEL - 120
        elif obstacle_type == "low_bird":
            self.width = 40
            self.height = 30
            self.y = GROUND_LEVEL - 40
        elif obstacle_type == "boulder":
            self.width = 45
            self.height = 45
            self.y = GROUND_LEVEL - 45
            self.rotation = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

        self.animation_timer += 1
        if self.animation_timer > 8:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

        if self.obstacle_type == "boulder":
            self.rotation = (self.rotation + 5) % 360

    def draw(self, screen):
        if "cactus" in self.obstacle_type:
            self.draw_cactus(screen)
        elif "bird" in self.obstacle_type:
            self.draw_bird(screen)
        elif self.obstacle_type == "boulder":
            self.draw_boulder(screen)

    def draw_cactus(self, screen):
        if self.obstacle_type == "large_cactus":
            self.draw_large_cactus(screen)
        elif self.obstacle_type == "double_cactus":
            self.draw_double_cactus(screen)
        else:
            self.draw_normal_cactus(screen)

    def draw_normal_cactus(self, screen):
        main_body = pygame.Rect(self.x + 10, self.y, 10, self.height)
        pygame.draw.rect(screen, DARK_GREEN, main_body, border_radius=3)

        left_arm = pygame.Rect(self.x, self.y + 15, 10, 15)
        pygame.draw.rect(screen, DARK_GREEN, left_arm, border_radius=3)
        pygame.draw.rect(screen, DARK_GREEN,
                         (self.x + 5, self.y + 10, 5, 10), border_radius=2)

        right_arm = pygame.Rect(self.x + 20, self.y + 20, 10, 12)
        pygame.draw.rect(screen, DARK_GREEN, right_arm, border_radius=3)
        pygame.draw.rect(screen, DARK_GREEN,
                         (self.x + 20, self.y + 15, 5, 10), border_radius=2)

        for i in range(0, self.height, 8):
            spike_y = self.y + i
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 12, spike_y), (self.x + 10, spike_y + 3), 2)
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 17, spike_y + 2), (self.x + 19, spike_y + 5), 2)

        pygame.draw.rect(screen, BLACK, main_body, 2, border_radius=3)
        pygame.draw.rect(screen, BLACK, left_arm, 1, border_radius=3)
        pygame.draw.rect(screen, BLACK, right_arm, 1, border_radius=3)

    def draw_large_cactus(self, screen):
        main_body = pygame.Rect(self.x + 10, self.y, 15, self.height)
        pygame.draw.rect(screen, DARK_GREEN, main_body, border_radius=4)

        left_arm1 = pygame.Rect(self.x, self.y + 20, 12, 20)
        pygame.draw.rect(screen, DARK_GREEN, left_arm1, border_radius=3)
        pygame.draw.rect(screen, DARK_GREEN,
                         (self.x + 5, self.y + 15, 7, 12), border_radius=2)

        left_arm2 = pygame.Rect(self.x + 2, self.y + 35, 10, 15)
        pygame.draw.rect(screen, DARK_GREEN, left_arm2, border_radius=3)

        right_arm = pygame.Rect(self.x + 25, self.y + 25, 12, 18)
        pygame.draw.rect(screen, DARK_GREEN, right_arm, border_radius=3)
        pygame.draw.rect(screen, DARK_GREEN,
                         (self.x + 25, self.y + 20, 7, 12), border_radius=2)

        for i in range(0, self.height, 6):
            spike_y = self.y + i
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 14, spike_y), (self.x + 12, spike_y + 3), 2)
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 20, spike_y + 2), (self.x + 22, spike_y + 5), 2)

        pygame.draw.rect(screen, BLACK, main_body, 2, border_radius=4)
        pygame.draw.rect(screen, BLACK, left_arm1, 1, border_radius=3)
        pygame.draw.rect(screen, BLACK, right_arm, 1, border_radius=3)

    def draw_double_cactus(self, screen):
        body1 = pygame.Rect(self.x + 5, self.y, 10, self.height)
        pygame.draw.rect(screen, DARK_GREEN, body1, border_radius=3)

        arm1 = pygame.Rect(self.x, self.y + 15, 8, 12)
        pygame.draw.rect(screen, DARK_GREEN, arm1, border_radius=2)

        for i in range(0, self.height, 8):
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 8, self.y + i), (self.x + 6, self.y + i + 3), 2)

        pygame.draw.rect(screen, BLACK, body1, 2, border_radius=3)
        pygame.draw.rect(screen, BLACK, arm1, 1, border_radius=2)

        body2 = pygame.Rect(self.x + 35, self.y + 5, 10, self.height - 5)
        pygame.draw.rect(screen, DARK_GREEN, body2, border_radius=3)

        arm2 = pygame.Rect(self.x + 45, self.y + 20, 8, 12)
        pygame.draw.rect(screen, DARK_GREEN, arm2, border_radius=2)

        for i in range(0, self.height - 5, 8):
            pygame.draw.line(screen, (0, 80, 0),
                             (self.x + 38, self.y + 5 + i), (self.x + 36, self.y + 8 + i), 2)

        pygame.draw.rect(screen, BLACK, body2, 2, border_radius=3)
        pygame.draw.rect(screen, BLACK, arm2, 1, border_radius=2)

    def draw_bird(self, screen):
        wing_offset = 5 if self.animation_frame == 0 else -5

        body_center_x = self.x + self.width // 2
        body_center_y = self.y + self.height // 2

        pygame.draw.ellipse(screen, BROWN,
                            (self.x + 10, self.y + 5, 20, 20))

        head_x = self.x + 25
        head_y = self.y + 8
        pygame.draw.circle(screen, BROWN, (head_x, head_y), 8)

        beak_points = [
            (head_x + 8, head_y),
            (head_x + 14, head_y - 2),
            (head_x + 14, head_y + 2)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)

        pygame.draw.circle(screen, WHITE, (head_x + 2, head_y - 2), 3)
        pygame.draw.circle(screen, BLACK, (head_x + 2, head_y - 2), 1)

        left_wing_points = [
            (body_center_x - 5, body_center_y),
            (body_center_x - 15, body_center_y + wing_offset),
            (body_center_x - 10, body_center_y + 5)
        ]
        pygame.draw.polygon(screen, (101, 67, 33), left_wing_points)
        pygame.draw.polygon(screen, BLACK, left_wing_points, 1)

        right_wing_points = [
            (body_center_x + 5, body_center_y),
            (body_center_x + 15, body_center_y + wing_offset),
            (body_center_x + 10, body_center_y + 5)
        ]
        pygame.draw.polygon(screen, (101, 67, 33), right_wing_points)
        pygame.draw.polygon(screen, BLACK, right_wing_points, 1)

        tail_points = [
            (self.x + 5, body_center_y),
            (self.x - 5, body_center_y - 5),
            (self.x - 5, body_center_y + 5)
        ]
        pygame.draw.polygon(screen, (101, 67, 33), tail_points)

        pygame.draw.ellipse(screen, BLACK, (self.x + 10, self.y + 5, 20, 20), 2)
        pygame.draw.circle(screen, BLACK, (head_x, head_y), 8, 2)

    def draw_boulder(self, screen):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        pygame.draw.circle(screen, (105, 105, 105), (int(center_x), int(center_y)),
                           self.width // 2)

        import math
        num_marks = 6
        for i in range(num_marks):
            angle = math.radians(self.rotation + (360 / num_marks) * i)
            mark_distance = self.width // 3
            mark_x = center_x + math.cos(angle) * mark_distance
            mark_y = center_y + math.sin(angle) * mark_distance
            pygame.draw.circle(screen, (75, 75, 75), (int(mark_x), int(mark_y)), 4)

        crack_points = [
            (center_x - 8, center_y - 10),
            (center_x - 3, center_y - 5),
            (center_x - 8, center_y + 2)
        ]
        pygame.draw.lines(screen, (60, 60, 60), False,
                          [(int(p[0]), int(p[1])) for p in crack_points], 2)

        pygame.draw.circle(screen, (140, 140, 140),
                           (int(center_x - 8), int(center_y - 8)), 8)

        pygame.draw.circle(screen, BLACK, (int(center_x), int(center_y)),
                           self.width // 2, 3)

    def is_off_screen(self):
        return self.x < -self.width


class ObstacleSpawner:
    def __init__(self):
        self.obstacle_types = {
            1: ["cactus", "bird"],
            2: ["cactus", "bird", "large_cactus", "high_bird"],
            3: ["cactus", "bird", "large_cactus", "double_cactus", "high_bird", "low_bird"],
            4: ["cactus", "bird", "large_cactus", "double_cactus", "high_bird", "low_bird", "boulder"]
        }
        self.last_obstacle_type = None

    def get_obstacle_types_for_level(self, level):
        if level >= 4:
            return self.obstacle_types[4]
        elif level == 3:
            return self.obstacle_types[3]
        elif level == 2:
            return self.obstacle_types[2]
        else:
            return self.obstacle_types[1]

    def spawn(self, level):
        available_types = self.get_obstacle_types_for_level(level)

        possible_types = [t for t in available_types if t != self.last_obstacle_type]
        if not possible_types:
            possible_types = available_types

        obstacle_type = random.choice(possible_types)
        self.last_obstacle_type = obstacle_type

        return Obstacle(SCREEN_WIDTH, 0, obstacle_type)