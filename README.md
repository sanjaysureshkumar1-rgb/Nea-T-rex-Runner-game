# Nea T-rex Runnergame

This project reimagines the offline Chrome Dino as an enhanced endless runner developed with Pygame. It introduces level progression, power-ups, unlockable skins, dynamic environments, improved visuals, sound effects, music, and a detailed scoring system with local leaderboards to enhance engagement and replayability.


## 📋 Table of Contents

- [About the Project]
- [Features]
- [Screenshots]
- [Getting Started]
- [How to Play]
- [Technologies Used]
- [Project Structure]

About the Project

The original Chrome T-Rex game was designed as a simple Easter egg for users without an internet connection. Whilst functional, it lacks variety, progression, and long-term engagement.

This project reimagines the classic endless runner with a full feature set — including unlockable skins, a coin economy, multiple game modes, a leaderboard, and dynamic level progression — transforming a throwaway minigame into a genuinely replayable experience.

Features 
- 🎮 **Single Player Mode** — Classic endless runner with increasing difficulty
- 👥 **2-Player Mode** — Local co-op on the same keyboard
- 📖 **Story Mode** — Five unique levels across different environments, each with its own objective
- 🏆 **Leaderboard** — Track high scores, total coins, and achievements
- 🦖 **Unlockable Skins** — Spend coins to customise your dinosaur
- 🏅 **Achievements System** — 15 achievements to unlock across all modes
- 🪙 **Coin Economy** — Collect coins during gameplay to spend in the skins shop
- ⚡ **Power-Ups** — Shield, Speed Boost, Double Jump, and Coin Magnet
- ⚙️ **Settings Menu** — Adjust music volume, sound effects, and view controls
- ⏸️ **Pause Functionality** — Pause and resume at any time


figure 1 - main menu 
<img width="1247" height="1047" alt="image" src="https://github.com/user-attachments/assets/0ac0d21f-b648-433c-a7d5-801e8617e6f0" />

[Figure 1 - Main Menu]

The main menu is the central hub of the game. From here, players can launch any game mode, access the skins shop, view achievements, check the leaderboard, or adjust settings. The player's total coin balance is displayed prominently beneath the title.

**Figure 2 — Single Player Gameplay**

![Figure 2 - Gameplay](assets/screenshots/figure2_gameplay.png)

The core single player gameplay loop. The player must dodge cacti and birds whilst collecting coins. The HUD displays the current score, high score, coin count, and level in real time. Difficulty increases as the level progresses.

---

**Figure 3 — 2-Player Mode**

![Figure 3 - 2 Player Mode](assets/screenshots/figure3_two_player.png)

Two-player local co-op on a shared screen. Player 1 (red) uses WASD and Player 2 (blue) uses the arrow keys. Each player's survival status is tracked independently in the top-right corner. The round ends when both players have been eliminated.

---

**Figure 4 — Pause Screen**

![Figure 4 - Paused](assets/screenshots/figure4_paused.png)

The pause screen overlays the current game state, freezing all action. Players can resume with `ESC` or `P`, or return to the main menu with `M`. Available in both single player and 2-player modes.

---

**Figure 5 — Story Mode: Level Select**

![Figure 5 - Level Select](assets/screenshots/figure5_level_select.png)

The Story Mode level select screen presents all five levels, each with a unique objective displayed beneath the button. Levels range from surviving in the desert to mastering all environments, offering a structured progression through the game.

---

**Figure 6 — Story Mode: Level 1 — Desert**

![Figure 6 - Level 1 Desert](assets/screenshots/figure6_level1_desert.png)

Level 1 takes place in a sandy desert environment with a scrolling mountain backdrop. The objective is to survive and accumulate a score of 1000. The HUD shows the current objective and live progress at the top of the screen.

---

**Figure 7 — Story Mode: Level 2 — Forest**

![Figure 7 - Level 2 Forest](assets/screenshots/figure7_level2_forest.png)

Level 2 switches the environment to a lush green forest with trees and grass. The objective changes to collecting 20 coins, adding a layer of strategy as players must actively chase coins whilst avoiding obstacles.

---

**Figure 8 — Story Mode: Level 3 — Arctic**

![Figure 8 - Level 3 Arctic](assets/screenshots/figure8_level3_arctic.png)

Level 3 is set in a snowy arctic environment with falling snowflakes and icy obstacles. The objective is to survive for 30 seconds, testing the player's endurance as the pace increases.

---

**Figure 9 — Story Mode: Level 4 — City**

![Figure 9 - Level 4 City](assets/screenshots/figure9_level4_city.png)

Level 4 takes place in a dark urban cityscape at night, complete with glowing building windows. The objective is to score 2000 points — the most demanding scoring challenge in Story Mode.

---

**Figure 10 — Story Mode: Level 5 — All Environments**

*Screenshot coming soon*

Level 5 is the final and most challenging story level. The objective is to master all environments, cycling through every biome in a single run. This level tests everything the player has learnt across the previous four stages.

---

**Figure 11 — Skins Shop**

![Figure 11 - Skins Shop](assets/screenshots/figure11_skins.png)

The skins shop allows players to spend their collected coins on cosmetic dinosaur colours. Unlocked skins are shown in grey, the currently equipped skin is highlighted in green, and locked skins display their coin cost in yellow. Skins range from 200 to 600+ coins.

---

**Figure 12 — Achievements**

![Figure 12 - Achievements](assets/screenshots/figure12_achievements.png)

The achievements screen tracks progress across 15 challenges, from basic milestones like "First Jump" to long-term goals like "Ultra Runner" and "Coin Master". Completed achievements are highlighted in green, with a progress bar at the top showing overall completion percentage.

---

**Figure 13 — Leaderboard**

![Figure 13 - Leaderboard](assets/screenshots/figure13_leaderboard.png)

The leaderboard provides a summary of the player's overall statistics — displaying their all-time high score, total coins collected, and number of achievements completed out of 15.

---

**Figure 14 — Settings**

![Figure 14 - Settings](assets/screenshots/figure14_settings.png)

The settings screen provides sliders to independently adjust music volume and sound effects. It also acts as a quick-reference guide, listing all controls and detailing the four power-ups available during gameplay.

---

**Figure 15 — Game Over Screen**

![Figure 15 - Game Over](assets/screenshots/figure15_game_over.png)

The game over screen displays the player's final score and coins earned in that run. Players can instantly restart with `SPACE` or return to the main menu with `ESC`.

---

## Getting Started

### Prerequisites

- Python 3.8 or above
- Pygame

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sanjaysureshkumar1-rgb/Nea-T-rex-Runner-game.git
   cd Nea-T-rex-Runner-game
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python main.py
   ```

---

## How to Play

### Single Player

| Key | Action |
|-----|--------|
| `SPACE` / `↑` | Jump |
| `↓` | Duck |
| `ESC` / `P` | Pause |

### 2-Player Mode

| Player | Jump | Duck | Move Left | Move Right |
|--------|------|------|-----------|------------|
| P1 (Red) | `W` | `S` | `A` | `D` |
| P2 (Blue) | `↑` | `↓` | `←` | `→` |

### Power-Ups

| Power-Up | Effect |
|----------|--------|
| 🛡️ Shield | Blocks one hit |
| ⚡ Speed Boost | Move faster and jump higher |
| 🔀 Double Jump | Jump again whilst in mid-air |
| 🧲 Coin Magnet | Automatically attracts nearby coins |

---

## Technologies Used

- **Language:** Python 3
- **Library:** Pygame


