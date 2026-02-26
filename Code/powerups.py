import pygame
import random
from settings import *
class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.speed = 5
        self.animation_frame = 0
        self.animation_timer = 0

        self.width = 35
        self.height = 35

        if powerup_type == "shield":
            self.colour = (100, 149, 237)
            self.duration = 300
        elif powerup_type == "speed":
            self.colour = (255, 215, 0)
            self.duration = 180
        elif powerup_type == "double_jump":
            self.colour = (147, 112, 219)
            self.duration = 240
        elif powerup_type == "coin_magnet":
            self.colour = (255, 105, 180)
            self.duration = 360

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.float_offset = 0
        self.float_direction = 1

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

        self.animation_timer += 1
        if self.animation_timer % 3 == 0:
            self.float_offset += self.float_direction
            if abs(self.float_offset) > 10:
                self.float_direction *= -1

        self.rect.y = self.y + self.float_offset

        self.animation_frame = (self.animation_frame + 1) % 360

    def draw(self, screen):
        current_y = self.y + self.float_offset

        if self.powerup_type == "shield":
            self.draw_shield(screen, current_y)
        elif self.powerup_type == "speed":
            self.draw_speed(screen, current_y)
        elif self.powerup_type == "double_jump":
            self.draw_double_jump(screen, current_y)
        elif self.powerup_type == "coin_magnet":
            self.draw_coin_magnet(screen, current_y)

        pulse = abs((self.animation_frame % 60) - 30) / 30.0
        glow_radius = int(20 + pulse * 5)
        glow_colour = tuple(min(c + 50, 255) for c in self.colour)
        pygame.draw.circle(screen, glow_colour,
                           (int(self.x + self.width // 2), int(current_y + self.height // 2)),
                           glow_radius, 2)

    def draw_shield(self, screen, y):
        center_x = self.x + self.width // 2
        center_y = int(y + self.height // 2)

        shield_points = [
            (center_x, center_y - 15),
            (center_x + 12, center_y - 5),
            (center_x + 8, center_y + 15),
            (center_x - 8, center_y + 15),
            (center_x - 12, center_y - 5)
        ]
        pygame.draw.polygon(screen, self.colour, shield_points)
        pygame.draw.polygon(screen, WHITE, shield_points, 3)

        pygame.draw.line(screen, WHITE,
                         (center_x, center_y - 10),
                         (center_x, center_y + 10), 3)
        pygame.draw.line(screen, WHITE,
                         (center_x - 8, center_y),
                         (center_x + 8, center_y), 3)

    def draw_speed(self, screen, y):
        center_x = self.x + self.width // 2
        center_y = int(y + self.height // 2)

        pygame.draw.circle(screen, self.colour, (center_x, center_y), 16)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), 16, 2)

        bolt_points = [
            (center_x - 3, center_y - 12),
            (center_x + 2, center_y - 2),
            (center_x - 2, center_y + 2),
            (center_x + 5, center_y + 12),
            (center_x + 2, center_y + 2),
            (center_x + 8, center_y - 5),
            (center_x + 3, center_y - 2)
        ]
        pygame.draw.polygon(screen, WHITE, bolt_points)

        for i in range(3):
            offset = i * 5
            pygame.draw.line(screen, WHITE,
                             (center_x + 12, center_y - 8 + offset),
                             (center_x + 18, center_y - 8 + offset), 2)

    def draw_double_jump(self, screen, y):
        center_x = self.x + self.width // 2
        center_y = int(y + self.height // 2)

        pygame.draw.circle(screen, self.colour, (center_x, center_y), 16)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), 16, 2)

        arrow1_points = [
            (center_x, center_y - 10),
            (center_x - 6, center_y - 4),
            (center_x - 3, center_y - 4),
            (center_x - 3, center_y + 2),
            (center_x + 3, center_y + 2),
            (center_x + 3, center_y - 4),
            (center_x + 6, center_y - 4)
        ]
        pygame.draw.polygon(screen, WHITE, arrow1_points)

        arrow2_points = [
            (center_x, center_y + 2),
            (center_x - 6, center_y + 8),
            (center_x - 3, center_y + 8),
            (center_x - 3, center_y + 14),
            (center_x + 3, center_y + 14),
            (center_x + 3, center_y + 8),
            (center_x + 6, center_y + 8)
        ]
        pygame.draw.polygon(screen, WHITE, arrow2_points)

    def draw_coin_magnet(self, screen, y):
        center_x = self.x + self.width // 2
        center_y = int(y + self.height // 2)

        pygame.draw.circle(screen, self.colour, (center_x, center_y), 16)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), 16, 2)

        pygame.draw.rect(screen, (220, 20, 60),
                         (center_x - 10, center_y - 8, 6, 16))
        pygame.draw.rect(screen, (220, 20, 60),
                         (center_x + 4, center_y - 8, 6, 16))
        pygame.draw.rect(screen, (220, 20, 60),
                         (center_x - 10, center_y + 8, 20, 4))

        sparkle_positions = [
            (center_x - 14, center_y - 10),
            (center_x + 14, center_y - 10),
            (center_x - 14, center_y + 4),
            (center_x + 14, center_y + 4)
        ]
        for pos in sparkle_positions:
            if (self.animation_frame // 10) % 4 == sparkle_positions.index(pos):
                pygame.draw.circle(screen, (255, 255, 100), pos, 2)

    def is_off_screen(self):
        return self.x < -self.width


class PowerUpManager:
    def __init__(self):
        self.active_powerups = {
            'shield': {'active': False, 'timer': 0},
            'speed': {'active': False, 'timer': 0},
            'double_jump': {'active': False, 'timer': 0, 'jumps_left': 0},
            'coin_magnet': {'active': False, 'timer': 0}
        }

    def activate(self, powerup_type, duration):
        if powerup_type in self.active_powerups:
            self.active_powerups[powerup_type]['active'] = True
            self.active_powerups[powerup_type]['timer'] = duration

            if powerup_type == 'double_jump':
                self.active_powerups[powerup_type]['jumps_left'] = 2

    def update(self):
        for powerup_type, data in self.active_powerups.items():
            if data['active']:
                data['timer'] -= 1
                if data['timer'] <= 0:
                    data['active'] = False
                    if powerup_type == 'double_jump':
                        data['jumps_left'] = 0

    def is_active(self, powerup_type):
        return self.active_powerups.get(powerup_type, {}).get('active', False)

    def get_timer(self, powerup_type):
        return self.active_powerups.get(powerup_type, {}).get('timer', 0)

    def use_double_jump(self):
        if self.is_active('double_jump') and self.active_powerups['double_jump']['jumps_left'] > 0:
            self.active_powerups['double_jump']['jumps_left'] -= 1
            return True
        return False

    def has_jumps_left(self):
        return self.active_powerups['double_jump'].get('jumps_left', 0) > 0

    def deactivate(self, powerup_type):
        if powerup_type in self.active_powerups:
            self.active_powerups[powerup_type]['active'] = False
            self.active_powerups[powerup_type]['timer'] = 0

    def draw_indicators(self, screen, x, y):
        offset_y = 0
        font = pygame.font.Font(None, 24)

        for powerup_type, data in self.active_powerups.items():
            if data['active']:
                box_width = 150
                box_height = 30
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x, y + offset_y, box_width, box_height),
                                 border_radius=5)
                pygame.draw.rect(screen, WHITE,
                                 (x, y + offset_y, box_width, box_height), 2,
                                 border_radius=5)

                name_text = powerup_type.replace('_', ' ').title()
                text_surface = font.render(name_text, True, WHITE)
                screen.blit(text_surface, (x + 5, y + offset_y + 5))

                time_remaining = data['timer'] / 60.0
                bar_width = 40
                bar_height = 8
                bar_x = x + box_width - bar_width - 5
                bar_y = y + offset_y + 11

                pygame.draw.rect(screen, GRAY,
                                 (bar_x, bar_y, bar_width, bar_height))

                timer_percent = data['timer'] / (5 * 60)
                if timer_percent > 0.5:
                    bar_colour = GREEN
                elif timer_percent > 0.25:
                    bar_colour = (255, 165, 0)
                else:
                    bar_colour = RED

                filled_width = int(bar_width * min(timer_percent, 1.0))
                pygame.draw.rect(screen, bar_colour,
                                 (bar_x, bar_y, filled_width, bar_height))

                offset_y += 35