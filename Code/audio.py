import pygame


class AudioManager:
    """Simple audio manager that won't crash if files are missing"""

    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            pass

        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.sounds = {}
        self.enabled = True

    def play_sound(self, sound_name):
        """Play a sound effect - won't crash if missing"""
        pass  # Silently ignore for now

    def play_music(self, music_file=None):
        """Play background music - won't crash if missing"""
        pass  # Silently ignore for now

    def stop_music(self):
        """Stop music"""
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def set_music_volume(self, volume):
        """Set music volume"""
        self.music_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume):
        """Set sound effects volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def get_music_volume(self):
        """Get music volume"""
        return self.music_volume

    def get_sfx_volume(self):
        """Get sound effects volume"""
        return self.sfx_volume


class VolumeSlider:
    """Volume slider UI element"""

    def __init__(self, x, y, width, height, label, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = initial_value
        self.dragging = False

    def update(self, mouse_pos, mouse_pressed):
        """Update slider"""
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_y = self.rect.y + self.rect.height // 2

        distance = ((mouse_pos[0] - handle_x) ** 2 + (mouse_pos[1] - handle_y) ** 2) ** 0.5

        if mouse_pressed and distance < 15:
            self.dragging = True

        if not mouse_pressed:
            self.dragging = False

        if self.dragging:
            relative_x = mouse_pos[0] - self.rect.x
            self.value = max(0.0, min(1.0, relative_x / self.rect.width))
            return True

        return False

    def draw(self, screen):
        """Draw slider"""
        # Label
        font = pygame.font.Font(None, 28)
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 30))

        # Track
        track_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 2 - 3,
                                 self.rect.width, 6)
        pygame.draw.rect(screen, (100, 100, 100), track_rect, border_radius=3)

        # Filled portion
        filled_width = int(self.value * self.rect.width)
        filled_rect = pygame.Rect(track_rect.x, track_rect.y, filled_width, track_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), filled_rect, border_radius=3)

        # Handle
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_y = self.rect.y + self.rect.height // 2

        pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 12)
        pygame.draw.circle(screen, (0, 0, 0), (handle_x, handle_y), 12, 2)

        # Value display
        value_text = font.render(f"{int(self.value * 100)}%", True, (255, 255, 255))
        screen.blit(value_text, (self.rect.x + self.rect.width + 20,
                                 self.rect.y + self.rect.height // 2 - 14))