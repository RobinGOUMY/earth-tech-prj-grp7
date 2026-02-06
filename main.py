import pygame  # Importation de la bibliothèque Pygame
import random # Importation de la bibliothèque random
import cv2 # Importation de la bibliothèque OpenCV (pip install opencv-python)
import sys # Importation de la bibliothèque sys
from dataHandler import * # Importation des classes

def image_path(number):
    if number == 1:
        return "assets/apple.png"
    if number == 2:
        return "assets/cherry.png"
    if number == 3:
        return "assets/orange.png"
    if number == 4:
        return "assets/raisin.png"
    if number == 5:
        return "assets/citron.png"
    if number == 6:
        return "assets/citrong.png"
    if number == 7:
        return "assets/melon.png"
    if number == 8:
        return "assets/watermelon.png"
    if number == 9:
        return "assets/poire.png"
    if number == 10:
        return "assets/pech.png"
    else: 
        return "assets/strawberry.png"

def onclick(num_image_path,falling_objects, player, start_x, is_falling):
    if is_falling:
        # Mettre à jour la position de l'objet (descendre progressivement)
        falling_objects[-1].start_fall()

        # Creer le nouveau fruit
        onclick(num_image_path,falling_objects, player, 0, False)

    # À chaque clic de souris, mettre à jour le score du joueur
    else :
        falling_objects.append(FallingObject(num_image_path, start_x, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 750))
    pygame.display.set_caption('pyFruits - InGame')

    background = pygame.image.load("assets/game_background.png")
    background = pygame.transform.scale(background, (500, 750))
    player = Player()
    falling_objects = []
    clock = pygame.time.Clock()

    #Faire apparaitre le premier fruit
    number_image_path = image_path(random.randint(1,10))
    onclick(number_image_path,falling_objects, player, 0, False)

    while player.check_end() == False:

        # Dessiner le fond à chaque itération pour effacer l'écran
        screen.blit(background, (0, 0))

        #Faire en sorte que les fruits ne sortent pas de la boite
        fruitX_MIN = round(28+(cv2.imread(number_image_path).shape[0]/2))
        fruitX_MAX = round(473-(cv2.imread(number_image_path).shape[0]/2))
        nextFRUIT = random.randint(fruitX_MIN,fruitX_MAX)

        for ev in pygame.event.get():     
            if ev.type == pygame.QUIT:  
                pygame.quit()
                return None
            
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                # Image renouvelée
                number_image_path = image_path(random.randint(1,10))
                onclick(number_image_path,falling_objects, player, nextFRUIT, True)

                # Position de la souris
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Vérifier chaque fruit pour voir s'il a été cliqué
                for obj in falling_objects:
                    if obj.is_clicked((mouse_x, mouse_y)):
                        # Le fruit a été cliqué, le retirer de la liste
                        falling_objects.remove(obj)
                        player.update_fruits()

        # Dessiner les murs
        pygame.draw.line(screen, (6,10,43), (480, 685), (480, 80), 15)
        pygame.draw.line(screen, (6,10,43), (20, 80), (20, 685), 15)

        # Mettre à jour la position de chaque objet dans la liste
        for obj in falling_objects:
            obj.update(nextFRUIT)
            obj.draw(screen)
            # Faire perdre le fruit une fois arrivée au sol
            if obj.rect.y + cv2.imread(number_image_path).shape[0] >= 750:
                player.end_mesage(screen)
                return None
            
        # Dessiner le sol
        pygame.draw.line(screen, (255,0,0), (13, 685), (487, 685), 15)
        pygame.draw.line(screen, (253,203,154), (0, 725), (500, 725), 65)

        # Mettre à jour le score du joueur
        player.draw(screen)
        clock.tick(60)

        pygame.display.update()

    player.end_mesage(screen)

def level():
    pygame.init()

    clock = pygame.time.Clock()

    # Initialisation de l'écran
    screen = pygame.display.set_mode((500, 750))
    background = pygame.image.load("assets/launcher_background.jpg")
    background = pygame.transform.scale(background, (500, 750))  # Redimensionner l'image

    # Couleurs
    pygame.display.set_caption('pyFruits - LevelSettings')

    # Couleurs
    COLOR = (215, 175, 237)
    BUTTON_COLOR = (253, 242, 238)

    # Police de texte
    font = pygame.font.Font(None, 36)

    # Texte du bouton "Jouer"
    leveldown_text = font.render("Moins difficile!", True, COLOR)
    leveldown_rect = leveldown_text.get_rect(center=(253, 485))

    levelup_text = font.render("Plus difficile !", True, COLOR)
    levelup_rect = levelup_text.get_rect(center=(253, 560))

    quit_text = font.render("Revenir", True, COLOR)
    quit_rect = quit_text.get_rect(center=(253, 645))

    buttons = [
    {"text": "Moins difficile!", "rect": leveldown_rect, "highlighted": False},
    {"text": "Plus difficile !", "rect": levelup_rect, "highlighted": False},
    {"text": "Revenir", "rect": quit_rect, "highlighted": False}
    ]
    while True:
        screen.blit(background, (0, 0))  

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Vérifier si la souris survole un bouton
        for button in buttons:
            if button["rect"].collidepoint(mouse_x, mouse_y):
                button["highlighted"] = True
            else:
                button["highlighted"] = False

        # Dessiner les boutons et le soulignement s'il la souris surlvol le boutton
        for button in buttons:
            # Dessiner le fond du bouton
            pygame.draw.rect(screen, BUTTON_COLOR, button["rect"])

            # Souligner le bouton s'il la souris surlvol le boutton
            if button["highlighted"]:
                pygame.draw.line(screen, COLOR, button["rect"].bottomleft, button["rect"].bottomright, 2)

            # Afficher le texte du bouton
            screen.blit(font.render(button["text"], True, COLOR), button["rect"].topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if leveldown_rect.collidepoint(mouse_x, mouse_y):
                    # Appeler la fonction FallingObject pour changer les contantes
                    FallingObject.decrease_level()
                    return None
                if levelup_rect.collidepoint(mouse_x, mouse_y):
                    # Appeler la fonction FallingObject pour changer les constantes
                    FallingObject.increase_level()
                    return None
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    # Revenir lorsque le bouton "Revenir" est pressé
                    return None

        clock.tick(30)


def launcher():
    pygame.init()

    clock = pygame.time.Clock()

    # Initialisation de l'écran
    screen = pygame.display.set_mode((500, 750))
    background = pygame.image.load("assets/launcher_background.jpg")
    background = pygame.transform.scale(background, (500, 750))  # Redimensionner l'image

    # Couleurs
    pygame.display.set_caption('pyFruits')

    # Couleurs
    COLOR = (215, 175, 237)
    BUTTON_COLOR = (253, 242, 238)

    # Police de texte
    font = pygame.font.Font(None, 36)

    # Texte du bouton "Jouer"
    play_text = font.render("Jouer", True, COLOR)
    play_rect = play_text.get_rect(center=(253, 485))

    level_text = font.render("Niveau", True, COLOR)
    level_rect = level_text.get_rect(center=(253, 560))

    quit_text = font.render("Quitter", True, COLOR)
    quit_rect = quit_text.get_rect(center=(253, 645))

    buttons = [
    {"text": "Jouer", "rect": play_rect, "highlighted": False},
    {"text": "Niveau", "rect": level_rect, "highlighted": False},
    {"text": "Quitter", "rect": quit_rect, "highlighted": False}
    ]
    while True:
        screen.blit(background, (0, 0))  

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Vérifier si la souris survole un bouton
        for button in buttons:
            if button["rect"].collidepoint(mouse_x, mouse_y):
                button["highlighted"] = True
            else:
                button["highlighted"] = False

        # Dessiner les boutons et le soulignement s'il la souris surlvol le boutton
        for button in buttons:
            # Dessiner le fond du bouton
            pygame.draw.rect(screen, BUTTON_COLOR, button["rect"])

            # Souligner le bouton s'il la souris surlvol le boutton
            if button["highlighted"]:
                pygame.draw.line(screen, COLOR, button["rect"].bottomleft, button["rect"].bottomright, 2)

            # Afficher le texte du bouton
            screen.blit(font.render(button["text"], True, COLOR), button["rect"].topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_x, mouse_y):
                    # Appeler la fonction main() lorsque le bouton "Jouer" est pressé
                    main()
                    replay_text = font.render("Rejouer", True, COLOR)
                    replay_rect = replay_text.get_rect(center=(255, 485))
                    buttons[0]["text"] = "Rejouer"
                    buttons[0]["rect"] = replay_rect
                if level_rect.collidepoint(mouse_x, mouse_y):
                    # Appeler la fonction level() lorsque le bouton "Niveau" est pressé
                    level()
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    # Quitter lorsque le bouton "Quitter" est pressé
                    pygame.quit()
                    sys.exit()

        clock.tick(30)

if __name__ == "__main__":
    launcher()