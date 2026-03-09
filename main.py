import pygame
import random
import sys
import os
import math
from dataHandler import (
    Player, SpawnManager,
    DECHETS_DATA, ASSETS_PATH
)

# ============================================================
# GLOBAL CONSTANTS
# ============================================================

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
FPS_GAME = 60
FPS_MENU = 30
GROUND_Y = 650           # Y position of the ground

# Eco-friendly theme colors
VERT_FONCE = (30, 100, 60)
VERT_CLAIR = (46, 139, 87)
VERT_BOUTON = (60, 180, 100)
VERT_HOVER = (80, 210, 130)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 230, 100)
ROUGE = (220, 60, 60)
BLEU_CIEL = (135, 206, 250)
GRIS_FONCE = (60, 60, 60)


# ============================================================
# VISUAL EFFECTS
# ============================================================

class ParticleEffect:
    """Particle effect when a waste is caught."""

    def __init__(self, x, y, color=(100, 255, 100)):
        self.particles = []
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append({
                "x": x, "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(15, 30),
                "size": random.randint(3, 7),
                "color": (
                    min(255, color[0] + random.randint(-30, 30)),
                    min(255, color[1] + random.randint(-30, 30)),
                    min(255, color[2] + random.randint(-30, 30)),
                )
            })

    def update(self):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15  # Gravity on particles
            p["life"] -= 1
            p["size"] = max(1, p["size"] - 0.1)
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, screen):
        for p in self.particles:
            alpha = min(255, p["life"] * 10)
            size = int(p["size"])
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), size)

    def is_done(self):
        return len(self.particles) == 0


class FloatingText:
    """Floating text (+10, +20, Combo!) that rises and disappears."""

    def __init__(self, x, y, text, color=(255, 255, 100)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 40
        self.font = pygame.font.Font(None, 28)

    def update(self):
        self.y -= 1.5
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            text_surface = self.font.render(self.text, True, self.color)
            screen.blit(text_surface, (self.x, self.y))

    def is_done(self):
        return self.life <= 0


# ============================================================
# MAIN GAME
# ============================================================

def main(player):
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Sauve la ville !")

    # Load the background
    bg_path = os.path.join(ASSETS_PATH, "game_background.png")
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialization
    player.replay()
    falling_objects = []
    spawn_manager = SpawnManager()
    particles = []
    floating_texts = []
    clock = pygame.time.Clock()

    # Timer to display the level at the start
    level_display_timer = 120  # 2 seconds

    # Game loop
    running = True
    while running and not player.check_end():

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pause - return to menu
                    running = False
                    return "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check each waste to see if it was clicked
                for obj in falling_objects:
                    if obj.is_clicked((mouse_x, mouse_y)) and not obj.caught:
                        obj.caught = True
                        falling_objects.remove(obj)

                        # Mettre à jour le score
                        player.attraper_dechet()

                        # Visual effects
                        particles.append(ParticleEffect(
                            obj.rect.centerx, obj.rect.centery,
                            color=(100, 255, 100)
                        ))

                        # Floating text
                        points = 10
                        if player.combo >= 5:
                            points = 30
                            floating_texts.append(FloatingText(
                                obj.rect.centerx, obj.rect.y,
                                f"+{points} COMBO!", (255, 200, 50)
                            ))
                        elif player.combo >= 3:
                            points = 20
                            floating_texts.append(FloatingText(
                                obj.rect.centerx, obj.rect.y,
                                f"+{points}!", (255, 255, 100)
                            ))
                        else:
                            floating_texts.append(FloatingText(
                                obj.rect.centerx, obj.rect.y,
                                f"+{points}", (200, 255, 200)
                            ))

                        # Waste decomposition info
                        if obj.dechet_info:
                            nom = obj.dechet_info[1]
                            temps = obj.dechet_info[2]
                            player.fact_actuel = f"{nom} : {temps} pour se décomposer"
                            player.fact_timer = 120

                        break  # Only one waste per click

        # Spawn new waste
        spawn_manager.update(falling_objects, player)

        # Update waste
        for obj in falling_objects:
            obj.update()

            # Check if the waste hits the ground
            if obj.has_hit_ground(GROUND_Y):
                falling_objects.remove(obj)
                player.perdre_vie()

                # Visual effect for miss
                particles.append(ParticleEffect(
                    obj.rect.centerx, GROUND_Y,
                    color=(255, 80, 80)
                ))
                floating_texts.append(FloatingText(
                    obj.rect.centerx, GROUND_Y - 30,
                    "Raté !", (255, 100, 100)
                ))

        # Update effects
        for p in particles:
            p.update()
            if p.is_done():
                particles.remove(p)

        for ft in floating_texts:
            ft.update()
            if ft.is_done():
                floating_texts.remove(ft)

        # ---- RENDERING ----
        screen.blit(background, (0, 0))

        # Draw side walls
        pygame.draw.line(screen, VERT_FONCE, (12, GROUND_Y), (12, 100), 8)
        pygame.draw.line(screen, VERT_FONCE, (488, GROUND_Y), (488, 100), 8)

        # Draw the ground (green area)
        pygame.draw.rect(screen, VERT_CLAIR, (0, GROUND_Y, SCREEN_WIDTH, 10))
        pygame.draw.rect(screen, VERT_FONCE, (0, GROUND_Y + 10, SCREEN_WIDTH, 90))

        # Draw waste
        for obj in falling_objects:
            obj.draw(screen)

        # Draw effects
        for p in particles:
            p.draw(screen)
        for ft in floating_texts:
            ft.draw(screen)

        # Player HUD
        player.draw(screen)

        # Level display at the start
        if level_display_timer > 0:
            level_display_timer -= 1
            font_level = pygame.font.Font(None, 48)
            level_text = font_level.render(f"Niveau {player.current_level}", True, JAUNE)
            level_rect = level_text.get_rect(center=(250, 375))

            # Message background
            bg_rect = level_rect.inflate(40, 20)
            level_bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            level_bg.fill((0, 0, 0, min(200, level_display_timer * 5)))
            screen.blit(level_bg, bg_rect.topleft)
            if level_display_timer > 20:  # Fade out
                screen.blit(level_text, level_rect)

        pygame.display.update()
        clock.tick(FPS_GAME)

    if player.check_end():
        # Display the background + last objects
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, VERT_CLAIR, (0, GROUND_Y, SCREEN_WIDTH, 10))
        pygame.draw.rect(screen, VERT_FONCE, (0, GROUND_Y + 10, SCREEN_WIDTH, 90))
        player.end_message(screen)

    return "menu"


# ============================================================
# LEVEL SELECTION SCREEN
# ============================================================

def level_screen(player):
    """Difficulty level configuration screen."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Réglages")
    clock = pygame.time.Clock()

    # Background
    bg_path = os.path.join(ASSETS_PATH, "level_background.png") 
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fonts
    font_title = pygame.font.Font(None, 60) 
    font_btn = pygame.font.Font(None, 40)  
    font_info = pygame.font.Font(None, 30)

    btn_easier = pygame.Rect(115, 440, 280, 55)
    btn_harder = pygame.Rect(115, 510, 280, 55)
    btn_back = pygame.Rect(115, 580, 280, 55)

    buttons = [
        {"rect": btn_easier, "text": "Plus facile", "action": "easier"},
        {"rect": btn_harder, "text": "Plus difficile", "action": "harder"},
        {"rect": btn_back, "text": "Retour", "action": "back"},
    ]

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        title_text = font_title.render("Réglages", True, BLANC)
        title_shadow = font_title.render("Réglages", True, (0, 50, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 5 , 340))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)

        level_info = f"Gravité: {round(player.GRAVITY, 2)} | Paraboles: {int(player.PARABOLIC_CHANCE*100)}%"
        info_text = font_info.render(level_info, True, (200, 255, 200))
        info_shadow = font_info.render(level_info, True, (0, 30, 0))
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2 + 5, 380))
        screen.blit(info_shadow, (info_rect.x + 1, info_rect.y + 1))
        screen.blit(info_text, info_rect)

        for btn in buttons:
            is_hover = btn["rect"].collidepoint(mouse_x, mouse_y)
            text_color = JAUNE if is_hover else BLANC
            
            shadow = font_btn.render(btn["text"], True, (50, 40, 20))
            text = font_btn.render(btn["text"], True, text_color)
            
            text_rect = text.get_rect(center=btn["rect"].center)
            
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)

            if is_hover:
                pygame.draw.line(screen, JAUNE,
                                 (btn["rect"].left + 40, btn["rect"].bottom - 5),
                                 (btn["rect"].right - 40, btn["rect"].bottom - 5), 3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in buttons:
                        if btn["rect"].collidepoint(mouse_x, mouse_y):
                            if btn["action"] == "easier":
                                player.decrease_level()
                            elif btn["action"] == "harder":
                                player.increase_level()
                            elif btn["action"] == "back":
                                return

        clock.tick(FPS_MENU)

# ============================================================
# HELP SCREEN
# ============================================================

def help_screen():
    """Help screen with game rules."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Aide")
    clock = pygame.time.Clock()

    # Background
    bg_path = os.path.join(ASSETS_PATH, "help_background.png")
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_title = pygame.font.Font(None, 55)
    font_text = pygame.font.Font(None, 28) 
    font_btn = pygame.font.Font(None, 40)

    rules = [
        "Comment jouer :",
        "",
        "Des déchets tombent du ciel !",
        "Cliquez dessus pour les attraper",
        "avant qu'ils ne touchent le sol.",
        "",
        "Si un déchet touche le sol,",
        "vous perdez une vie (5 max).",
        "",
        "Attrapez-en plusieurs d'affilée",
        "pour faire des combos et gagner",
        "plus de points !",
        "",
        "Attention : certains déchets",
        "sont jetés depuis les bâtiments !",
        "",
        "Apprenez combien de temps chaque",
        "déchet met à se décomposer."
    ]

    btn_back = {"rect": pygame.Rect(115, 680, 270, 55), "text": "Retour", "action": "back"}

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Semi-transparent overlay for text readability
        overlay = pygame.Surface((440, 540), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 160), overlay.get_rect(), border_radius=20)
        screen.blit(overlay, (30, 110))

        # Title
        title_text = font_title.render("Aide", True, BLANC)
        title_shadow = font_title.render("Aide", True, (0, 50, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)

        # Rules text (Centré)
        y_pos = 200
        for line in rules:
            color = VERT_HOVER if line == "Comment jouer :" else BLANC
            if line == "":
                y_pos += 12
                continue
            
            text_shadow = font_text.render(line, True, (0, 30, 0))
            text_surf = font_text.render(line, True, color)
            
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            
            screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text_surf, text_rect)
            y_pos += 26

        # Back button (Transparent)
        is_hover = btn_back["rect"].collidepoint(mouse_x, mouse_y)
        btn_color = VERT_HOVER if is_hover else VERT_BOUTON
        text_color = JAUNE if is_hover else BLANC

        # Création d'une surface transparente pour le bouton
        btn_surface = pygame.Surface(btn_back["rect"].size, pygame.SRCALPHA)
        
        # Opacité : 220 au survol, 160 sinon (sur 255)
        alpha_value = 220 if is_hover else 160 
        r, g, b = btn_color[:3]
        color_with_alpha = (r, g, b, alpha_value)
        
        # Dessin du bouton et de sa bordure sur sa surface dédiée
        pygame.draw.rect(btn_surface, color_with_alpha, btn_surface.get_rect(), border_radius=15)
        pygame.draw.rect(btn_surface, (255, 255, 255, 200), btn_surface.get_rect(), width=2, border_radius=15)
        
        # Affichage du bouton sur l'écran
        screen.blit(btn_surface, btn_back["rect"].topleft)

        # Texte du bouton
        shadow = font_btn.render(btn_back["text"], True, (50, 40, 20))
        text = font_btn.render(btn_back["text"], True, text_color)
        text_rect = text.get_rect(center=btn_back["rect"].center)

        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text, text_rect)

        if is_hover:
            pygame.draw.line(screen, JAUNE,
                             (btn_back["rect"].left + 40, btn_back["rect"].bottom - 5),
                             (btn_back["rect"].right - 40, btn_back["rect"].bottom - 5), 3)

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_back["rect"].collidepoint(mouse_x, mouse_y):
                        return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        clock.tick(FPS_MENU)

# ============================================================
# MAIN MENU (LAUNCHER)
# ============================================================

def launcher():
    """Main menu of the EcoCatch game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Menu")
    clock = pygame.time.Clock()

    #init player
    player = Player()

    # Background
    bg_path = os.path.join(ASSETS_PATH, "launcher_background.png") 
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fonts - Police légèrement plus grande pour bien remplir les boutons en bois
    font_btn = pygame.font.Font(None, 40)

    # Falling waste animation in the background (decoration)
    deco_objects = []
    deco_timer = 0

    has_played = False

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Buttons definition
        # Coordonnées ajustées pour correspondre aux boutons en bois de l'image
        btn_play_text = "Rejouer" if has_played else "Jouer"
        buttons = [
            {"rect": pygame.Rect(115, 435, 270, 55), "text": btn_play_text, "action": "play"},
            {"rect": pygame.Rect(115, 505, 270, 55), "text": "Niveau", "action": "level"},
            {"rect": pygame.Rect(115, 579, 270, 55), "text": "Aide", "action": "help"},
            {"rect": pygame.Rect(115, 650, 270, 55), "text": "Quitter", "action": "quit"},
        ]

        for btn in buttons:
            is_hover = btn["rect"].collidepoint(mouse_x, mouse_y)
            
            # Au lieu de dessiner un rectangle qui cacherait l'image, on modifie la couleur du texte au survol
            text_color = JAUNE if is_hover else BLANC
            
            # Ombre pour le texte (meilleure lisibilité sur le bois)
            shadow = font_btn.render(btn["text"], True, (50, 40, 20))
            text = font_btn.render(btn["text"], True, text_color)
            
            text_rect = text.get_rect(center=btn["rect"].center)
            
            # Affichage du texte
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)

            # Ligne de soulignement optionnelle au survol
            if is_hover:
                pygame.draw.line(screen, JAUNE,
                                 (btn["rect"].left + 40, btn["rect"].bottom - 5),
                                 (btn["rect"].right - 40, btn["rect"].bottom - 5), 3)

        # Mini decoration: waste falling in the background
        deco_timer += 1
        if deco_timer % 30 == 0 and len(deco_objects) < 20:
            dechet = random.choice(DECHETS_DATA)
            try:
                deco_img = pygame.image.load(os.path.join(ASSETS_PATH, dechet[0])).convert_alpha()
                deco_img = pygame.transform.scale(deco_img, (32, 32))
                deco_objects.append({
                    "img": deco_img,
                    "x": random.randint(20, SCREEN_WIDTH - 20),
                    "y": -32,
                    "speed": random.uniform(1.5, 2.5),
                    "alpha": 100
                })
            except Exception:
                pass

        for deco in deco_objects:
            deco["y"] += deco["speed"]
            screen.blit(deco["img"], (deco["x"], deco["y"]))
            if deco["y"] > SCREEN_HEIGHT:
                deco_objects.remove(deco)

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic gauche uniquement
                    for btn in buttons:
                        if btn["rect"].collidepoint(mouse_x, mouse_y):
                            if btn["action"] == "play":
                                main(player)
                                has_played = True
                            elif btn["action"] == "level":
                                level_screen(player)
                            elif btn["action"] == "help":
                                help_screen()
                            elif btn["action"] == "quit":
                                pygame.quit()
                                sys.exit()

        clock.tick(FPS_MENU)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    launcher()
