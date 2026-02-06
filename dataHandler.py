import pygame  # Importation de la bibliothèque Pygame
import cv2  # Importation de la bibliothèque OpenCV (pip install opencv-python)

#definition des classes
class Player:
    def __init__(self):
        # Nombre de fruits restant
        self.score = 30

    def draw(self, screen):
        # Dessiner le joueur (dans ce cas, un simple texte pour afficher le score)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Fruit: {self.score} restant", True, (6, 10, 43))
        screen.blit(score_text, (10, 10))

    def update_fruits(self):
        # Mise à jour du nombre de fruits restant
        self.score -= 1
    
    def check_end(self):
        # Vérification si le nombre de fruit demandé est atteint
        if self.score <= 0:
            return True
        else :
            return False
        
    def end_mesage(self, screen):
        # Check si le joueur a perdu ou gagné
        if self.score > 0 :
            message = "Arrhhrh !"
        else :
            message = "Bien joué !"

        # Supprimer ce qui est présent sur l'écran
        screen.fill((255,255,255))

        # Ecrire le message
        font = pygame.font.Font(None, 48)
        message_text = font.render(message, True, (255, 253, 228))
        message_rect = message_text.get_rect(center=(255,300))

        #Afficher le background
        background = pygame.image.load("assets/game_background.png")
        background = pygame.transform.scale(background, (500, 750))
        screen.blit(background, (0,0))

        #Afficher le message
        screen.blit(message_text, message_rect.topleft)
        
        # Laisser le message pendant 1 seconde
        pygame.display.flip()
        pygame.time.delay(500)

            
class FallingObject:
    # Constantes
    GRAVITY = 0.2
    AIR_RESISTANCE = 0.02
    ELASTICITY = 0.02   
    
    def __init__(self, image_path, start_x, start_y):
        # Initialisation
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (start_x - (cv2.imread(image_path).shape[1]/2), start_y) # centre l'image
        self.is_falling = False
        self.x = start_x - (cv2.imread(image_path).shape[1]/2)
        self.rect.y = 0 - cv2.imread(image_path).shape[1]
        self.velocity_y = 0

    def start_fall(self):
        self.is_falling = True

    def update(self, start_x):
        if self.is_falling:
            # Calculer la nouvelle vitesse en fonction de la gravité et de la résistance de l'air
            self.velocity_y += FallingObject.GRAVITY - self.velocity_y * FallingObject.AIR_RESISTANCE
            # Mettre à jour la position de l'objet en fonction de la vitesse
            self.rect.y += self.velocity_y

            # Mettre à jour la position de l'objet (descendre progressivement)
            if self.rect.y >= 880 - self.rect.height:
                # Remettre l'objet en bas de l'écran au pire des cas
                self.rect.y = 880 - self.rect.height
                self.velocity_y = 0
                self.velocity_y *= -FallingObject.ELASTICITY
                if abs(self.velocity_y) < 1:
                    self.velocity_y = 0
        else:
            self.rect.x = start_x + self.x

    def is_clicked(self, mouse_pos):
        # Vérifier si le clic de souris est sur l'objet
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # Dessiner l'objet sur l'écran
        screen.blit(self.image, self.rect.topleft)

    def increase_level():
        FallingObject.GRAVITY += 0.1
        FallingObject.ELASTICITY += 0.1

    def decrease_level():
        FallingObject.GRAVITY -= 0.2
        FallingObject.AIR_RESISTANCE += 0.01
        FallingObject.ELASTICITY -= 0.5
        if FallingObject.GRAVITY <= 0 or FallingObject.ELASTICITY <= 0:
            FallingObject.GRAVITY = 0.1
            FallingObject.ELASTICITY = 0.1