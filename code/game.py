import pygame
import sys
import os
import math
from constant import *
from effect import ParticleEffect, FloatingText
from dataHandler import SpawnManager, ASSETS_PATH

# ============================================================
# MAIN GAME
# ============================================================

def main(player):
    """Main game loop handling gameplay logic and rendering."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EcoCatch - Save the City!")

    # --- Manual Path Configuration ---
    # Using relative paths to point to the root directory from the /code folder
    FONT_PATH = "..\\NotoEmoji-VariableFont_wght.ttf"
    ASSETS_FOLDER = "..\\assets"
    
    # Load Font
    try:
        game_font = pygame.font.Font(FONT_PATH, 20)
    except FileNotFoundError:
        # Fallback to default if font is missing
        game_font = pygame.font.Font(None, 20)

    # Load Background
    bg_path = os.path.join(ASSETS_FOLDER, "game_background.png")
    try:
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        # Fallback: Solid color background if image fails
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(VERT_FONCE)

    # --- Initialization ---
    player.replay()  # Reset player stats (score, lives, etc.)
    falling_objects = []
    spawn_manager = SpawnManager()
    particles = []
    floating_texts = []
    clock = pygame.time.Clock()

    # Timer to display the level at the start (in frames)
    level_display_timer = 120  # Approx 2 seconds at 60 FPS

    # --- Game loop ---
    running = True
    while running and not player.check_end():

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to menu
                    running = False
                    return "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if a waste object was clicked
                for obj in falling_objects:
                    if obj.is_clicked((mouse_x, mouse_y)) and not obj.caught:
                        obj.caught = True
                        falling_objects.remove(obj)

                        # Update player stats
                        player.attraper_dechet() # Function to increment score/combo

                        # Visual Feedback: Particles
                        particles.append(ParticleEffect(
                            obj.rect.centerx, obj.rect.centery,
                            color=(100, 255, 100)
                        ))

                        # Visual Feedback: Floating point text
                        points = 10
                        if player.combo >= 5:
                            points = 30
                            text = f"+{points} COMBO!"
                            color = (255, 200, 50)
                        elif player.combo >= 3:
                            points = 20
                            text = f"+{points}!"
                            color = (255, 255, 100)
                        else:
                            text = f"+{points}"
                            color = (200, 255, 200)
                        
                        floating_texts.append(FloatingText(
                            obj.rect.centerx, obj.rect.y, text, color
                        ))

                        # Display educational fact about the waste
                        if obj.dechet_info:
                            name = obj.dechet_info[1]
                            time = obj.dechet_info[2]
                            player.fact_actuel = f"{name}: {time} to decompose"
                            player.fact_timer = 120
                        break

        # 2. Update Logic
        # Spawn management
        spawn_manager.update(falling_objects, player)

        # Update falling waste positions
        for obj in falling_objects[:]:
            obj.update()

            # Check for collision with ground
            if obj.has_hit_ground(GROUND_Y):
                falling_objects.remove(obj)
                player.lose_life() # Reduce player health

                # Miss visual effects
                particles.append(ParticleEffect(
                    obj.rect.centerx, GROUND_Y,
                    color=(255, 80, 80)
                ))
                floating_texts.append(FloatingText(
                    obj.rect.centerx, GROUND_Y - 30,
                    "Miss!", (255, 100, 100)
                ))

        # Update visual effects
        for p in particles[:]:
            p.update()
            if p.is_done():
                particles.remove(p)

        for ft in floating_texts[:]:
            ft.update()
            if ft.is_done():
                floating_texts.remove(ft)

        # 3. Rendering
        # Draw background
        screen.blit(background, (0, 0))

        # Draw environment (Walls and Ground)
        pygame.draw.line(screen, VERT_FONCE, (12, GROUND_Y), (12, 100), 8)
        pygame.draw.line(screen, VERT_FONCE, (488, GROUND_Y), (488, 100), 8)
        pygame.draw.rect(screen, VERT_CLAIR, (0, GROUND_Y, SCREEN_WIDTH, 10))
        pygame.draw.rect(screen, VERT_FONCE, (0, GROUND_Y + 10, SCREEN_WIDTH, 90))

        # Draw all game objects
        for obj in falling_objects:
            obj.draw(screen)

        for p in particles:
            p.draw(screen)
        for ft in floating_texts:
            ft.draw(screen)

        # Draw User Interface (HUD)
        player.draw(screen)

        # Start of Level Message
        if level_display_timer > 0:
            level_display_timer -= 1
            font_level = pygame.font.Font(None, 48)
            level_text = font_level.render(f"Level {player.current_level}", True, JAUNE)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Overlay box for the level text
            bg_rect = level_rect.inflate(40, 20)
            level_bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            alpha = min(200, level_display_timer * 5)
            level_bg.fill((0, 0, 0, alpha))
            screen.blit(level_bg, bg_rect.topleft)
            
            if level_display_timer > 20:
                screen.blit(level_text, level_rect)

        pygame.display.update()
        clock.tick(FPS_GAME)

    # --- Game Over Logic ---
    if player.check_end():
        # Final render state
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, VERT_CLAIR, (0, GROUND_Y, SCREEN_WIDTH, 10))
        pygame.draw.rect(screen, VERT_FONCE, (0, GROUND_Y + 10, SCREEN_WIDTH, 90))
        player.end_message(screen)

    return "menu"