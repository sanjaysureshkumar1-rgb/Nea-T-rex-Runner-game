import pygame
import random
from settings import *
from obstacles import ObstacleSpawner


class TwoPlayerDino:
    """T-Rex player class for 2-player mode with LEFT/RIGHT movement"""

    def __init__(self, x, colour, controls, player_num):
        self.x = x
        self.y = GROUND_LEVEL
        self.width = 40
        self.height = 50
        self.colour = colour
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.is_ducking = False
        self.controls = controls
        self.player_num = player_num
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.alive = True
        self.facing_right = True  # NEW: Track which direction player is facing

        # Animation
        self.run_animation_frame = 0
        self.animation_speed = 10
        self.animation_counter = 0

        # Movement
        self.move_speed = 6

    def jump(self):
        """Make player jump"""
        if not self.is_jumping and not self.is_ducking and self.alive:
            self.velocity_y = -16
            self.is_jumping = True
            return True
        return False

    def duck(self):
        """Make player duck"""
        if not self.is_jumping and self.alive:
            self.is_ducking = True
            self.height = 25
            self.y = GROUND_LEVEL + 25

    def stand_up(self):
        """Stand up from ducking"""
        if not self.is_jumping:
            self.is_ducking = False
            self.height = 50
            self.y = GROUND_LEVEL

    def move_left(self):
        """Move player left"""
        if self.alive and not self.is_ducking:
            self.velocity_x = -self.move_speed
            self.facing_right = False

    def move_right(self):
        """Move player right"""
        if self.alive and not self.is_ducking:
            self.velocity_x = self.move_speed
            self.facing_right = True

    def stop_horizontal_movement(self):
        """Stop horizontal movement"""
        self.velocity_x = 0

    def update(self):
        """Update player physics and animation"""
        if self.alive:
            # Handle jumping physics
            if self.is_jumping:
                self.velocity_y += GRAVITY
                self.y += self.velocity_y

                if self.y >= GROUND_LEVEL:
                    self.y = GROUND_LEVEL
                    self.velocity_y = 0
                    self.is_jumping = False

            # Handle horizontal movement
            self.x += self.velocity_x

            # Keep player on screen
            if self.x < 0:
                self.x = 0
            elif self.x > SCREEN_WIDTH - self.width:
                self.x = SCREEN_WIDTH - self.width

            # Update animation
            if not self.is_jumping and abs(self.velocity_x) > 0:
                self.animation_counter += 1
                if self.animation_counter >= self.animation_speed:
                    self.run_animation_frame = (self.run_animation_frame + 1) % 2
                    self.animation_counter = 0

        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

    def draw(self, screen):
        """Draw the T-Rex player"""
        if self.alive:
            # Flip the drawing if facing left
            flip = -1 if not self.facing_right else 1
            center_x = self.x + self.width // 2

            # Main body
            body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, self.colour, body_rect)

            # Head (offset based on direction)
            head_width = 25
            head_height = 20
            head_x = center_x + (flip * 7) - head_width // 2
            head_rect = pygame.Rect(head_x, self.y - 15, head_width, head_height)
            pygame.draw.rect(screen, self.colour, head_rect)

            # Eye (position based on direction)
            eye_x = center_x + (flip * 15)
            eye_y = self.y - 10
            pygame.draw.circle(screen, WHITE, (int(eye_x), eye_y), 4)
            pygame.draw.circle(screen, BLACK, (int(eye_x), eye_y), 2)

            # Mouth (points in facing direction)
            mouth_start = (center_x + (flip * 18), self.y - 5)
            mouth_end = (center_x + (flip * 18), self.y)
            pygame.draw.line(screen, BLACK, mouth_start, mouth_end, 2)

            if not self.is_ducking:
                # Tail (opposite side from face)
                tail_tip_x = center_x - (flip * 25)
                tail_points = [
                    (center_x - (flip * 10), self.y + 10),
                    (tail_tip_x, self.y + 5),
                    (tail_tip_x + (flip * 5), self.y + 15)
                ]
                pygame.draw.polygon(screen, self.colour, tail_points)

                # Arms (small)
                arm_rect = pygame.Rect(self.x + 5, self.y + 15, 8, 12)
                pygame.draw.rect(screen, self.colour, arm_rect)

                # Legs (running animation)
                if self.run_animation_frame == 0 or abs(self.velocity_x) < 0.1:
                    # Both legs down when standing still or frame 0
                    left_leg = pygame.Rect(self.x + 8, self.y + 35, 8, 20)
                    right_leg = pygame.Rect(self.x + 24, self.y + 35, 8, 20)
                else:
                    # Alternating legs when running
                    left_leg = pygame.Rect(self.x + 8, self.y + 40, 8, 15)
                    right_leg = pygame.Rect(self.x + 24, self.y + 35, 8, 20)

                pygame.draw.rect(screen, self.colour, left_leg)
                pygame.draw.rect(screen, self.colour, right_leg)
            else:
                # Ducking - shorter body, no visible legs
                pass

            # Player number badge
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.player_num), True, WHITE)
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)

        else:
            # Draw dead T-Rex (grey and fallen)
            dead_body = pygame.Rect(self.x, self.y + 20, self.height, self.width - 10)
            pygame.draw.rect(screen, GRAY, dead_body)

            dead_head = pygame.Rect(self.x + self.height, self.y + 20, 20, 20)
            pygame.draw.rect(screen, GRAY, dead_head)

            # X eyes
            pygame.draw.line(screen, RED,
                             (self.x + self.height + 5, self.y + 25),
                             (self.x + self.height + 15, self.y + 35), 3)
            pygame.draw.line(screen, RED,
                             (self.x + self.height + 15, self.y + 25),
                             (self.x + self.height + 5, self.y + 35), 3)


class Coin:
    """Coin collectible"""

    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5
        self.collected = False

    def update(self):
        """Move coin left"""
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        """Draw coin"""
        pygame.draw.circle(screen, GOLD, (int(self.x + 10), int(self.y + 10)), 10)
        pygame.draw.circle(screen, BLACK, (int(self.x + 10), int(self.y + 10)), 10, 2)

    def is_off_screen(self):
        """Check if coin is off screen"""
        return self.x < -self.width


def two_player_game(screen, clock, audio_manager, skin_manager):
    """Main 2-player game function with LEFT/RIGHT movement"""

    # Create two players with different controls
    # Player 1 (Red) - WASD controls
    player1_controls = {
        'jump': pygame.K_w,
        'duck': pygame.K_s,
        'left': pygame.K_a,  # NEW
        'right': pygame.K_d  # NEW
    }
    player1 = TwoPlayerDino(150, RED, player1_controls, 1)

    # Player 2 (Blue) - Arrow keys
    player2_controls = {
        'jump': pygame.K_UP,
        'duck': pygame.K_DOWN,
        'left': pygame.K_LEFT,  # NEW
        'right': pygame.K_RIGHT  # NEW
    }
    player2 = TwoPlayerDino(250, BLUE, player2_controls, 2)

    players = [player1, player2]

    # Game variables
    obstacles = []
    coins = []
    score = 0
    spawn_timer = 0
    coin_spawn_timer = 0
    level = 1
    game_over = False
    paused = False

    # Create obstacle spawner
    obstacle_spawner = ObstacleSpawner()

    # Fonts
    score_font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72)
    instruction_font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 48)

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Return to main menu

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # Restart 2-player game
                        return two_player_game(screen, clock, audio_manager, skin_manager)
                    elif event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        return  # Return to menu

                elif paused:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = False
                        audio_manager.play_sound('coin')
                    elif event.key == pygame.K_m:
                        return  # Return to menu

                else:
                    # Player 1 jump
                    if event.key == player1.controls['jump']:
                        if player1.jump():
                            audio_manager.play_sound('jump')

                    # Player 2 jump
                    if event.key == player2.controls['jump']:
                        if player2.jump():
                            audio_manager.play_sound('jump')

                    # Pause
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = True

        # Get continuous key states for movement and ducking
        keys = pygame.key.get_pressed()

        if not game_over and not paused:
            # ===== PLAYER 1 CONTROLS =====
            # Ducking (continuous press)
            if keys[player1.controls['duck']]:
                player1.duck()
            else:
                player1.stand_up()

            # Left/Right movement (NEW!)
            if keys[player1.controls['left']]:
                player1.move_left()
            elif keys[player1.controls['right']]:
                player1.move_right()
            else:
                player1.stop_horizontal_movement()

            # ===== PLAYER 2 CONTROLS =====
            # Ducking
            if keys[player2.controls['duck']]:
                player2.duck()
            else:
                player2.stand_up()

            # Left/Right movement (NEW!)
            if keys[player2.controls['left']]:
                player2.move_left()
            elif keys[player2.controls['right']]:
                player2.move_right()
            else:
                player2.stop_horizontal_movement()

            # Update players
            for player in players:
                player.update()

            # Spawn obstacles
            spawn_timer += 1
            spawn_interval = max(60, 90 - (level * 5))
            if spawn_timer > spawn_interval:
                spawn_timer = 0
                obstacles.append(obstacle_spawner.spawn(level))

            # Spawn coins at random positions (not just scrolling)
            coin_spawn_timer += 1
            if coin_spawn_timer > 90:
                coin_spawn_timer = 0
                # Spawn coins at random X positions across screen
                coin_x = random.randint(50, SCREEN_WIDTH - 50)
                coin_y = random.choice([GROUND_LEVEL - 50, GROUND_LEVEL - 100, GROUND_LEVEL - 150])
                coins.append(Coin(coin_x, coin_y))

            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 10

                # Check collision with both players
                for player in players:
                    if player.alive and player.rect.colliderect(obstacle.rect):
                        player.alive = False
                        audio_manager.play_sound('hit')

            # Update coins (they scroll, but players can move to get them)
            for coin in coins[:]:
                coin.update()
                if coin.is_off_screen():
                    coins.remove(coin)

                # Check if either player collected the coin
                for player in players:
                    if player.alive and player.rect.colliderect(coin.rect) and not coin.collected:
                        coins.remove(coin)
                        score += 50
                        audio_manager.play_sound('coin')
                        break

            # Check if both players are dead
            if not player1.alive and not player2.alive:
                game_over = True
                # Award coins to account
                earned_coins = score // 20
                skin_manager.add_coins(earned_coins)

            # Level progression
            if score > 0 and score % 500 == 0:
                if score // 500 > level - 1:
                    level += 1
                    audio_manager.play_sound('level_up')

        # ===== DRAWING =====
        screen.fill(BG_COLOR)

        # Draw ground line
        pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL + 50), (SCREEN_WIDTH, GROUND_LEVEL + 50), 3)

        # Draw players
        for player in players:
            player.draw(screen)

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw coins
        for coin in coins:
            coin.draw(screen)

        # Draw UI
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        level_text = score_font.render(f"Level: {level}", True, BLACK)
        screen.blit(level_text, (10, 50))

        # Draw mode indicator
        mode_text = instruction_font.render("2-PLAYER MODE", True, PURPLE)
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 10))

        # Draw player controls (at bottom) - UPDATED
        p1_label = instruction_font.render("P1 (Red): W=Jump, S=Duck, A=Left, D=Right", True, RED)
        screen.blit(p1_label, (10, SCREEN_HEIGHT - 60))

        p2_label = instruction_font.render("P2 (Blue): ↑=Jump, ↓=Duck, ←=Left, →=Right", True, BLUE)
        screen.blit(p2_label, (10, SCREEN_HEIGHT - 30))

        # Draw player status (top right)
        p1_status_text = "ALIVE" if player1.alive else "DEAD"
        p1_status_colour = GREEN if player1.alive else RED
        p1_status = instruction_font.render(f"P1: {p1_status_text}", True, p1_status_colour)
        screen.blit(p1_status, (SCREEN_WIDTH - 120, 10))

        p2_status_text = "ALIVE" if player2.alive else "DEAD"
        p2_status_colour = GREEN if player2.alive else RED
        p2_status = instruction_font.render(f"P2: {p2_status_text}", True, p2_status_colour)
        screen.blit(p2_status, (SCREEN_WIDTH - 120, 40))

        # Draw pause hint
        if not game_over and not paused:
            pause_hint = instruction_font.render("ESC/P - Pause", True, GRAY)
            screen.blit(pause_hint, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 30))

        # ===== PAUSE SCREEN =====
        if paused and not game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            pause_text = game_over_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(pause_text, pause_rect)

            resume_text = instruction_font.render("Press ESC or P to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(resume_text, resume_rect)

            menu_text = instruction_font.render("Press M to return to menu", True, WHITE)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(menu_text, menu_rect)

        # ===== GAME OVER SCREEN =====
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(WHITE)
            screen.blit(overlay, (0, 0))

            game_over_text = game_over_font.render("GAME OVER", True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_over_text, game_over_rect)

            final_score_text = score_font.render(f"Final Score: {score}", True, BLACK)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(final_score_text, final_score_rect)

            earned_coins = score // 20
            coins_text = score_font.render(f"Coins Earned: {earned_coins}", True, GOLD)
            coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(coins_text, coins_rect)

            # Winner announcement
            if player1.alive and not player2.alive:
                winner_text = title_font.render("Player 1 (Red) Wins!", True, RED)
            elif player2.alive and not player1.alive:
                winner_text = title_font.render("Player 2 (Blue) Wins!", True, BLUE)
            else:
                winner_text = title_font.render("Both Players Defeated!", True, BLACK)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(winner_text, winner_rect)

            restart_text = instruction_font.render("Press R to Restart", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(restart_text, restart_rect)

            menu_text = instruction_font.render("Press M or ESC for Main Menu", True, BLACK)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(menu_text, menu_rect)

        pygame.display.flip()

    return  # Return to menu when loop ends