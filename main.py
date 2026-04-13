import os
import pygame
from modules.screen import *
from codecarbon import EmissionsTracker


# ============================================================
# ENTRY POINT
# ============================================================


def wrap_text(font, text, max_width):
    """Split text into centered lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""

    for word in words:
        trial = word if not current else f"{current} {word}"
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def fit_font_size(text, start_size, min_size, max_width):
    """Find a font size where text fits within max_width."""
    size = start_size
    while size > min_size:
        font = pygame.font.Font(None, size)
        if font.size(text)[0] <= max_width:
            return font
        size -= 1
    return pygame.font.Font(None, min_size)


def show_session_report(emissions_kg, energy_kwh):
    """Display a clean session summary page before closing the game."""
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("EcoCatch - Bilan de session")
        clock = pygame.time.Clock()

        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "help_background.png")
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        panel_w, panel_h = 460, 310
        panel_x, panel_y = 20, 205
        content_w = panel_w - 40

        title_font = pygame.font.Font(None, 62)
        hint_font = pygame.font.Font(None, 30)

        if energy_kwh is None:
            energy_line = "Consommation energie : non disponible"
        else:
            energy_wh = energy_kwh * 1000
            energy_line = f"Consommation energie : {energy_kwh:.6f} kWh ({energy_wh:.2f} Wh)"

        co2_line = f"Emissions CO2 : {emissions_kg:.6f} kg"

        metric_start_size = 40
        metric_min_size = 24
        metric_font = fit_font_size(energy_line, metric_start_size, metric_min_size, content_w)
        metric_font = fit_font_size(co2_line, metric_font.get_height() + 8, metric_min_size, content_w)

        hint_text = "Appuie sur Entree, Espace, Echap ou clique pour quitter"
        hint_lines = wrap_text(hint_font, hint_text, content_w)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            screen.blit(background, (0, 0))

            overlay = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 178), overlay.get_rect(), border_radius=20)
            pygame.draw.rect(overlay, (255, 255, 255, 210), overlay.get_rect(), width=2, border_radius=20)
            screen.blit(overlay, (panel_x, panel_y))

            title = title_font.render("Bilan de session", True, BLANC)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 70))
            screen.blit(title, title_rect)

            energy_text = metric_font.render(energy_line, True, JAUNE)
            energy_rect = energy_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 145))
            screen.blit(energy_text, energy_rect)

            co2_text = metric_font.render(co2_line, True, BLANC)
            co2_rect = co2_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 195))
            screen.blit(co2_text, co2_rect)

            hint_y = panel_y + 245
            for line in hint_lines:
                hint_surface = hint_font.render(line, True, BLANC)
                hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2, hint_y))
                screen.blit(hint_surface, hint_rect)
                hint_y += 28

            pygame.display.update()
            clock.tick(30)

        pygame.quit()
    except Exception:
        pass


tracker = EmissionsTracker(save_to_file=False)
tracker.start()

try:
    launcher()
finally:
    emissions = tracker.stop()

    final_data = getattr(tracker, "final_emissions_data", None)
    energy_kwh = None
    if final_data is not None:
        energy_kwh = getattr(final_data, "energy_consumed", None)
        if energy_kwh is None:
            energy_kwh = getattr(final_data, "energy_consumption", None)

    show_session_report(emissions, energy_kwh)
    print(f"Emissions de CO2 pour cette session : {round(emissions, 6)} kg")
import os
import pygame
from modules.screen import *
from codecarbon import EmissionsTracker


# ============================================================
# ENTRY POINT
# ============================================================


def show_session_report(emissions_kg, energy_kwh):
    """Affiche un bilan de session avant fermeture du jeu."""
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("EcoCatch - Bilan de session")
        clock = pygame.time.Clock()

        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "help_background.png")
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        title_font = pygame.font.Font(None, 62)
        main_font = pygame.font.Font(None, 38)
        small_font = pygame.font.Font(None, 30)

        if energy_kwh is None:
            energy_line = "Consommation energie : non disponible"
        else:
            energy_wh = energy_kwh * 1000
            energy_line = f"Consommation energie : {energy_kwh:.6f} kWh ({energy_wh:.2f} Wh)"

        co2_line = f"Emissions CO2 : {emissions_kg:.6f} kg"

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            screen.blit(background, (0, 0))

            overlay = pygame.Surface((460, 270), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 170), overlay.get_rect(), border_radius=20)
            pygame.draw.rect(overlay, (255, 255, 255, 200), overlay.get_rect(), width=2, border_radius=20)
            screen.blit(overlay, (20, 220))

            title = title_font.render("Bilan de session", True, BLANC)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(title, title_rect)

            energy_text = main_font.render(energy_line, True, JAUNE)
            energy_rect = energy_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            screen.blit(energy_text, energy_rect)

            co2_text = main_font.render(co2_line, True, BLANC)
            co2_rect = co2_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            screen.blit(co2_text, co2_rect)

            hint = small_font.render("Appuie sur Entree, Espace, Echap ou clique pour quitter", True, BLANC)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 460))
            screen.blit(hint, hint_rect)

            pygame.display.update()
            clock.tick(30)

        pygame.quit()
    except Exception:
        pass


# Initialize the tracker
tracker = EmissionsTracker(save_to_file=False)
tracker.start()

try:
    # Code to start the launcher
    launcher()
finally:
    # Important: ensures the tracker stops even if the game crashes
    emissions: float = tracker.stop()

    final_data = getattr(tracker, "final_emissions_data", None)
    energy_kwh = None
    if final_data is not None:
        energy_kwh = getattr(final_data, "energy_consumed", None)
        if energy_kwh is None:
            energy_kwh = getattr(final_data, "energy_consumption", None)

    show_session_report(emissions, energy_kwh)
    print(f"Emissions de CO2 pour cette session : {round(emissions, 6)} kg")
from modules.screen import *
from codecarbon import EmissionsTracker


# ============================================================
# ENTRY POINT
# ============================================================


# Initialize the tracker
tracker = EmissionsTracker(save_to_file=False)
tracker.start()

try:
    # Code to start the launcher
    launcher()
finally:
    # Important: ensures the tracker stops even if the game crashes
    emissions: float = tracker.stop()
    print(f"Emissions de CO2 pour cette session : {round(emissions, 6)} kg")