import pygame
from settings import *


class SpriteSheet:
    """Handles sprite sheet loading and frame extraction"""

    def __init__(self):
        self.frames = {}
        self._create_trex_sprites()

    def _create_trex_sprites(self):
        """Create T-Rex sprites programmatically"""
        # Standing frames (2 frames for animation)
        self.frames['standing'] = [
            self._create_standing_frame(0),
            self._create_standing_frame(1)
        ]

        # Ducking frames (2 frames for animation)
        self.frames['ducking'] = [
            self._create_ducking_frame(0),
            self._create_ducking_frame(1)
        ]

        # Jumping frame (single frame)
        self.frames['jumping'] = [self._create_jumping_frame()]

    def _create_standing_frame(self, frame_num):
        """Create a standing T-Rex frame"""
        surface = pygame.Surface((60, 70), pygame.SRCALPHA)
        color = DARK_GREEN

        # Main body
        pygame.draw.rect(surface, color, (10, 20, 25, 30))

        # Head
        pygame.draw.rect(surface, color, (28, 5, 20, 20))

        # Open mouth
        pygame.draw.polygon(surface, color, [
            (48, 10), (58, 13), (48, 18)
        ])

        # Eye
        pygame.draw.circle(surface, BLACK, (42, 12), 2)

        # Arms
        arm_color = tuple(max(0, c - 20) for c in color)
        pygame.draw.rect(surface, arm_color, (12, 28, 4, 10))
        pygame.draw.rect(surface, arm_color, (28, 28, 4, 10))

        # Legs with animation offset
        leg_offset = 4 if frame_num == 0 else -4
        pygame.draw.rect(surface, arm_color, (12, 48, 8, 12 + abs(leg_offset)))
        pygame.draw.rect(surface, arm_color, (25, 48, 8, 12 + abs(-leg_offset)))

        # Tail
        tail_points = [(10, 30), (-5, 22), (0, 38)]
        pygame.draw.polygon(surface, color, tail_points)

        # Spikes
        spike_color = tuple(min(255, c + 30) for c in color)
        for i in range(4):
            spike_x = 15 + i * 7
            spike_y = 18
            pygame.draw.polygon(surface, spike_color, [
                (spike_x, spike_y),
                (spike_x - 3, spike_y + 8),
                (spike_x + 3, spike_y + 8)
            ])

        # Outlines
        pygame.draw.rect(surface, BLACK, (10, 20, 25, 30), 2)
        pygame.draw.rect(surface, BLACK, (28, 5, 20, 20), 2)
        pygame.draw.polygon(surface, BLACK, tail_points, 2)

        return surface

    def _create_ducking_frame(self, frame_num):
        """Create a ducking T-Rex frame"""
        surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        color = DARK_GREEN

        # Body stretched horizontally
        pygame.draw.rect(surface, color, (0, 35, 40, 20))

        # Head pointing forward
        pygame.draw.rect(surface, color, (30, 30, 22, 18))

        # Snout
        pygame.draw.polygon(surface, color, [
            (52, 35), (60, 38), (52, 42)
        ])

        # Eye
        pygame.draw.circle(surface, BLACK, (45, 37), 2)

        # Tail
        tail_points = [(0, 42), (-18, 38), (-12, 48)]
        pygame.draw.polygon(surface, color, tail_points)

        # Spikes
        spike_color = tuple(min(255, c + 30) for c in color)
        for i in range(3):
            spike_x = 8 + i * 12
            spike_y = 33
            pygame.draw.polygon(surface, spike_color, [
                (spike_x, spike_y),
                (spike_x - 3, spike_y + 6),
                (spike_x + 3, spike_y + 6)
            ])

        # Outlines
        pygame.draw.rect(surface, BLACK, (0, 35, 40, 20), 2)
        pygame.draw.rect(surface, BLACK, (30, 30, 22, 18), 2)
        pygame.draw.polygon(surface, BLACK, tail_points, 2)

        return surface

    def _create_jumping_frame(self):
        """Create a jumping T-Rex frame"""
        surface = pygame.Surface((60, 70), pygame.SRCALPHA)
        color = DARK_GREEN

        # Main body
        pygame.draw.rect(surface, color, (10, 20, 25, 30))

        # Head
        pygame.draw.rect(surface, color, (28, 5, 20, 20))

        # Open mouth
        pygame.draw.polygon(surface, color, [
            (48, 10), (58, 13), (48, 18)
        ])

        # Eye
        pygame.draw.circle(surface, BLACK, (42, 12), 2)

        # Arms
        arm_color = tuple(max(0, c - 20) for c in color)
        pygame.draw.rect(surface, arm_color, (12, 28, 4, 10))
        pygame.draw.rect(surface, arm_color, (28, 28, 4, 10))

        # Legs bent for jumping
        pygame.draw.rect(surface, arm_color, (14, 48, 8, 10))
        pygame.draw.rect(surface, arm_color, (23, 48, 8, 10))

        # Tail
        tail_points = [(10, 30), (-5, 22), (0, 38)]
        pygame.draw.polygon(surface, color, tail_points)

        # Spikes
        spike_color = tuple(min(255, c + 30) for c in color)
        for i in range(4):
            spike_x = 15 + i * 7
            spike_y = 18
            pygame.draw.polygon(surface, spike_color, [
                (spike_x, spike_y),
                (spike_x - 3, spike_y + 8),
                (spike_x + 3, spike_y + 8)
            ])

        # Outlines
        pygame.draw.rect(surface, BLACK, (10, 20, 25, 30), 2)
        pygame.draw.rect(surface, BLACK, (28, 5, 20, 20), 2)
        pygame.draw.polygon(surface, BLACK, tail_points, 2)

        return surface

    def get_frame(self, state, frame_num=0):
        """Get a specific frame for a state"""
        if state in self.frames:
            frames = self.frames[state]
            return frames[frame_num % len(frames)]
        return self.frames['standing'][0]

    def colorize_sprite(self, sprite, color):
        """Change the color of a sprite"""
        colored_sprite = sprite.copy()
        w, h = colored_sprite.get_size()

        # Create a color overlay
        for x in range(w):
            for y in range(h):
                current_color = colored_sprite.get_at((x, y))
                if current_color.a > 0:  # If pixel is not transparent
                    # Check if it's black (outline) - preserve black
                    if current_color.r < 50 and current_color.g < 50 and current_color.b < 50:
                        continue  # Keep black outlines

                    # Preserve the darkness/lightness but change hue
                    brightness = (current_color.r + current_color.g + current_color.b) / (255 * 3)
                    new_color = (
                        int(color[0] * brightness),
                        int(color[1] * brightness),
                        int(color[2] * brightness),
                        current_color.a
                    )
                    colored_sprite.set_at((x, y), new_color)

        return colored_sprite


class AnimatedSprite:
    """Handles sprite animation for the player"""

    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
        self.current_state = 'standing'
        self.frame_index = 0
        self.animation_speed = 8  # Frames to wait before changing sprite
        self.animation_counter = 0
        self.current_color = DARK_GREEN

    def update(self, state, is_moving=True):
        """Update the animation state"""
        self.current_state = state

        # Only animate if moving (for standing/ducking)
        if is_moving and state in ['standing', 'ducking']:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                num_frames = len(self.sprite_sheet.frames[state])
                self.frame_index = (self.frame_index + 1) % num_frames
        else:
            self.frame_index = 0

    def set_color(self, color):
        """Set the sprite color"""
        self.current_color = color

    def get_current_sprite(self):
        """Get the current sprite frame"""
        base_sprite = self.sprite_sheet.get_frame(self.current_state, self.frame_index)
        return self.sprite_sheet.colorize_sprite(base_sprite, self.current_color)

    def draw(self, screen, x, y, effects=None):
        """Draw the sprite with optional effects"""
        sprite = self.get_current_sprite()

        # Draw shield effect if active
        if effects and 'shield' in effects:
            shield_radius = 45
            shield_alpha = int(100 + 50 * abs((pygame.time.get_ticks() % 1000) / 1000 - 0.5))
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 200, 255, shield_alpha),
                               (shield_radius, shield_radius), shield_radius, 4)
            screen.blit(shield_surface, (x + sprite.get_width() // 2 - shield_radius,
                                         y + sprite.get_height() // 2 - shield_radius))

        # Draw the sprite
        screen.blit(sprite, (x, y))

        # Draw speed effect if active
        if effects and 'speed' in effects:
            for i in range(5):
                line_length = 15 - i * 2
                line_x = x - 15 - i * 6
                line_y = y + sprite.get_height() // 2 + i * 4 - 10
                line_alpha = 255 - i * 40

                line_surface = pygame.Surface((line_length, 3), pygame.SRCALPHA)
                pygame.draw.line(line_surface, (*YELLOW[:3], line_alpha),
                                 (0, 1), (line_length, 1), 3)
                screen.blit(line_surface, (line_x, line_y))