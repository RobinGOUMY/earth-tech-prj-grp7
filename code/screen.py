import pygame
import sys
import os
import random
from constant import *
from game import main
from dataHandler import DECHETS_DATA, ASSETS_PATH, Player

# ============================================================
# LEVEL SELECTION SCREEN
# ============================================================

def level_screen(player):
    """Screen allowing the player to configure game difficulty."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Settings")
    clock = pygame.time.Clock()

    # Load Background
    bg_path = os.path.join(ASSETS_PATH, "level_background.png") 
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize Fonts
    font_title = pygame.font.Font(None, 60) 
    font_btn = pygame.font.Font(None, 40)   
    font_info = pygame.font.Font(None, 30)

    # Define Button Rectangles
    btn_easier = pygame.Rect(115, 440, 280, 55)
    btn_harder = pygame.Rect(115, 510, 280, 55)
    btn_back = pygame.Rect(115, 580, 280, 55)

    buttons = [
        {"rect": btn_easier, "text": "Easier", "action": "easier"},
        {"rect": btn_harder, "text": "Harder", "action": "harder"},
        {"rect": btn_back, "text": "Back", "action": "back"},
    ]

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render Title with shadow
        title_text = font_title.render("Settings", True, BLANC)
        title_shadow = font_title.render("Settings", True, (0, 50, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 5 , 340))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)

        # Display current level stats (Gravity & Parabolic chance)
        level_info = f"Gravity: {round(player.GRAVITY, 2)} | Parabolas: {int(player.PARABOLIC_CHANCE*100)}%"
        info_text = font_info.render(level_info, True, (200, 255, 200))
        info_shadow = font_info.render(level_info, True, (0, 30, 0))
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2 + 5, 380))
        screen.blit(info_shadow, (info_rect.x + 1, info_rect.y + 1))
        screen.blit(info_text, info_rect)

        # Draw Buttons and check for Hover effects
        for btn in buttons:
            is_hover = btn["rect"].collidepoint(mouse_x, mouse_y)
            text_color = JAUNE if is_hover else BLANC
            
            shadow = font_btn.render(btn["text"], True, (50, 40, 20))
            text = font_btn.render(btn["text"], True, text_color)
            text_rect = text.get_rect(center=btn["rect"].center)
            
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)

            # Add underline if hovering
            if is_hover:
                pygame.draw.line(screen, JAUNE,
                                 (btn["rect"].left + 40, btn["rect"].bottom - 5),
                                 (btn["rect"].right - 40, btn["rect"].bottom - 5), 3)

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
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
    """Screen displaying game instructions and rules."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Help")
    clock = pygame.time.Clock()

    # Load Background
    bg_path = os.path.join(ASSETS_PATH, "help_background.png")
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_title = pygame.font.Font(None, 55)
    font_text = pygame.font.Font(None, 28) 
    font_btn = pygame.font.Font(None, 40)

    # Instruction lines
    rules = [
        "How to play:",
        "",
        "Waste is falling from the sky!",
        "Click on it to catch it",
        "before it hits the ground.",
        "",
        "If a piece of waste hits the ground,",
        "you lose a life (Max: 5).",
        "",
        "Catch several in a row",
        "to trigger combos and earn",
        "more points!",
        "",
        "Watch out: some waste",
        "is thrown from buildings!",
        "",
        "Learn how long each type",
        "takes to decompose."
    ]

    btn_back = {"rect": pygame.Rect(115, 680, 270, 55), "text": "Back", "action": "back"}

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Semi-transparent overlay for text readability
        overlay = pygame.Surface((440, 540), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 160), overlay.get_rect(), border_radius=20)
        screen.blit(overlay, (30, 110))

        # Render Help Title
        title_text = font_title.render("Help", True, BLANC)
        title_shadow = font_title.render("Help", True, (0, 50, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)

        # Render instruction text line by line
        y_pos = 200
        for line in rules:
            color = VERT_HOVER if line == "How to play:" else BLANC
            if line == "":
                y_pos += 12
                continue
            
            text_shadow = font_text.render(line, True, (0, 30, 0))
            text_surf = font_text.render(line, True, color)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            
            screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text_surf, text_rect)
            y_pos += 26

        # Handle Back Button appearance
        is_hover = btn_back["rect"].collidepoint(mouse_x, mouse_y)
        btn_color = VERT_HOVER if is_hover else VERT_BOUTON
        text_color = JAUNE if is_hover else BLANC

        # Create transparent surface for the button
        btn_surface = pygame.Surface(btn_back["rect"].size, pygame.SRCALPHA)
        alpha_value = 220 if is_hover else 160 
        r, g, b = btn_color[:3]
        color_with_alpha = (r, g, b, alpha_value)
        
        pygame.draw.rect(btn_surface, color_with_alpha, btn_surface.get_rect(), border_radius=15)
        pygame.draw.rect(btn_surface, (255, 255, 255, 200), btn_surface.get_rect(), width=2, border_radius=15)
        screen.blit(btn_surface, btn_back["rect"].topleft)

        # Button Text
        shadow = font_btn.render(btn_back["text"], True, (50, 40, 20))
        text = font_btn.render(btn_back["text"], True, text_color)
        text_rect = text.get_rect(center=btn_back["rect"].center)

        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text, text_rect)

        # Underline on hover
        if is_hover:
            pygame.draw.line(screen, JAUNE,
                             (btn_back["rect"].left + 40, btn_back["rect"].bottom - 5),
                             (btn_back["rect"].right - 40, btn_back["rect"].bottom - 5), 3)

        pygame.display.update()

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
    """Main menu and entry point of the EcoCatch application."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Menu")
    clock = pygame.time.Clock()

    # Initialize Player instance
    player = Player()

    # Load Background (Manual Path)
    bg_path = "..\\assets\\launcher_background.png"
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_btn = pygame.font.Font(None, 40)

    # Decorative background animation: falling waste
    deco_objects = []
    deco_timer = 0
    has_played = False

    while True:
        screen.blit(background, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update Play button text based on game state
        btn_play_text = "Replay" if has_played else "Play"
        buttons = [
            {"rect": pygame.Rect(115, 435, 270, 55), "text": btn_play_text, "action": "play"},
            {"rect": pygame.Rect(115, 505, 270, 55), "text": "Difficulty", "action": "level"},
            {"rect": pygame.Rect(115, 579, 270, 55), "text": "Help", "action": "help"},
            {"rect": pygame.Rect(115, 650, 270, 55), "text": "Quit", "action": "quit"},
        ]

        # Render menu buttons
        for btn in buttons:
            is_hover = btn["rect"].collidepoint(mouse_x, mouse_y)
            text_color = JAUNE if is_hover else BLANC
            
            # Text shadow for better readability on wood textures
            shadow = font_btn.render(btn["text"], True, (50, 40, 20))
            text = font_btn.render(btn["text"], True, text_color)
            text_rect = text.get_rect(center=btn["rect"].center)
            
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)

            if is_hover:
                pygame.draw.line(screen, JAUNE,
                                 (btn["rect"].left + 40, btn["rect"].bottom - 5),
                                 (btn["rect"].right - 40, btn["rect"].bottom - 5), 3)

        # Background decoration logic: Spawn falling waste
        deco_timer += 1
        if deco_timer % 30 == 0 and len(deco_objects) < 20:
            dechet = random.choice(DECHETS_DATA)
            try:
                # Try loading the specific waste image from assets
                deco_img_path = os.path.join(ASSETS_PATH, dechet[0])
                deco_img = pygame.image.load(deco_img_path).convert_alpha()
                deco_img = pygame.transform.scale(deco_img, (32, 32))
                deco_objects.append({
                    "img": deco_img,
                    "x": random.randint(20, SCREEN_WIDTH - 20),
                    "y": -32,
                    "speed": random.uniform(1.5, 2.5)
                })
            except Exception:
                pass

        # Update and draw background decorations
        for deco in deco_objects[:]: # Copy list to allow removal
            deco["y"] += deco["speed"]
            screen.blit(deco["img"], (deco["x"], deco["y"]))
            if deco["y"] > SCREEN_HEIGHT:
                deco_objects.remove(deco)

        pygame.display.update()

        # Handle Menu Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click only
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