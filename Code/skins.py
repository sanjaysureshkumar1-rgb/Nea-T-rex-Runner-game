import pygame
from settings import AVAILABLE_SKINS, SCREEN_WIDTH, WHITE, TEXT_SHADOW, GOLD, GREEN, GRAY, RED, BLACK, BUTTON_SHADOW


class SkinManager:
    """Manages player skins"""

    def __init__(self):
        self.skins = AVAILABLE_SKINS.copy()
        self.current_skin = "Classic"
        self.total_coins = 0

    def get_current_color(self):
        """Get color of current skin"""
        return self.skins[self.current_skin]["color"]

    def is_unlocked(self, skin_name):
        """Check if skin is unlocked"""
        return self.skins[skin_name]["unlocked"]

    def can_afford(self, skin_name):
        """Check if player can afford skin"""
        return self.total_coins >= self.skins[skin_name]["cost"]

    def unlock_skin(self, skin_name):
        """Unlock a skin"""
        if not self.is_unlocked(skin_name) and self.can_afford(skin_name):
            cost = self.skins[skin_name]["cost"]
            self.total_coins -= cost
            self.skins[skin_name]["unlocked"] = True
            self.current_skin = skin_name
            return True
        return False

    def select_skin(self, skin_name):
        """Select a skin"""
        if self.is_unlocked(skin_name):
            self.current_skin = skin_name
            return True
        return False

    def add_coins(self, amount):
        """Add coins"""
        self.total_coins += amount

    def get_skin_list(self):
        """Get all skins"""
        return [(name, data) for name, data in self.skins.items()]

    def save_data(self):
        """Save data"""
        return {
            "skins": self.skins,
            "current_skin": self.current_skin,
            "total_coins": self.total_coins
        }

    def load_data(self, data):
        """Load data"""
        if "skins" in data:
            self.skins = data["skins"]
        if "current_skin" in data:
            self.current_skin = data["current_skin"]
        if "total_coins" in data:
            self.total_coins = data["total_coins"]


class SkinDisplay:
    """Displays skin selection screen"""

    def __init__(self, skin_manager):
        self.skin_manager = skin_manager
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 30

    def handle_scroll(self, scroll_y):
        """Handle mouse wheel scrolling"""
        self.scroll_offset -= scroll_y * self.scroll_speed
        # Clamp scroll to valid range
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    def draw(self, screen):
        """Draw skin selection"""
        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("SELECT SKIN", True, WHITE)
        title_shadow = title_font.render("SELECT SKIN", True, TEXT_SHADOW)
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 3, 53))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Coins
        coin_font = pygame.font.Font(None, 40)
        coin_text = coin_font.render(f"Coins: {self.skin_manager.total_coins}", True, GOLD)
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, 120))

        # Calculate max scroll based on content
        skin_count = len(self.skin_manager.get_skin_list())
        total_content_height = skin_count * 65
        visible_area_start = 180
        visible_area_height = screen.get_height() - visible_area_start - 20
        self.max_scroll = max(0, total_content_height - visible_area_height)

        # Draw skins with scroll offset
        y_pos = 180 - self.scroll_offset
        for skin_name, skin_data in self.skin_manager.get_skin_list():
            # Only draw if visible on screen
            if -65 < y_pos < screen.get_height():
                self.draw_skin_card(screen, skin_name, skin_data, y_pos)
            y_pos += 65

        # Draw scroll indicator if needed
        if self.max_scroll > 0:
            indicator_font = pygame.font.Font(None, 24)
            if self.scroll_offset < self.max_scroll:
                scroll_text = indicator_font.render("↓ Scroll for more ↓", True, WHITE)
                screen.blit(scroll_text, (SCREEN_WIDTH // 2 - scroll_text.get_width() // 2,
                                          screen.get_height() - 30))

    def draw_skin_card(self, screen, skin_name, skin_data, y):
        """Draw skin card"""
        x = SCREEN_WIDTH // 2 - 200
        width = 400
        height = 55

        # Color based on status
        if skin_name == self.skin_manager.current_skin:
            card_color = GREEN
            border_color = WHITE
        elif skin_data["unlocked"]:
            card_color = GRAY
            border_color = BLACK
        else:
            card_color = (80, 80, 80)
            border_color = RED

        # Shadow
        shadow_rect = pygame.Rect(x + 4, y + 4, width, height)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=10)

        # Card
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, card_color, card_rect, border_radius=10)
        pygame.draw.rect(screen, border_color, card_rect, 3, border_radius=10)

        # Preview
        preview_x = x + 15
        preview_y = y + height // 2 - 15
        pygame.draw.rect(screen, skin_data["color"],
                         pygame.Rect(preview_x, preview_y, 25, 30), border_radius=4)
        pygame.draw.circle(screen, skin_data["color"], (preview_x + 22, preview_y + 8), 8)
        pygame.draw.rect(screen, BLACK,
                         pygame.Rect(preview_x, preview_y, 25, 30), 2, border_radius=4)

        # Name
        name_font = pygame.font.Font(None, 32)
        name_text = name_font.render(skin_name, True, WHITE)
        screen.blit(name_text, (x + 80, y + 8))

        # Status
        status_font = pygame.font.Font(None, 24)
        if skin_name == self.skin_manager.current_skin:
            status_text = status_font.render("EQUIPPED", True, WHITE)
        elif skin_data["unlocked"]:
            status_text = status_font.render("UNLOCKED", True, WHITE)
        else:
            status_text = status_font.render(f"{skin_data['cost']} coins", True, GOLD)
        screen.blit(status_text, (x + 80, y + 32))

        return card_rect

    def handle_click(self, mouse_pos):
        """Handle clicks"""
        y_pos = 180 - self.scroll_offset
        for skin_name, skin_data in self.skin_manager.get_skin_list():
            card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 55)

            if card_rect.collidepoint(mouse_pos):
                if skin_data["unlocked"]:
                    self.skin_manager.select_skin(skin_name)
                    return True
                else:
                    if self.skin_manager.unlock_skin(skin_name):
                        return True

            y_pos += 65

        return False