import pygame
import random
import json
import os
from settings import *
from buttons import Button
from player import Player
from obstacles import Obstacle, ObstacleSpawner
from powerups import (
    PowerUp, PowerUpManager)
from skins import SkinManager, SkinDisplay
from audio import AudioManager, VolumeSlider
from achievements import AchievementManager, AchievementDisplay
from backgrounds import BackgroundManager
from two_player import two_player_game
from level_system import LevelManager

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced T-Rex Game")
clock = pygame.time.Clock()

# Game state
game_state = "MENU"
score = 0
high_score = 0
coins_collected_this_game = 0
level = 1
distance = 0
game_time = 0
paused = False

# Initialise managers
skin_manager = SkinManager()
audio_manager = AudioManager()
achievement_manager = AchievementManager()
power_up_manager = PowerUpManager()
obstacle_spawner = ObstacleSpawner()
background_manager = BackgroundManager()
level_manager = LevelManager()
use_level_system = False

# UI displays
skin_display = SkinDisplay(skin_manager)
achievement_display = AchievementDisplay(achievement_manager)

# Power-ups and obstacles
powerups_list = []
obstacles = []
coins_list = []

# Timers
powerup_spawn_timer = 0
obstacle_timer = 0
coin_timer = 0
powerups_collected_this_game = 0

# Initialise player
player = Player(100, GROUND_LEVEL)
if hasattr(player, 'set_skin_colour'):
    player.set_skin_colour(skin_manager.get_current_color())
if hasattr(player, 'set_power_up_manager'):
    player.set_power_up_manager(power_up_manager)

# Story mode
story_mode = False
story_level = 0
story_objectives = {
    1: {"name": "Desert", "desc": "Survive in the Desert", "target": 1000, "type": "distance", "environment": "desert"},
    2: {"name": "Jungle", "desc": "Collect 20 Coins", "target": 20, "type": "coins", "environment": "jungle"},
    3: {"name": "Ice Age", "desc": "Survive 30 seconds", "target": 1800, "type": "time", "environment": "ice"},
    4: {"name": "Future", "desc": "Score 2000 points", "target": 2000, "type": "score", "environment": "future"},
    5: {"name": "Master", "desc": "Master all environments", "target": 3000, "type": "distance", "environment": "night"}
}
story_progress = 0
story_timer = 0

# Menu buttons
start_button = Button(SCREEN_WIDTH // 2 - 100, 180, 200, 60, "Start Game", GREEN, DARK_GREEN)
two_player_button = Button(SCREEN_WIDTH // 2 - 100, 260, 200, 60, "2 Players", BLUE, (0, 80, 200))
platform_button = Button(SCREEN_WIDTH // 2 - 100, 340, 200, 60, "Platform Mode", (0, 200, 200), (0, 150, 150))
story_button = Button(SCREEN_WIDTH // 2 - 100, 420, 200, 60, "Story Mode", (255, 165, 0), (255, 140, 0))
skins_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 60, "Skins", (255, 105, 180), (255, 80, 150))
achievements_button = Button(SCREEN_WIDTH // 2 - 100, 580, 200, 60, "Achievements", PURPLE, (120, 80, 200))
leaderboard_button = Button(SCREEN_WIDTH // 2 - 100, 660, 200, 60, "Leaderboard", BLUE, (0, 80, 200))
settings_button = Button(20, SCREEN_HEIGHT - 70, 140, 50, "Settings", GRAY, (100, 100, 100))
quit_button = Button(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 70, 140, 50, "Quit", RED, (200, 0, 0))

# Back button
back_button = Button(20, 20, 100, 40, "Back", GRAY, (100, 100, 100))

# Pause menu buttons
resume_button = Button(SCREEN_WIDTH // 2 - 100, 200, 200, 60, "Resume", GREEN, DARK_GREEN)
restart_button = Button(SCREEN_WIDTH // 2 - 100, 280, 200, 60, "Restart", (255, 165, 0), (255, 140, 0))
menu_button = Button(SCREEN_WIDTH // 2 - 100, 360, 200, 60, "Main Menu", BLUE, (0, 80, 200))
pause_quit_button = Button(SCREEN_WIDTH // 2 - 100, 440, 200, 60, "Quit Game", RED, (200, 0, 0))

# Level select buttons
level_buttons = []
for i in range(5):
    row = i // 3
    col = i % 3
    x = SCREEN_WIDTH // 2 - 200 + col * 150
    y = 180 + row * 100
    level_buttons.append(Button(x, y, 120, 70, f"Level {i + 1}", BLUE, (0, 100, 255)))

# Settings volume sliders
music_slider = VolumeSlider(SCREEN_WIDTH // 2 - 150, 200, 300, 30, "Music Volume", 0.5)
sfx_slider = VolumeSlider(SCREEN_WIDTH // 2 - 150, 280, 300, 30, "Sound Effects", 0.7)


def load_game_data():
    """Load saved game data"""
    try:
        if os.path.exists("game_data.json"):
            with open("game_data.json", "r") as f:
                data = json.load(f)

                # Load high score
                global high_score
                high_score = data.get("high_score", 0)

                # Load skin data
                skin_manager.load_data(data.get("skin_data", {}))

                # Load achievement data
                achievement_manager.load_data(data.get("achievement_data", {}))

                # Load audio settings
                if "audio_settings" in data:
                    audio_manager.set_music_volume(data["audio_settings"].get("music_volume", 0.5))
                    audio_manager.set_sfx_volume(data["audio_settings"].get("sfx_volume", 0.7))
                    music_slider.value = audio_manager.get_music_volume()
                    sfx_slider.value = audio_manager.get_sfx_volume()

                # Update player with loaded skin
                if hasattr(player, 'set_skin_colour'):
                    player.set_skin_colour(skin_manager.get_current_color())
    except Exception as e:
        print(f"Could not load game data: {e}")


def save_game_data():
    """Save game data to file"""
    try:
        data = {
            "high_score": high_score,
            "skin_data": skin_manager.save_data(),
            "achievement_data": achievement_manager.save_data(),
            "audio_settings": {
                "music_volume": audio_manager.get_music_volume(),
                "sfx_volume": audio_manager.get_sfx_volume()
            }
        }

        with open("game_data.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Could not save game data: {e}")


def reset_game():
    """Reset all game variables for new game"""
    global player, obstacles, score, obstacle_timer, level, distance
    global story_progress, story_timer, coin_timer, power_up_manager
    global powerups_list, powerup_spawn_timer, coins_list, coins_collected_this_game
    global game_time, powerups_collected_this_game, use_level_system

    # Create new power-up manager
    power_up_manager = PowerUpManager()

    # Reset player
    player = Player(100, GROUND_LEVEL)
    if hasattr(player, 'set_skin_colour'):
        player.set_skin_colour(skin_manager.get_current_color())
    if hasattr(player, 'set_power_up_manager'):
        player.set_power_up_manager(power_up_manager)

    obstacles = []
    powerups_list = []
    coins_list = []
    score = 0
    obstacle_timer = 0
    coin_timer = 0
    powerup_spawn_timer = 0
    distance = 0
    story_progress = 0
    story_timer = 0
    game_time = 0
    coins_collected_this_game = 0
    powerups_collected_this_game = 0

    # Set up platform or normal mode
    if use_level_system:
        level_manager.load_level(0)
        if hasattr(player, 'set_platforms'):
            player.set_platforms(level_manager.get_current_level().get_platforms())
    else:
        if hasattr(player, 'disable_platforms'):
            player.disable_platforms()
        # Set background based on mode
        if story_mode and story_level > 0:
            level_obj = story_objectives.get(story_level)
            if level_obj and "environment" in level_obj:
                background_manager.set_environment(level_obj["environment"])
        else:
            background_manager.set_level_environment(level)
            level = 1


def spawn_obstacle():
    """Spawn an obstacle appropriate for current level"""
    return obstacle_spawner.spawn(level)


def spawn_coin():
    """Spawn a coin at random height"""
    return {
        "x": SCREEN_WIDTH,
        "y": GROUND_LEVEL - random.randint(50, 150),
        "collected": False
    }


def spawn_powerup():
    """Spawn a random power-up"""
    powerup_types = ["shield", "speed", "double_jump", "coin_magnet"]
    powerup_type = random.choice(powerup_types)
    y_position = GROUND_LEVEL - random.randint(80, 150)
    return PowerUp(SCREEN_WIDTH, y_position, powerup_type)


# Load saved data on startup
load_game_data()

# Start background music
audio_manager.play_music()

# Main game loop
run = True
while run:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data()
            run = False

        # Handle mouse wheel scrolling
        if event.type == pygame.MOUSEWHEEL:
            if game_state == "SKINS":
                skin_display.handle_scroll(event.y)
            elif game_state == "ACHIEVEMENTS":
                achievement_display.handle_scroll(event.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if start_button.is_clicked(mouse_pos):
                    story_mode = False
                    use_level_system = False
                    game_state = "PLAYING"
                    reset_game()
                    audio_manager.play_sound('level_up')
                elif two_player_button.is_clicked(mouse_pos):
                    two_player_game(screen, clock, audio_manager, skin_manager)
                    game_state = "MENU"
                elif platform_button.is_clicked(mouse_pos):
                    use_level_system = True
                    story_mode = False
                    game_state = "PLAYING"
                    reset_game()
                    if hasattr(player, 'set_platforms'):
                        player.set_platforms(level_manager.get_current_level().get_platforms())
                    audio_manager.play_sound('level_up')
                elif story_button.is_clicked(mouse_pos):
                    game_state = "LEVEL_SELECT"
                elif skins_button.is_clicked(mouse_pos):
                    game_state = "SKINS"
                elif achievements_button.is_clicked(mouse_pos):
                    game_state = "ACHIEVEMENTS"
                elif leaderboard_button.is_clicked(mouse_pos):
                    game_state = "LEADERBOARD"
                elif settings_button.is_clicked(mouse_pos):
                    game_state = "SETTINGS"
                elif quit_button.is_clicked(mouse_pos):
                    save_game_data()
                    run = False

            elif game_state == "LEVEL_SELECT":
                for i, btn in enumerate(level_buttons):
                    if btn.is_clicked(mouse_pos):
                        story_mode = True
                        story_level = i + 1
                        use_level_system = False
                        game_state = "PLAYING"
                        reset_game()
                        audio_manager.play_sound('level_up')
                        break
                if back_button.is_clicked(mouse_pos):
                    game_state = "MENU"

            elif game_state == "SKINS":
                if back_button.is_clicked(mouse_pos):
                    game_state = "MENU"
                    save_game_data()
                    if hasattr(player, 'set_skin_colour'):
                        player.set_skin_colour(skin_manager.get_current_color())
                else:
                    if skin_display.handle_click(mouse_pos):
                        if hasattr(player, 'set_skin_colour'):
                            player.set_skin_colour(skin_manager.get_current_color())
                        audio_manager.play_sound('coin')

            elif game_state == "ACHIEVEMENTS":
                if back_button.is_clicked(mouse_pos):
                    game_state = "MENU"

            elif game_state == "LEADERBOARD":
                if back_button.is_clicked(mouse_pos):
                    game_state = "MENU"

            elif game_state == "SETTINGS":
                if back_button.is_clicked(mouse_pos):
                    game_state = "MENU"
                    save_game_data()

        # Handle pause menu clicks
        if game_state == "PLAYING" and paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_clicked(mouse_pos):
                    paused = False
                    audio_manager.play_sound('coin')
                elif restart_button.is_clicked(mouse_pos):
                    paused = False
                    reset_game()
                    audio_manager.play_sound('level_up')
                elif menu_button.is_clicked(mouse_pos):
                    paused = False
                    game_state = "MENU"
                    save_game_data()
                    audio_manager.play_sound('level_up')
                elif pause_quit_button.is_clicked(mouse_pos):
                    save_game_data()
                    run = False

        if game_state == "PLAYING" and player is not None and not paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                    audio_manager.play_sound('jump')
                if event.key == pygame.K_DOWN:
                    player.duck()
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.stand_up()

        # Allow resume from keyboard when paused
        if game_state == "PLAYING" and paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = False

    screen.fill(BG_COLOR)

    # ===== MENU STATE =====
    if game_state == "MENU":
        # Title
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("T-REX RUNNER", True, BLACK)
        title_shadow = title_font.render("T-REX RUNNER", True, TEXT_SHADOW)
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 53))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display total coins
        coin_text = pygame.font.Font(None, 40).render(f"Total Coins: {skin_manager.total_coins}", True, GOLD)
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, 120))

        # Update and draw buttons
        start_button.update(mouse_pos)
        two_player_button.update(mouse_pos)
        platform_button.update(mouse_pos)
        story_button.update(mouse_pos)
        skins_button.update(mouse_pos)
        achievements_button.update(mouse_pos)
        leaderboard_button.update(mouse_pos)
        settings_button.update(mouse_pos)
        quit_button.update(mouse_pos)

        start_button.draw(screen)
        two_player_button.draw(screen)
        platform_button.draw(screen)
        story_button.draw(screen)
        skins_button.draw(screen)
        achievements_button.draw(screen)
        leaderboard_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

    # ===== LEVEL SELECT STATE =====
    elif game_state == "LEVEL_SELECT":
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("SELECT LEVEL", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, btn in enumerate(level_buttons):
            btn.update(mouse_pos)
            btn.draw(screen)

            obj = story_objectives[i + 1]
            desc_font = pygame.font.Font(None, 20)
            desc_text = desc_font.render(obj["desc"], True, BLACK)
            screen.blit(desc_text, (btn.rect.centerx - desc_text.get_width() // 2, btn.rect.bottom + 5))

        back_button.update(mouse_pos)
        back_button.draw(screen)

    # ===== SKINS STATE =====
    elif game_state == "SKINS":
        skin_display.draw(screen)
        back_button.update(mouse_pos)
        back_button.draw(screen)

    # ===== ACHIEVEMENTS STATE =====
    elif game_state == "ACHIEVEMENTS":
        achievement_display.draw(screen)
        back_button.update(mouse_pos)
        back_button.draw(screen)

    # ===== PLAYING STATE =====
    elif game_state == "PLAYING" and player is not None:
        # Check if game is paused
        if paused:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Draw pause title
            pause_font = pygame.font.Font(None, 100)
            pause_text = pause_font.render("PAUSED", True, WHITE)
            pause_shadow = pause_font.render("PAUSED", True, TEXT_SHADOW)
            screen.blit(pause_shadow, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2 + 3, 73))
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 70))

            # Draw pause instructions
            instruction_font = pygame.font.Font(None, 30)
            instruction_text = instruction_font.render("Press ESC or P to resume", True, WHITE)
            screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 150))

            # Update and draw pause menu buttons
            resume_button.update(mouse_pos)
            restart_button.update(mouse_pos)
            menu_button.update(mouse_pos)
            pause_quit_button.update(mouse_pos)

            resume_button.draw(screen)
            restart_button.draw(screen)
            menu_button.draw(screen)
            pause_quit_button.draw(screen)

        else:
            # Normal gameplay (only update if not paused)

            if use_level_system:
                # ========== PLATFORM MODE ==========
                screen.fill((135, 206, 235))  # Sky blue background

                current_level = level_manager.get_current_level()
                current_level.draw(screen)

                # Update player platforms
                if hasattr(player, 'set_platforms'):
                    player.set_platforms(level_manager.get_current_level().get_platforms())

                # Update game time and power-ups
                game_time += 1
                power_up_manager.update()

                # Update player
                player.update()
                player.draw(screen)

                distance += 1

                # Update achievements
                achievement_manager.update_progress('distance', distance)
                achievement_manager.update_progress('time', game_time)

                # Check coin collection
                for coin_tile in current_level.coins[:]:
                    if player.rect.colliderect(coin_tile.rect):
                        current_level.remove_coin(coin_tile.rect)
                        coins_collected_this_game += 1
                        score += COIN_COLLECT_POINTS
                        audio_manager.play_sound('coin')

                # Check powerup collection
                for powerup_tile in current_level.powerups[:]:
                    if player.rect.colliderect(powerup_tile.rect):
                        current_level.remove_powerup(powerup_tile.rect)
                        ptype = random.choice(['shield', 'speed', 'double_jump'])
                        power_up_manager.activate(ptype, 300)
                        score += POWERUP_COLLECT_POINTS
                        powerups_collected_this_game += 1
                        audio_manager.play_sound('powerup')

                # Check obstacle collision
                for obstacle_tile in current_level.obstacles:
                    if player.rect.colliderect(obstacle_tile.rect):
                        if power_up_manager.is_active('shield'):
                            power_up_manager.deactivate('shield')
                            audio_manager.play_sound('shield_break')
                            score += SHIELD_BLOCK_POINTS
                        else:
                            game_state = "GAME_OVER"
                            audio_manager.play_sound('hit')
                            if score > high_score:
                                high_score = score
                            skin_manager.add_coins(coins_collected_this_game)
                            achievement_manager.update_progress('score', score)
                            achievement_manager.update_progress('coins_game', coins_collected_this_game)
                            achievement_manager.update_progress('coins_total', skin_manager.total_coins)
                            achievement_manager.update_progress('powerups_game', powerups_collected_this_game)
                            save_game_data()

            else:
                # ========== NORMAL MODE ==========
                background_manager.update()
                background_manager.draw(screen)

                # Draw ground line
                pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL + 60), (SCREEN_WIDTH, GROUND_LEVEL + 60), 3)

                # Update game time
                game_time += 1

                # Update power-up manager
                power_up_manager.update()

                # Update player
                player.update()
                player.draw(screen)

                distance += 1

                # Update achievements
                achievement_manager.update_progress('distance', distance)
                achievement_manager.update_progress('time', game_time)
                achievement_manager.update_progress('level', level)

                # Spawn obstacles
                obstacle_timer += 1
                if obstacle_timer > 90:
                    obstacles.append(spawn_obstacle())
                    obstacle_timer = 0

                # Spawn coins
                coin_timer += 1
                if coin_timer > 120:
                    coins_list.append(spawn_coin())
                    coin_timer = 0

                # Spawn power-ups
                powerup_spawn_timer += 1
                if powerup_spawn_timer > POWERUP_SPAWN_RATE:
                    powerups_list.append(spawn_powerup())
                    powerup_spawn_timer = 0

                # Update obstacles
                for obstacle in obstacles[:]:
                    obstacle.update()
                    obstacle.draw(screen)

                    if obstacle.is_off_screen():
                        obstacles.remove(obstacle)
                        score += OBSTACLE_DODGE_POINTS

                    # Collision detection
                    if player.rect.colliderect(obstacle.rect):
                        if power_up_manager.is_active('shield'):
                            power_up_manager.deactivate('shield')
                            obstacles.remove(obstacle)
                            score += SHIELD_BLOCK_POINTS
                            audio_manager.play_sound('shield_break')
                        else:
                            game_state = "GAME_OVER"
                            audio_manager.play_sound('hit')
                            if score > high_score:
                                high_score = score

                            # Award coins and update achievements
                            skin_manager.add_coins(coins_collected_this_game)
                            achievement_manager.update_progress('score', score)
                            achievement_manager.update_progress('coins_game', coins_collected_this_game)
                            achievement_manager.update_progress('coins_total', skin_manager.total_coins)
                            achievement_manager.update_progress('powerups_game', powerups_collected_this_game)

                            save_game_data()

                # Coin magnet range
                magnet_range = 100 if power_up_manager.is_active('coin_magnet') else 0

                # Update coins
                for coin in coins_list[:]:
                    coin["x"] -= 5

                    # Magnet effect
                    if magnet_range > 0:
                        distance_to_player = ((coin["x"] - player.x) ** 2 + (coin["y"] - player.y) ** 2) ** 0.5
                        if distance_to_player < magnet_range:
                            dx = player.x - coin["x"]
                            dy = player.y - coin["y"]
                            coin["x"] += dx * 0.15
                            coin["y"] += dy * 0.15

                    # Draw coin
                    pygame.draw.circle(screen, GOLD, (int(coin["x"]), int(coin["y"])), 15)
                    pygame.draw.circle(screen, BLACK, (int(coin["x"]), int(coin["y"])), 15, 2)

                    # Collision
                    coin_rect = pygame.Rect(coin["x"] - 15, coin["y"] - 15, 30, 30)
                    if player.rect.colliderect(coin_rect) and not coin["collected"]:
                        coin["collected"] = True
                        coins_collected_this_game += 1
                        score += COIN_COLLECT_POINTS
                        coins_list.remove(coin)
                        audio_manager.play_sound('coin')
                    elif coin["x"] < -30:
                        coins_list.remove(coin)

                # Update power-ups
                for powerup in powerups_list[:]:
                    powerup.update()
                    powerup.draw(screen)

                    if powerup.is_off_screen():
                        powerups_list.remove(powerup)

                    powerup_rect = pygame.Rect(powerup.x, powerup.y, powerup.width, powerup.height)
                    if player.rect.colliderect(powerup_rect):
                        power_up_manager.activate(powerup.powerup_type, powerup.duration)
                        powerups_list.remove(powerup)
                        score += POWERUP_COLLECT_POINTS
                        powerups_collected_this_game += 1
                        audio_manager.play_sound('powerup')

                # Level progression
                if score >= level * POINTS_PER_LEVEL:
                    level += 1
                    background_manager.set_level_environment(level)
                    audio_manager.play_sound('level_up')

                # Story mode progress
                if story_mode:
                    story_timer += 1
                    obj = story_objectives[story_level]

                    if obj["type"] == "distance":
                        story_progress = distance
                    elif obj["type"] == "coins":
                        story_progress = coins_collected_this_game
                    elif obj["type"] == "time":
                        story_progress = story_timer
                    elif obj["type"] == "score":
                        story_progress = score

                    if story_progress >= obj["target"]:
                        game_state = "VICTORY"
                        skin_manager.add_coins(coins_collected_this_game + 100)
                        save_game_data()

            # Draw UI (common for both modes)
            score_font = pygame.font.Font(None, 40)
            score_text = score_font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            high_score_text = score_font.render(f"High Score: {high_score}", True, BLACK)
            screen.blit(high_score_text, (10, 50))

            coin_text = score_font.render(f"Coins: {coins_collected_this_game}", True, BLACK)
            screen.blit(coin_text, (10, 90))

            # Power-up indicators
            power_up_manager.draw_indicators(screen, 10, 140)

            # Level display
            if not story_mode and not use_level_system:
                level_text = score_font.render(f"Level: {level}", True, BLACK)
                screen.blit(level_text, (SCREEN_WIDTH - 200, 10))

            # Story mode objective
            if story_mode:
                obj = story_objectives[story_level]
                obj_font = pygame.font.Font(None, 35)
                obj_text = obj_font.render(f"Objective: {obj['desc']}", True, BLACK)
                screen.blit(obj_text, (SCREEN_WIDTH // 2 - obj_text.get_width() // 2, 10))

                progress_text = obj_font.render(f"Progress: {story_progress}/{obj['target']}", True, BLACK)
                screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 45))

            # Draw achievement notifications
            achievement_manager.draw_notification(screen)

            # Draw pause hint in corner (only when not paused)
            hint_font = pygame.font.Font(None, 24)
            hint_text = hint_font.render("ESC/P - Pause", True, GRAY)
            screen.blit(hint_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))

    # ===== VICTORY STATE =====
    elif game_state == "VICTORY":
        victory_font = pygame.font.Font(None, 80)
        victory_text = victory_font.render("VICTORY!", True, GREEN)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 200))

        obj = story_objectives[story_level]
        complete_font = pygame.font.Font(None, 40)
        complete_text = complete_font.render(f"Level {story_level} Complete!", True, BLACK)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 300))

        coins_earned = complete_font.render(f"Coins Earned: {coins_collected_this_game + 100}", True, GOLD)
        screen.blit(coins_earned, (SCREEN_WIDTH // 2 - coins_earned.get_width() // 2, 350))

        restart_font = pygame.font.Font(None, 35)
        restart_text = restart_font.render("Press SPACE for menu", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 450))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "MENU"

    # ===== GAME OVER STATE =====
    elif game_state == "GAME_OVER":
        game_over_font = pygame.font.Font(None, 80)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))

        final_score_font = pygame.font.Font(None, 50)
        final_score_text = final_score_font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 300))

        coins_earned = final_score_font.render(f"Coins Earned: {coins_collected_this_game}", True, GOLD)
        screen.blit(coins_earned, (SCREEN_WIDTH // 2 - coins_earned.get_width() // 2, 350))

        restart_font = pygame.font.Font(None, 40)
        restart_text = restart_font.render("Press SPACE to restart or ESC for menu", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 450))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "PLAYING"
            reset_game()
        if keys[pygame.K_ESCAPE]:
            game_state = "MENU"

    # ===== LEADERBOARD STATE =====
    elif game_state == "LEADERBOARD":
        text = pygame.font.Font(None, 50).render("LEADERBOARD", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        high_score_display = pygame.font.Font(None, 40).render(f"High Score: {high_score}", True, BLACK)
        screen.blit(high_score_display, (SCREEN_WIDTH // 2 - high_score_display.get_width() // 2, 200))

        total_coins_display = pygame.font.Font(None, 40).render(
            f"Total Coins: {skin_manager.total_coins}", True, GOLD
        )
        screen.blit(total_coins_display, (SCREEN_WIDTH // 2 - total_coins_display.get_width() // 2, 250))

        achievements_earned = pygame.font.Font(None, 40).render(
            f"Achievements: {len(achievement_manager.get_unlocked_achievements())}/{len(achievement_manager.achievements)}",
            True, BLACK
        )
        screen.blit(achievements_earned, (SCREEN_WIDTH // 2 - achievements_earned.get_width() // 2, 300))

        back_button.update(mouse_pos)
        back_button.draw(screen)

    # ===== SETTINGS STATE =====
    elif game_state == "SETTINGS":
        text = pygame.font.Font(None, 50).render("SETTINGS", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 80))

        # Update sliders
        if music_slider.update(mouse_pos, mouse_pressed):
            audio_manager.set_music_volume(music_slider.value)

        if sfx_slider.update(mouse_pos, mouse_pressed):
            audio_manager.set_sfx_volume(sfx_slider.value)

        # Draw sliders
        music_slider.draw(screen)
        sfx_slider.draw(screen)

        # Controls info
        info_font = pygame.font.Font(None, 30)
        controls_text = [
            "",
            "Controls:",
            "SPACE/UP - Jump",
            "DOWN - Duck",
            "ESC/P - Pause",
            "",
            "Power-Ups:",
            "Shield - Blocks one hit",
            "Speed Boost - Move faster & jump higher",
            "Double Jump - Jump in mid-air",
            "Coin Magnet - Attract coins"
        ]

        y_pos = 350
        for line in controls_text:
            text_surface = info_font.render(line, True, BLACK)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, y_pos))
            y_pos += 30

        back_button.update(mouse_pos)
        back_button.draw(screen)

    pygame.display.update()

pygame.quit()