<<<<<<< Updated upstream
# EcoCatch - Earth Tech Project (Group 7)

EcoCatch is an educational Python/Pygame mini-game where the player must click on falling waste before it hits the ground.

The project combines:
- fast arcade gameplay (score, combo, lives, difficulty)
- environmental awareness (decomposition times, educational messages)
- carbon footprint tracking per session (CodeCarbon)

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

- Waste appears on screen and falls with simple physics (gravity + air resistance).
- Some waste can be thrown in parabolic trajectories (higher difficulty).
- The player earns points by clicking waste:
  - +10 points (normal)
  - +20 points (combo >= 3)
  - +30 points (combo >= 5)
- When waste hits the ground, the player loses one life.
- The game ends when lives reach 0.

## Features

- Main menu: Play/Replay, Difficulty, Help, Quit
- Difficulty settings screen (gravity, speeds, parabolic chance)
- Visual feedback effects: particles + floating text
- HUD display: score, lives, combo
- Educational messages and eco facts during gameplay
- CO2 emissions tracking for each session via CodeCarbon

## Technologies

- Python 3
- Pygame
- CodeCarbon

## Prerequisites

- Windows (tested in this environment)
- Python 3.10+ recommended
- Pip

## Installation

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install pygame codecarbon
```

## Run the Project

The entry point is `main.py` inside the `code` folder.

From the project root:

```bash
cd code
python main.py
```

## Controls

- Mouse:
  - Click waste to catch it
  - Click menu buttons
- Keyboard:
  - `ESC` during gameplay: return to menu

## Project Structure

```text
earth-tech-prj-grp7/
|- assets/                 # Images and visual resources
|- code/
|  |- main.py              # Entry point + CodeCarbon tracking
|  |- screen.py            # Menus (launcher, help, difficulty)
|  |- game.py              # Main game loop
|  |- dataHandler.py       # Player, objects, spawn, educational data
|  |- effect.py            # Visual effects (particles, floating text)
|  |- constant.py          # Global constants
|  |- emissions.csv        # Local history of CodeCarbon sessions
|- README.md
```

## Educational Content

The game includes educational information about:
- waste types
- decomposition times
- environmental awareness messages

## Carbon Footprint

When a game session starts, a CodeCarbon tracker is launched automatically.
At the end of the session, emissions are printed in the console and saved in `code/emissions.csv`.

=======
# Earth Tech

Jeu Python sur le thème de l'écologie, réalisé avec `pygame-ce`.

## Prérequis
- Python 3.13 ou plus récent
- Windows, macOS ou Linux

## Installation
1. Ouvre un terminal dans le dossier du projet.
2. Installe les dépendances nécessaires :

```bash
python -m pip install pygame-ce codecarbon
```

Si tu préfères utiliser un environnement virtuel, crée-le d'abord puis installe les paquets dedans.

## Lancement
Depuis la racine du projet, lance :

```bash
python main.py
```

Le point d'entrée importe le jeu depuis le dossier `modules/`, donc il faut lancer le script depuis la racine du projet et pas directement depuis un sous-dossier.

## Structure du projet
- `main.py` : point d'entrée
- `modules/constant.py` : constantes globales
- `modules/dataHandler.py` : données, classes et chargement des ressources
- `modules/effect.py` : effets visuels
- `modules/game.py` : boucle principale du jeu
- `modules/screen.py` : écrans du menu et de l'aide
- `assets/` : images, polices et autres ressources

## Dépendances
- `pygame-ce` : affichage, événements, boucles de jeu
- `codecarbon` : suivi optionnel des émissions carbone affiché dans `main.py`
>>>>>>> Stashed changes

