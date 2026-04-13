import pygame
import random
import os


# ============================================================
# EDUCATIONAL DATA ABOUT WASTE
# ============================================================

# Each waste: (file_name, display_name, decomposition_time, sorting_category)
DECHETS_DATA = [
    ("bouteille_plastique.png", "Bouteille plastique", "450 ans", "Plastique"),
    ("canette.png", "Canette aluminium", "200 ans", "Métal"),
    ("papier.png", "Papier froissé", "2-5 mois", "Papier"),
    ("sac_plastique.png", "Sac plastique", "400 ans", "Plastique"),
    ("gobelet.png", "Gobelet carton", "5 ans", "Carton"),
    ("pile.png", "Pile usagée", "7000 ans", "Déchets spéciaux"),
    ("trognon.png", "Trognon de pomme", "1-5 mois", "Compost"),
    ("emballage.png", "Emballage bonbon", "5 ans", "Plastique"),
    ("masque.png", "Masque chirurgical", "450 ans", "Ordures"),
    ("megot.png", "Mégot cigarette", "12 ans", "Ordures"),
    ("boite_conserve.png", "Boîte de conserve", "50-100 ans", "Métal"),
]

# Educational messages displayed when the player catches a waste
ECO_MESSAGES = [
    "Bravo ! Tu protèges la planète !",
    "Super réflexe ! Moins de pollution !",
    "Bien joué ! Chaque geste compte !",
    "Génial ! La Terre te remercie !",
    "Excellent ! Tu es un éco-héros !",
    "Incroyable ! Continue comme ça !",
    "Magnifique ! La ville reste propre !",
    "Trop fort ! Les animaux te remercient !",
]

# Messages with info about decomposition time
ECO_FACTS = [
    "Un sac plastique met 400 ans à se décomposer !",
    "Une canette met 200 ans à disparaître !",
    "Un mégot pollue 500 litres d'eau !",
    "Une pile peut contaminer 1m³ de terre !",
    "Le verre met 4000 ans à se décomposer !",
    "Le papier se recycle jusqu'à 7 fois !",
    "Le plastique représente 80% des déchets marins !",
    "Recycler 1 canette = 3h de TV en énergie !",
]

# Path to assets
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets")
FONT_PATH = os.path.join(ASSETS_PATH, "NotoEmoji-VariableFont_wght.ttf")

# ============================================================
# PLAYER CLASS - Manages the player and score
# ============================================================

class Player:
    """Manages the score, lives, and player display."""

    def __init__(self):
        # Game stats
        self.score = 0                   # Player's score (caught waste)
        self.vies = 5                    # Number of lives (missed waste allowed)
        self.dechets_attrapes = 0        # Total counter
        self.combo = 0                   # Current combo (consecutive catches)
        self.max_combo = 0               # Best combo
        self.message_actuel = ""         # Current educational message
        self.message_timer = 0           # Timer for displaying the message
        self.fact_actuel = ""            # Current ecological fact
        self.fact_timer = 0              # Timer for the ecological fact

        # Difficulty level management
        self.current_level = 1           # Current level (for difficulty scaling)
        
        # Physics parameters (class variables for easy level management)
        self.GRAVITY = 0.15              # Gravity (pixels/frame^2)
        self.AIR_RESISTANCE = 0.01       # Air resistance
        self.SPAWN_SPEED_MIN = 1.0       # Minimum falling speed
        self.SPAWN_SPEED_MAX = 2.5       # Maximum falling speed
        self.PARABOLIC_CHANCE = 0.0      # Chance of parabolic throw (0 = never, 1 = always)
        self.SPRITE_SIZE = 80            # Base sprite size

    def replay(self):
        """Resets the player's stats for a new game."""
        self.score = 0
        self.vies = 5
        self.dechets_attrapes = 0
        self.combo = 0
        self.max_combo = 0
        self.message_actuel = ""
        self.message_timer = 0
        self.fact_actuel = ""
        self.fact_timer = 0

    def draw(self, screen):
        """Displays the score, lives, and educational messages."""
        # Score at the top left
        font = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)

        # Semi-transparent background for the HUD
        hud_surface = pygame.Surface((490, 50), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 100))
        screen.blit(hud_surface, (5, 5))

        # Score
        score_text = font.render(f"Score : {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (15, 15))

        # Lives (small green hearts)
        font_vies = pygame.font.Font(FONT_PATH, 20)
        vies_text = font_vies.render(f"{'♥' * self.vies}", True, (100, 255, 100))
        screen.blit(vies_text, (180, 15))

        # Combo
        if self.combo >= 3:
            combo_text = font.render(f"Combo x{self.combo}!", True, (255, 215, 0))
            screen.blit(combo_text, (365, 15))

        # Educational message (at the bottom of the screen)
        if self.message_timer > 0:
            msg_surface = pygame.Surface((480, 35), pygame.SRCALPHA)
            msg_surface.fill((46, 139, 87, 180))
            screen.blit(msg_surface, (10, 60))
            msg_text = font_small.render(self.message_actuel, True, (255, 255, 255))
            msg_rect = msg_text.get_rect(center=(250, 77))
            screen.blit(msg_text, msg_rect)
            self.message_timer -= 1

        # Ecological fact (at the bottom)
        if self.fact_timer > 0:
            fact_surface = pygame.Surface((480, 30), pygame.SRCALPHA)
            fact_surface.fill((0, 100, 150, 160))
            screen.blit(fact_surface, (10, 710))
            fact_text = font_small.render(self.fact_actuel, True, (200, 240, 255))
            fact_rect = fact_text.get_rect(center=(250, 725))
            screen.blit(fact_text, fact_rect)
            self.fact_timer -= 1

    def attraper_dechet(self):
        """The player has caught a waste."""
        self.dechets_attrapes += 1
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo

        # Score calculation (combo bonus)
        points = 10
        if self.combo >= 5:
            points = 30
        elif self.combo >= 3:
            points = 20
        self.score += points

        # Random educational message
        self.message_actuel = random.choice(ECO_MESSAGES)
        self.message_timer = 90  # env 1.5 sec à 60 FPS

        # Display an ecological fact from time to time
        if self.dechets_attrapes % 5 == 0:
            self.fact_actuel = random.choice(ECO_FACTS)
            self.fact_timer = 180  # 3 sec

    def lose_life(self):
        """A waste has hit the ground."""
        self.vies -= 1
        self.combo = 0  # Reset combo

    def check_end(self):
        """Checks if the game is over."""
        return self.vies <= 0

    def end_message(self, screen):
        """Displays the end of game screen."""
        # Semi-transparent background
        overlay = pygame.Surface((500, 750), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        font_big = pygame.font.Font(None, 56)
        font_med = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        if self.score >= 200:
            titre = "Éco-Héros !"
            color = (100, 255, 100)
        elif self.score >= 100:
            titre = "Bien joué !"
            color = (255, 230, 100)
        else:
            titre = "Fin de partie"
            color = (255, 150, 150)

        titre_text = font_big.render(titre, True, color)
        titre_rect = titre_text.get_rect(center=(250, 250))
        screen.blit(titre_text, titre_rect)

        # Stats
        stats = [
            f"Score final : {self.score} points",
            f"Déchets attrapés : {self.dechets_attrapes}",
            f"Meilleur combo : x{self.max_combo}",
        ]
        for i, stat in enumerate(stats):
            stat_text = font_med.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(250, 330 + i * 40))
            screen.blit(stat_text, stat_rect)

        # Message éducatif final
        msg = "Chaque déchet ramassé aide la planète !"
        msg_text = font_small.render(msg, True, (150, 255, 200))
        msg_rect = msg_text.get_rect(center=(250, 480))
        screen.blit(msg_text, msg_rect)

        pygame.display.flip()
        pygame.time.delay(3000)

    
    # ---- Level management ----

    def increase_level(self):
        """Increases the difficulty."""
        self.GRAVITY = min(self.GRAVITY + 0.05, 0.35)
        self.SPAWN_SPEED_MIN = min(self.SPAWN_SPEED_MIN + 0.3, 3.0)
        self.SPAWN_SPEED_MAX = min(self.SPAWN_SPEED_MAX + 0.3, 5.0)
        self.PARABOLIC_CHANCE = min(self.PARABOLIC_CHANCE + 0.25, 0.7)
        self.SPRITE_SIZE = max(self.SPRITE_SIZE - 4, 40)
        self.current_level += 1

    def decrease_level(self):
        """Decreases the difficulty."""
        self.GRAVITY = max(self.GRAVITY - 0.05, 0.08)
        self.SPAWN_SPEED_MIN = max(self.SPAWN_SPEED_MIN - 0.3, 0.5)
        self.SPAWN_SPEED_MAX = max(self.SPAWN_SPEED_MAX - 0.3, 1.0)
        self.PARABOLIC_CHANCE = max(self.PARABOLIC_CHANCE - 0.15, 0.0)
        self.SPRITE_SIZE = min(self.SPRITE_SIZE + 4, 72)
        self.current_level = max(self.current_level - 1, 1)


# ============================================================
# FALLINGOBJECT CLASS - Manages falling waste
# ============================================================

class FallingObject:
    """
    Represents a waste that falls or is thrown in a parabola.
    Parabolic trajectory: x(t) = x0 + vx*t, y(t) = y0 + vy*t + 0.5*g*t²
    """

    def __init__(self, dechet_type, start_x, start_y, SPRITE_SIZE, 
                 GRAVITY, AIR_RESISTANCE, SPAWN_SPEED_MIN, SPAWN_SPEED_MAX, parabolic=False):
        """
        Initializes a falling waste.

        Args:
            image_path: Path to the waste image
            start_x: Starting X position
            start_y: Starting Y position
            SPRITE_SIZE: Size of the sprite
            GRAVITY: Gravity strength
            AIR_RESISTANCE: Air resistance factor
            SPAWN_SPEED_MIN: Minimum initial falling speed
            SPAWN_SPEED_MAX: Maximum initial falling speed
            parabolic: If True, parabolic trajectory (thrown from a building)
        """

        self.SPRITE_SIZE = SPRITE_SIZE
        self.GRAVITY = GRAVITY
        self.AIR_RESISTANCE = AIR_RESISTANCE
        self.SPAWN_SPEED_MIN = SPAWN_SPEED_MIN
        self.SPAWN_SPEED_MAX = SPAWN_SPEED_MAX
        
        # Store the waste type for educational messages
        self.dechet_info = dechet_type

        full_path = os.path.join(ASSETS_PATH, self.dechet_info[0])
        self.image = pygame.image.load(full_path).convert_alpha()

        # Enlarge the sprite to make it more visible and easier to click
        self.image = pygame.transform.scale(self.image, (self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.rect = self.image.get_rect()

        self.is_parabolic = parabolic
        self.is_falling = True  # Starts falling as soon as created
        self.caught = False     # Has been caught


        if parabolic:
            # Parabolic trajectory: thrown from a side (building)
            # Choose a random side (left or right)
            side = random.choice(["left", "right"])
            if side == "left":
                self.rect.x = random.randint(-20, 30)
                self.velocity_x = random.uniform(10.5, 20.0)  # To the right
            else:
                self.rect.x = random.randint(440, 490)
                self.velocity_x = random.uniform(-20.0, -10.5)  # To the left

            self.rect.y = random.randint(60, 200)  # From a building window
            # Initial vertical speed (upwards then falls)
            self.velocity_y = random.uniform(-3.0, -1.0)
        else:
            # Classic vertical fall (like the original)
            self.rect.x = start_x
            self.rect.y = start_y - SPRITE_SIZE  # Starts above the screen
            self.velocity_x = random.uniform(-3.3, 0.3)  # Slight horizontal drift
            self.velocity_y = random.uniform(
                self.SPAWN_SPEED_MIN,
                self.SPAWN_SPEED_MAX
            )

    def update(self):
        """Updates the position of the waste according to physics."""
        if self.caught:
            return

        # Apply gravity
        self.velocity_y += self.GRAVITY

        # Air resistance (slightly slows down)
        self.velocity_y -= self.velocity_y * self.AIR_RESISTANCE
        self.velocity_x -= self.velocity_x * self.AIR_RESISTANCE

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Bounce on side walls
        if self.rect.x <= 15:
            self.rect.x = 15
            self.velocity_x = abs(self.velocity_x) * 0.7
        elif self.rect.x >= 500 - self.SPRITE_SIZE - 15:
            self.rect.x = 500 - self.SPRITE_SIZE - 15
            self.velocity_x = -abs(self.velocity_x) * 0.7

    def has_hit_ground(self, ground_y=650):
        """Checks if the waste has hit the ground."""
        return self.rect.y + self.SPRITE_SIZE >= ground_y

    def is_clicked(self, mouse_pos):
        """Checks if the player clicked on the waste."""
        # Slightly larger click area for children
        expanded_rect = self.rect.inflate(10, 10)
        return expanded_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        """Draws the waste on the screen."""
        if not self.caught:
            screen.blit(self.image, self.rect.topleft)


# ============================================================
# SPAWNMANAGER CLASS - Manages the appearance of waste
# ============================================================

class SpawnManager:
    """Manages the timing and spawn position of waste."""

    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = 60   # Frames between each spawn (1 second at 60 FPS)
        self.min_interval = 20     # Minimum interval
        self.dechets_spawned = 0   # Total counter

    def update(self, falling_objects, player):
        """
        Updates the timer and creates new waste if necessary.
        Returns: The new waste created or None
        """
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.dechets_spawned += 1

            # Gradually speed up the spawn
            if self.dechets_spawned % 10 == 0 and self.spawn_interval > self.min_interval:
                self.spawn_interval = max(self.spawn_interval - 5, self.min_interval)

            # Choose a random waste
            dechet_data = random.choice(DECHETS_DATA)

            # Random X position (within the walls)
            margin = player.SPRITE_SIZE // 2 + 20
            start_x = random.randint(margin, 500 - margin)

            # Determine if it's a parabolic throw
            is_parabolic = random.random() < player.PARABOLIC_CHANCE

            new_obj = FallingObject(dechet_data, start_x, 0, player.SPRITE_SIZE, player.GRAVITY, player.AIR_RESISTANCE, player.SPAWN_SPEED_MIN, player.SPAWN_SPEED_MAX, parabolic=is_parabolic)
            falling_objects.append(new_obj)
            return new_obj


    def reset(self):
        """Resets the spawn manager."""
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.dechets_spawned = 0
