# EcoCatch - Earth Tech Project (Group 7)

EcoCatch is an educational Python mini-game focused on ecology.
The player must click falling waste before it hits the ground.

The project combines:
- Arcade gameplay (score, combo, lives, difficulty)
- Environmental awareness (decomposition times, educational messages)
- Per-session CO2 tracking with CodeCarbon

## Authors

Earth Tech Project - Group 7

| Name | Group |
|------|-------|
| Geoffrey DELRIEU | INT3 |
| Robin GOUMY | INT3 |
| Jery Razafindrabe | INT3 |
| Sacha Molliere | INT3 |
| Yanis Chaineray | INT3 |

## Gameplay Overview

- Waste appears and falls with simple physics (gravity + air resistance).
- Some waste can follow parabolic trajectories (higher difficulty).
- The player earns points by clicking waste.
- If waste hits the ground, one life is lost.
- The game ends when lives reach 0.

## Features

- Main menu: Play/Replay, Difficulty, Help, Quit
- Difficulty settings screen
- Visual effects (particles + floating text)
- HUD display (score, lives, combo)
- Educational messages and facts during gameplay
- CO2 tracking with CodeCarbon

## Prerequisites

- Python 3.10+
- Pip
- Windows, macOS, or Linux

## Installation

From the project root:

```bash
pip install pygame-ce codecarbon
```

## Run

From the project root:

```bash
python main.py
```

The `main.py` entry point imports modules from the `modules/` folder.

## Controls

- Mouse:
  - Click waste to catch it
  - Click menu buttons
- Keyboard:
  - `ESC` during gameplay: return to menu

## Project Structure

```text
earth-tech-prj-grp7/
|- assets/                 # Images, fonts, and visual resources
|- modules/
|  |- constant.py          # Global constants
|  |- dataHandler.py       # Data, objects, spawn, educational content
|  |- effect.py            # Visual effects (particles, floating text)
|  |- game.py              # Main game loop
|  |- screen.py            # Menus (launcher, help, difficulty)
|- main.py                 # Entry point + CodeCarbon tracking
|- README.md
```

## Carbon Footprint

When a session starts, a CodeCarbon tracker is launched automatically.
At the end of the session, estimated emissions are printed in the console.

