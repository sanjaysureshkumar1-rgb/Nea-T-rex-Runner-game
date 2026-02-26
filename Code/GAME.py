import pygame
import random
import json
import os
from enum import Enum

# Initialise Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    LEADERBOARD = 4
    SETTINGS = 5
    SKINS = 6
    STORY_MODE = 7
    LEVEL_SELECT = 8

# Player Class
class Player:
    def __init__(self, x, y, skin_color=WHITE):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.is_ducking = False
        self.skin_color = skin_color
        self.shield_active = False
        self.speed_boost_active = False
        self.shield_timer = 0
        self.speed_timer = 0

    def jump(self):
        if self.on_ground and not self.is_ducking:
            self.vel_y = self.jump_power
            self.on_ground = False

    def duck(self):
        if self.on_ground:
            self.is_ducking = True
            self.height = 25

    def stand(self):
        self.is_ducking = False
        self.height = 50

    def update(self, ground_y):
        # Apply gravity
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Ground collision
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Update power-up timers
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.speed_boost_active:
            self.speed_timer -= 1
            if self.speed_timer <= 0:
                self.speed_boost_active = False

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 300  # 5 seconds at 60 FPS

    def activate_speed_boost(self):
        self.speed_boost_active = True
        self.speed_timer = 180  # 3 seconds at 60 FPS

    def draw(self, screen):
        # Draw shield effect
        if self.shield_active:
            pygame.draw.circle(screen, BLUE, (int(self.x + self.width//2), int(self.y + self.height//2)),
                               max(self.width, self.height)//2 + 5, 3)

        # Draw player
        pygame.draw.rect(screen, self.skin_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Obstacle Class
class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (139, 69, 19)  # Brown

    def update(self, speed_multiplier=1.0):
        self.x -= self.speed * speed_multiplier

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0

# Power-up Class
class PowerUp:
    def __init__(self, x, y, type_name):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        self.type = type_name  # "shield" or "speed"
        self.color = BLUE if type_name == "shield" else YELLOW

    def update(self, speed_multiplier=1.0):
        self.x -= self.speed * speed_multiplier

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + self.height//2)),
                           self.width//2)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width//2), int(self.y + self.height//2)),
                           self.width//2, 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0

# Coin Class
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 5
        self.color = YELLOW

    def update(self, speed_multiplier=1.0):
        self.x -= self.speed * speed_multiplier

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + self.height//2)),
                           self.width//2)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width//2), int(self.y + self.height//2)),
                           self.width//2, 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game Class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced T-Rex Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU

        # Game variables
        self.score = 0
        self.high_score = 0
        self.coins = 0
        self.total_coins = 0
        self.level = 1
        self.ground_y = SCREEN_HEIGHT - 50

        # Player
        self.player = Player(100, self.ground_y - 50)

        # Game objects
        self.obstacles = []
        self.powerups = []
        self.coins_list = []

        # Timers
        self.obstacle_timer = 0
        self.powerup_timer = 0
        self.coin_timer = 0

        # Skins
        self.available_skins = {
            "Classic": {"color": WHITE, "unlocked": True, "cost": 0},
            "Red": {"color": RED, "unlocked": False, "cost": 100},
            "Blue": {"color": BLUE, "unlocked": False, "cost": 150},
            "Green": {"color": (0, 255, 0), "unlocked": False, "cost": 200},
            "Yellow": {"color": YELLOW, "unlocked": False, "cost": 250},
        }
        self.current_skin = "Classic"

        # Leaderboard
        self.leaderboard = []

        # Load data
        self.load_data()

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        center_x = SCREEN_WIDTH // 2 - 100
        self.start_button = Button(center_x, 230, 200, 60, "Start Game", GREEN)
        self.leaderboard_button = Button(center_x, 330, 200, 60, "Leaderboard", BLUE)
        self.settings_button = Button(center_x, 430, 200, 60, "Settings", GRAY)
        self.quit_button = Button(center_x, 530, 200, 60, "Quit", RED)
        self.back_button = Button(20, 20, 100, 40, "Back", GRAY)
        self.skins_button = Button(center_x, 330, 200, 60, "Skins", (255, 200, 0))

    def reset_game(self):
        self.score = 0
        self.coins = 0
        self.level = 1
        self.player = Player(100, self.ground_y - 50, self.available_skins[self.current_skin]["color"])
        self.obstacles = []
        self.powerups = []
        self.coins_list = []
        self.obstacle_timer = 0
        self.powerup_timer = 0
        self.coin_timer = 0

    def spawn_obstacle(self):
        # Different obstacle types based on level
        if self.level == 1:
            height = random.choice([40, 50, 60])
            width = 30
        elif self.level == 2:
            height = random.choice([50, 60, 70])
            width = random.choice([30, 40])
        else:
            height = random.choice([60, 70, 80])
            width = random.choice([40, 50])

        y = self.ground_y - height
        speed = 5 + self.level * 0.5

        obstacle = Obstacle(SCREEN_WIDTH, y, width, height, speed)
        self.obstacles.append(obstacle)

    def spawn_powerup(self):
        y = random.randint(self.ground_y - 200, self.ground_y - 100)
        powerup_type = random.choice(["shield", "speed"])
        powerup = PowerUp(SCREEN_WIDTH, y, powerup_type)
        self.powerups.append(powerup)

    def spawn_coin(self):
        y = random.randint(self.ground_y - 200, self.ground_y - 50)
        coin = Coin(SCREEN_WIDTH, y)
        self.coins_list.append(coin)

    def check_collisions(self):
        player_rect = self.player.get_rect()

        # Check obstacle collisions
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                if self.player.shield_active:
                    self.player.shield_active = False
                    self.obstacles.remove(obstacle)
                else:
                    self.game_over()
                    return

        # Check powerup collisions
        for powerup in self.powerups[:]:
            if player_rect.colliderect(powerup.get_rect()):
                if powerup.type == "shield":
                    self.player.activate_shield()
                elif powerup.type == "speed":
                    self.player.activate_speed_boost()
                self.powerups.remove(powerup)

        # Check coin collisions
        for coin in self.coins_list[:]:
            if player_rect.colliderect(coin.get_rect()):
                self.coins += 1
                self.total_coins += 1
                self.score += 5
                self.coins_list.remove(coin)

    def update_level(self):
        # Level up every 500 points
        new_level = (self.score // 500) + 1
        if new_level > self.level:
            self.level = new_level

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score

        # Add to leaderboard
        self.leaderboard.append(self.score)
        self.leaderboard.sort(reverse=True)
        self.leaderboard = self.leaderboard[:5]  # Keep top 5

        self.save_data()
        self.state = GameState.GAME_OVER

    def save_data(self):
        data = {
            "high_score": self.high_score,
            "total_coins": self.total_coins,
            "leaderboard": self.leaderboard,
            "skins": self.available_skins,
            "current_skin": self.current_skin
        }
        try:
            with open("game_data.json", "w") as f:
                json.dump(data, f)
        except:
            pass

    def load_data(self):
        try:
            if os.path.exists("game_data.json"):
                with open("game_data.json", "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.total_coins = data.get("total_coins", 0)
                    self.leaderboard = data.get("leaderboard", [])
                    self.available_skins = data.get("skins", self.available_skins)
                    self.current_skin = data.get("current_skin", "Classic")
        except:
            pass

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.start_button.is_clicked(pos):
                self.reset_game()
                self.state = GameState.PLAYING
            elif self.leaderboard_button.is_clicked(pos):
                self.state = GameState.LEADERBOARD
            elif self.skins_button.is_clicked(pos):
                self.state = GameState.SKINS
            elif self.settings_button.is_clicked(pos):
                self.state = GameState.SETTINGS
            elif self.quit_button.is_clicked(pos):
                self.running = False

    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.player.jump()
            elif event.key == pygame.K_DOWN:
                self.player.duck()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.player.stand()

    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.state = GameState.MENU

    def handle_other_screen_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.back_button.is_clicked(pos):
                self.state = GameState.MENU

            # Skin selection
            if self.state == GameState.SKINS:
                y_pos = 150
                for skin_name, skin_data in self.available_skins.items():
                    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_pos, 300, 50)
                    if button_rect.collidepoint(pos):
                        if skin_data["unlocked"]:
                            self.current_skin = skin_name
                            self.save_data()
                        elif self.total_coins >= skin_data["cost"]:
                            self.total_coins -= skin_data["cost"]
                            skin_data["unlocked"] = True
                            self.current_skin = skin_name
                            self.save_data()
                    y_pos += 70

    def update_playing(self):
        # Update score
        self.score += 1

        # Update level
        self.update_level()

        # Update player
        speed_multiplier = 1.5 if self.player.speed_boost_active else 1.0
        self.player.update(self.ground_y)

        # Spawn obstacles
        self.obstacle_timer += 1
        spawn_rate = max(60, 120 - self.level * 10)
        if self.obstacle_timer >= spawn_rate:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        # Spawn powerups
        self.powerup_timer += 1
        if self.powerup_timer >= 300:  # Every 5 seconds
            self.spawn_powerup()
            self.powerup_timer = 0

        # Spawn coins
        self.coin_timer += 1
        if self.coin_timer >= 100:  # More frequent than powerups
            self.spawn_coin()
            self.coin_timer = 0

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(speed_multiplier)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update(speed_multiplier)
            if powerup.is_off_screen():
                self.powerups.remove(powerup)

        # Update coins
        for coin in self.coins_list[:]:
            coin.update(speed_multiplier)
            if coin.is_off_screen():
                self.coins_list.remove(coin)

        # Check collisions
        self.check_collisions()

    def draw_menu(self):
        self.screen.fill(GREEN)

        # Title
        title = self.title_font.render("T-REX RUNNER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 130))
        self.screen.blit(title, title_rect)

        # Buttons
        self.start_button.draw(self.screen)
        self.leaderboard_button.draw(self.screen)
        self.skins_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        # Display total coins
        coins_text = self.small_font.render(f"Total Coins: {self.total_coins}", True, BLACK)
        self.screen.blit(coins_text, (10, SCREEN_HEIGHT - 30))

    def draw_playing(self):
        # Background color changes with level
        if self.level == 1:
            bg_color = GREEN
        elif self.level == 2:
            bg_color = (255, 200, 150)  # Desert
        elif self.level == 3:
            bg_color = (150, 255, 150)  # Jungle
        else:
            bg_color = (200, 230, 255)  # Ice

        self.screen.fill(bg_color)

        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, self.ground_y), (SCREEN_WIDTH, self.ground_y), 3)

        # Draw game objects
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        for coin in self.coins_list:
            coin.draw(self.screen)

        self.player.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (10, 50))

        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        coins_text = self.font.render(f"Coins: {self.coins}", True, BLACK)
        self.screen.blit(coins_text, (SCREEN_WIDTH - 150, 50))

        # Power-up indicators
        if self.player.shield_active:
            shield_text = self.small_font.render(f"Shield: {self.player.shield_timer//60}s", True, BLUE)
            self.screen.blit(shield_text, (10, 90))

        if self.player.speed_boost_active:
            speed_text = self.small_font.render(f"Speed: {self.player.speed_timer//60}s", True, YELLOW)
            self.screen.blit(speed_text, (10, 120))

    def draw_game_over(self):
        self.screen.fill(RED)

        # Game Over text
        game_over_text = self.title_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(game_over_text, game_over_rect)

        # Score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(score_text, score_rect)

        # High Score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(high_score_text, high_score_rect)

        # Coins earned
        coins_text = self.font.render(f"Coins Earned: {self.coins}", True, WHITE)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(coins_text, coins_rect)

        # Instructions
        restart_text = self.small_font.render("Click or press any key to return to menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(restart_text, restart_rect)

    def draw_leaderboard(self):
        self.screen.fill(BLUE)

        self.back_button.draw(self.screen)

        # Title
        title = self.title_font.render("LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)

        # Scores
        y_pos = 200
        for i, score in enumerate(self.leaderboard):
            score_text = self.font.render(f"{i+1}. {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            self.screen.blit(score_text, score_rect)
            y_pos += 60

        if not self.leaderboard:
            no_scores = self.font.render("No scores yet!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(no_scores, no_scores_rect)

    def draw_settings(self):
        self.screen.fill(GRAY)

        self.back_button.draw(self.screen)

        # Title
        title = self.title_font.render("SETTINGS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)

        # Settings info
        info = self.font.render("Settings coming soon!", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(info, info_rect)

    def draw_skins(self):
        self.screen.fill((255, 200, 0))

        self.back_button.draw(self.screen)

        # Title
        title = self.title_font.render("SKINS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)

        # Total coins
        coins_text = self.small_font.render(f"Total Coins: {self.total_coins}", True, BLACK)
        self.screen.blit(coins_text, (SCREEN_WIDTH//2 - 80, 120))

        # Skins
        y_pos = 180
        for skin_name, skin_data in self.available_skins.items():
            # Button color
            if skin_name == self.current_skin:
                button_color = (0, 200, 0)  # Green for selected
            elif skin_data["unlocked"]:
                button_color = (150, 150, 150)  # Gray for unlocked
            else:
                button_color = (100, 100, 100)  # Dark gray for locked

            # Draw button
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_pos, 300, 50)
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 3)

            # Draw skin preview
            preview_rect = pygame.Rect(SCREEN_WIDTH//2 - 140, y_pos + 10, 30, 30)
            pygame.draw.rect(self.screen, skin_data["color"], preview_rect)
            pygame.draw.rect(self.screen, BLACK, preview_rect, 2)

            # Text
            if skin_data["unlocked"]:
                text = skin_name + (" (Selected)" if skin_name == self.current_skin else "")
            else:
                text = f"{skin_name} - {skin_data['cost']} coins"

            skin_text = self.small_font.render(text, True, BLACK)
            self.screen.blit(skin_text, (SCREEN_WIDTH//2 - 100, y_pos + 15))

            y_pos += 70

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == GameState.MENU:
                    self.handle_menu_events(event)
                elif self.state == GameState.PLAYING:
                    self.handle_playing_events(event)
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_events(event)
                else:
                    self.handle_other_screen_events(event)

            # Update
            if self.state == GameState.PLAYING:
                self.update_playing()

            # Draw
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_playing()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            elif self.state == GameState.LEADERBOARD:
                self.draw_leaderboard()
            elif self.state == GameState.SETTINGS:
                self.draw_settings()
            elif self.state == GameState.SKINS:
                self.draw_skins()

            pygame.display.flip()

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()