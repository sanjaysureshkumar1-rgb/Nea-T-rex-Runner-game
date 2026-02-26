import pygame
import os
import math

# Initialize Pygame
pygame.init()

# Create assets folder if it doesn't exist
os.makedirs("assets/images", exist_ok=True)

WIDTH, HEIGHT = 850, 765


def create_cartoon_desert() -> object:
    """Create a vibrant cartoon desert background"""
    surface = pygame.Surface((WIDTH, HEIGHT))

    # === SKY - Beautiful gradient from light blue to peachy orange ===
    for y in range(int(HEIGHT * 0.6)):
        # Create smooth gradient
        progress = y / (HEIGHT * 0.6)

        # Sky colors: light blue at top, peachy orange at horizon
        r = int(135 + progress * 120)  # 135 -> 255
        g = int(206 - progress * 56)  # 206 -> 150
        b = int(235 - progress * 135)  # 235 -> 100

        color = (min(255, r), max(0, g), max(0, b))
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

    # === SAND DUNES - Multiple layers for depth ===

    # Back layer dunes (lighter, further away)
    back_dune_color = (237, 201, 175)
    for i in range(4):
        x_start = i * 250 - 100
        points = []
        for x in range(x_start, x_start + 350, 10):
            wave = 40 * math.sin((x + i * 100) * 0.01)
            y = int(HEIGHT * 0.5 + wave)
            points.append((x, y))
        points.append((x_start + 350, HEIGHT))
        points.append((x_start, HEIGHT))
        if len(points) > 3:
            pygame.draw.polygon(surface, back_dune_color, points)

    # Middle layer dunes (medium tan)
    mid_dune_color = (218, 165, 105)
    for i in range(3):
        x_start = i * 300
        points = []
        for x in range(x_start, x_start + 400, 10):
            wave = 60 * math.sin((x + i * 150) * 0.008)
            y = int(HEIGHT * 0.55 + wave)
            points.append((x, y))
        points.append((x_start + 400, HEIGHT))
        points.append((x_start, HEIGHT))
        if len(points) > 3:
            pygame.draw.polygon(surface, mid_dune_color, points)

    # Front layer dunes (darker, closest)
    front_dune_color = (194, 143, 92)
    for i in range(3):
        x_start = i * 280 + 50
        points = []
        for x in range(x_start, x_start + 380, 10):
            wave = 50 * math.sin((x + i * 120) * 0.012)
            y = int(HEIGHT * 0.62 + wave)
            points.append((x, y))
        points.append((x_start + 380, HEIGHT))
        points.append((x_start, HEIGHT))
        if len(points) > 3:
            pygame.draw.polygon(surface, front_dune_color, points)

    # === SUN - Big beautiful sun with glow ===
    sun_x, sun_y = 680, 120

    # Glow effect (multiple circles)
    for i in range(5, 0, -1):
        alpha_glow = 255 - (i * 30)
        glow_color = (255, 240 - i * 10, 100 - i * 15)
        pygame.draw.circle(surface, glow_color, (sun_x, sun_y), 50 + i * 8)

    # Main sun body
    pygame.draw.circle(surface, (255, 223, 0), (sun_x, sun_y), 50)

    # Sun highlight (makes it look more 3D)
    pygame.draw.circle(surface, (255, 255, 150), (sun_x - 15, sun_y - 15), 20)

    # Sun outline
    pygame.draw.circle(surface, (255, 200, 0), (sun_x, sun_y), 50, 3)

    # === CLOUDS - Puffy cartoon clouds ===
    cloud_color = (255, 255, 255)
    clouds = [
        (120, 100, [(0, 0, 35), (30, -5, 30), (55, 0, 32), (25, 15, 25)]),
        (350, 140, [(0, 0, 30), (25, -8, 28), (50, -3, 30), (30, 12, 22)]),
        (580, 90, [(0, 0, 38), (35, -10, 32), (65, 0, 35), (35, 18, 28)]),
    ]

    for cloud_x, cloud_y, circles in clouds:
        # Draw cloud puffs
        for cx, cy, radius in circles:
            pygame.draw.circle(surface, cloud_color, (cloud_x + cx, cloud_y + cy), radius)

        # Outline for depth
        for cx, cy, radius in circles:
            pygame.draw.circle(surface, (230, 230, 230), (cloud_x + cx, cloud_y + cy), radius, 2)

    # === CACTI - Detailed cartoon cacti in background ===
    cacti_positions = [
        (100, HEIGHT * 0.55, 25, 70),  # (x, y, width, height)
        (250, HEIGHT * 0.58, 20, 55),
        (450, HEIGHT * 0.56, 30, 80),
        (650, HEIGHT * 0.59, 22, 60),
        (780, HEIGHT * 0.57, 28, 75),
    ]

    for cactus_x, cactus_y, cactus_w, cactus_h in cacti_positions:
        cactus_x = int(cactus_x)
        cactus_y = int(cactus_y)

        # Main body (darker green)
        body_color = (34, 139, 34)
        pygame.draw.rect(surface, body_color,
                         (cactus_x, cactus_y, cactus_w, int(cactus_h)),
                         border_radius=8)

        # Left arm
        arm_w = int(cactus_w * 0.6)
        arm_h = int(cactus_h * 0.4)
        pygame.draw.rect(surface, body_color,
                         (cactus_x - arm_w + 5, cactus_y + int(cactus_h * 0.3),
                          arm_w, arm_h),
                         border_radius=6)
        # Connector
        pygame.draw.rect(surface, body_color,
                         (cactus_x, cactus_y + int(cactus_h * 0.3),
                          arm_w // 2, arm_h // 2),
                         border_radius=4)

        # Right arm
        pygame.draw.rect(surface, body_color,
                         (cactus_x + cactus_w - 5, cactus_y + int(cactus_h * 0.45),
                          arm_w, int(arm_h * 0.8)),
                         border_radius=6)
        # Connector
        pygame.draw.rect(surface, body_color,
                         (cactus_x + cactus_w - arm_w // 2, cactus_y + int(cactus_h * 0.45),
                          arm_w // 2, arm_h // 2),
                         border_radius=4)

        # Spikes/needles (small lines)
        spike_color = (0, 100, 0)
        for spike_y in range(int(cactus_y), int(cactus_y + cactus_h), 12):
            # Left side spikes
            pygame.draw.line(surface, spike_color,
                             (cactus_x, spike_y),
                             (cactus_x - 5, spike_y), 2)
            # Right side spikes
            pygame.draw.line(surface, spike_color,
                             (cactus_x + cactus_w, spike_y),
                             (cactus_x + cactus_w + 5, spike_y), 2)

        # Outline
        pygame.draw.rect(surface, (0, 100, 0),
                         (cactus_x, cactus_y, cactus_w, int(cactus_h)),
                         3, border_radius=8)

    # === SMALL ROCKS - scattered on ground ===
    rock_color = (139, 90, 43)
    rocks = [
        (200, HEIGHT * 0.7, 15, 10),
        (320, HEIGHT * 0.68, 20, 12),
        (500, HEIGHT * 0.72, 12, 8),
        (650, HEIGHT * 0.69, 18, 11),
    ]

    for rock_x, rock_y, rock_w, rock_h in rocks:
        pygame.draw.ellipse(surface, rock_color,
                            (int(rock_x), int(rock_y), rock_w, rock_h))
        pygame.draw.ellipse(surface, (100, 70, 30),
                            (int(rock_x), int(rock_y), rock_w, rock_h), 2)

    # === TUMBLEWEEDS - small cartoon tumbleweeds ===
    tumbleweed_color = (160, 120, 60)
    tumbleweeds = [(400, HEIGHT * 0.65, 20), (600, HEIGHT * 0.67, 18)]

    for tw_x, tw_y, tw_size in tumbleweeds:
        # Draw circular tumbleweed with lines
        pygame.draw.circle(surface, tumbleweed_color,
                           (int(tw_x), int(tw_y)), tw_size)
        # Cross lines
        for angle in range(0, 360, 45):
            end_x = tw_x + tw_size * 0.8 * math.cos(math.radians(angle))
            end_y = tw_y + tw_size * 0.8 * math.sin(math.radians(angle))
            pygame.draw.line(surface, (130, 90, 40),
                             (int(tw_x), int(tw_y)),
                             (int(end_x), int(end_y)), 2)

    # Save the image
    pygame.image.save(surface, "assets/images/desert.png")
    print("\n" + "=" * 50)
    print("✓ DESERT BACKGROUND CREATED SUCCESSFULLY!")
    print("=" * 50)
    print("📁 Saved to: assets/images/desert.png")
    print(f"📐 Size: {WIDTH}x{HEIGHT} pixels")
    print("\n🎨 Features included:")
    print("  • Beautiful sky gradient (blue to orange)")
    print("  • Layered sand dunes for depth")
    print("  • Glowing sun with highlights")
    print("  • Puffy cartoon clouds")
    print("  • Detailed cacti with arms and spikes")
    print("  • Rocks and tumbleweeds")
    print("\n✅ Ready to use in your game!")
    print("=" * 50 + "\n")


# Generate the desert background
print("\n🏜️  Generating Cartoon Desert Background...")
create_cartoon_desert()
pygame.quit()

print("🎮 To test it in your game:")
print("   1. Make sure this file created: assets/images/desert.png")
print("   2. Run your main.py")
print("   3. Start Story Mode → Select Level 1 (Desert)")
print("   4. Enjoy your new background!\n")