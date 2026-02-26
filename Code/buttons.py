import pygame
from settings import *
class Button:
    """Reusable button class for UI"""

    def __init__(self, x, y, width, height, text, colour, hover_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.current_colour = colour
        self.font = pygame.font.Font(None, 36)

    def update(self, mouse_pos):
        """Update button hover state"""
        if self.rect.collidepoint(mouse_pos):
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.colour

    def draw(self, screen):
        """Draw the button"""
        # Shadow
        shadow_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4,
                                   self.rect.width, self.rect.height)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=10)

        # Button background
        pygame.draw.rect(screen, self.current_colour, self.rect, border_radius=10)

        # Button border
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)

        # Button text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos)