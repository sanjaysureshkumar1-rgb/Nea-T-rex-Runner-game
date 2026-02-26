import pygame
from settings import *
from sprite_manager import SpriteSheet, AnimatedSprite


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.velocity_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = DARK_GREEN
        self.power_up_manager = None
        self.jump_count = 0
        self.max_jumps = 1

        # NEW: Sprite system
        self.sprite_sheet = SpriteSheet()
        self.animated_sprite = AnimatedSprite(self.sprite_sheet)
        self.use_sprites = True  # Toggle to switch between sprites and old drawing

        # Platform collision support
        self.platforms = []
        self.on_ground = False
        self.use_platforms = False

    def set_skin_colour(self, color):
        """Set the player's skin color"""
        self.color = color
        if self.use_sprites:
            self.animated_sprite.set_color(color)

    def set_power_up_manager(self, manager):
        """Set the power-up manager reference"""
        self.power_up_manager = manager

    def set_platforms(self, platform_list):
        """Set platforms for collision detection"""
        self.platforms = platform_list
        self.use_platforms = True

    def disable_platforms(self):
        """Disable platform mode (back to normal ground)"""
        self.use_platforms = False
        self.platforms = []

    def check_platform_collision(self):
        """Check collision with platforms"""
        self.on_ground = False

        for platform in self.platforms:
            if self.velocity_y >= 0:
                if (platform.top <= self.rect.bottom <= platform.bottom and
                        self.rect.right > platform.left + 5 and
                        self.rect.left < platform.right - 5):

                    if not self.is_ducking:
                        self.y = platform.top - self.height
                    else:
                        self.y = platform.top - 25

                    self.rect.y = self.y
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                    self.jump_count = 0
                    break

        if not self.on_ground and self.y > SCREEN_HEIGHT:
            self.x = 100
            self.y = 100
            self.velocity_y = 0

    def update(self):
        """Update player physics and position"""
        # Apply gravity
        if self.use_platforms:
            self.velocity_y += GRAVITY
            if self.velocity_y > 20:
                self.velocity_y = 20

            self.y += self.velocity_y
            self.check_platform_collision()
        else:
            if self.y < GROUND_LEVEL or self.velocity_y < 0:
                self.velocity_y += GRAVITY
                self.y += self.velocity_y

            if self.y > GROUND_LEVEL:
                self.y = GROUND_LEVEL
                self.velocity_y = 0
                self.is_jumping = False
                self.jump_count = 0

        # Update rect for collision
        if self.is_ducking:
            self.rect = pygame.Rect(self.x, self.y + 35, self.width, 25)
        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Update max jumps based on power-up
        if self.power_up_manager and self.power_up_manager.is_active('double_jump'):
            self.max_jumps = 2
        else:
            self.max_jumps = 1

        # Update sprite animation
        if self.use_sprites:
            sprite_state = 'standing'
            if self.is_ducking:
                sprite_state = 'ducking'
            elif self.is_jumping or (not self.on_ground and self.use_platforms):
                sprite_state = 'jumping'

            # Always animate (the sprite will be running)
            self.animated_sprite.update(sprite_state, is_moving=True)

    def jump(self):
        """Make the player jump"""
        can_jump = False

        if self.use_platforms:
            can_jump = (self.on_ground or self.jump_count < self.max_jumps)
        else:
            can_jump = (self.jump_count < self.max_jumps)

        if can_jump:
            jump_str = JUMP_STRENGTH
            if self.power_up_manager and self.power_up_manager.is_active('speed'):
                jump_str = JUMP_STRENGTH * 1.3

            self.velocity_y = jump_str
            self.is_jumping = True
            self.jump_count += 1

            if self.use_platforms:
                self.on_ground = False

    def duck(self):
        """Make the player duck"""
        if not self.is_jumping or self.use_platforms:
            self.is_ducking = True

    def stand_up(self):
        """Make the player stand up"""
        self.is_ducking = False

    def draw(self, screen):
        """Draw the player"""
        if self.use_sprites:
            self._draw_with_sprites(screen)
        else:
            self._draw_original(screen)

    def _draw_with_sprites(self, screen):
        """Draw using sprite system"""
        # Collect active effects
        effects = []
        if self.power_up_manager:
            if self.power_up_manager.is_active('shield'):
                effects.append('shield')
            if self.power_up_manager.is_active('speed'):
                effects.append('speed')

        # Draw the sprite
        self.animated_sprite.draw(screen, self.x, self.y, effects)

    def _draw_original(self, screen):
        """Original drawing method (fallback)"""
        # Draw shield effect if active
        if self.power_up_manager and self.power_up_manager.is_active('shield'):
            shield_radius = 45
            shield_alpha = int(100 + 50 * abs((pygame.time.get_ticks() % 1000) / 1000 - 0.5))
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 200, 255, shield_alpha),
                               (shield_radius, shield_radius), shield_radius, 4)
            screen.blit(shield_surface,
                        (self.x + self.width // 2 - shield_radius,
                         self.y + self.height // 2 - shield_radius))

        if not self.is_ducking:
            # STANDING T-REX
            body_color = self.color
            pygame.draw.rect(screen, body_color, (self.x + 10, self.y + 20, 25, 30))
            pygame.draw.rect(screen, body_color, (self.x + 28, self.y + 5, 20, 20))
            pygame.draw.polygon(screen, body_color, [
                (self.x + 48, self.y + 10),
                (self.x + 58, self.y + 13),
                (self.x + 48, self.y + 18)
            ])
            pygame.draw.circle(screen, BLACK, (int(self.x + 42), int(self.y + 12)), 2)

            arm_color = tuple(max(0, c - 20) for c in body_color)
            pygame.draw.rect(screen, arm_color, (self.x + 12, self.y + 28, 4, 10))
            pygame.draw.rect(screen, arm_color, (self.x + 28, self.y + 28, 4, 10))

            leg_offset = (pygame.time.get_ticks() // 100) % 8 - 4
            pygame.draw.rect(screen, arm_color, (self.x + 12, self.y + 48, 8, 12 + abs(leg_offset)))
            pygame.draw.rect(screen, arm_color, (self.x + 25, self.y + 48, 8, 12 + abs(-leg_offset)))

            tail_points = [
                (self.x + 10, self.y + 30),
                (self.x - 15, self.y + 22),
                (self.x - 10, self.y + 38)
            ]
            pygame.draw.polygon(screen, body_color, tail_points)

            spike_color = tuple(min(255, c + 30) for c in body_color)
            for i in range(4):
                spike_x = self.x + 15 + i * 7
                spike_y = self.y + 18
                pygame.draw.polygon(screen, spike_color, [
                    (spike_x, spike_y),
                    (spike_x - 3, spike_y + 8),
                    (spike_x + 3, spike_y + 8)
                ])

            pygame.draw.rect(screen, BLACK, (self.x + 10, self.y + 20, 25, 30), 2)
            pygame.draw.rect(screen, BLACK, (self.x + 28, self.y + 5, 20, 20), 2)
            pygame.draw.polygon(screen, BLACK, tail_points, 2)
        else:
            # DUCKING T-REX
            body_color = self.color
            pygame.draw.rect(screen, body_color, (self.x, self.y + 35, 40, 20))
            pygame.draw.rect(screen, body_color, (self.x + 30, self.y + 30, 22, 18))
            pygame.draw.polygon(screen, body_color, [
                (self.x + 52, self.y + 35),
                (self.x + 60, self.y + 38),
                (self.x + 52, self.y + 42)
            ])
            pygame.draw.circle(screen, BLACK, (int(self.x + 45), int(self.y + 37)), 2)

            tail_points = [
                (self.x, self.y + 42),
                (self.x - 18, self.y + 38),
                (self.x - 12, self.y + 48)
            ]
            pygame.draw.polygon(screen, body_color, tail_points)

            spike_color = tuple(min(255, c + 30) for c in body_color)
            for i in range(3):
                spike_x = self.x + 8 + i * 12
                spike_y = self.y + 33
                pygame.draw.polygon(screen, spike_color, [
                    (spike_x, spike_y),
                    (spike_x - 3, spike_y + 6),
                    (spike_x + 3, spike_y + 6)
                ])

            pygame.draw.rect(screen, BLACK, (self.x, self.y + 35, 40, 20), 2)
            pygame.draw.rect(screen, BLACK, (self.x + 30, self.y + 30, 22, 18), 2)
            pygame.draw.polygon(screen, BLACK, tail_points, 2)

        # Draw speed effect if active
        if self.power_up_manager and self.power_up_manager.is_active('speed'):
            for i in range(5):
                line_length = 15 - i * 2
                line_x = self.x - 15 - i * 6
                line_y = self.y + self.height // 2 + i * 4 - 10
                line_alpha = 255 - i * 40

                line_surface = pygame.Surface((line_length, 3), pygame.SRCALPHA)
                pygame.draw.line(line_surface, (*YELLOW[:3], line_alpha),
                                 (0, 1), (line_length, 1), 3)
                screen.blit(line_surface, (line_x, line_y))