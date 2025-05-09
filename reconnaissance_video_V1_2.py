"""
Version V1

Projet Robot resolveur de Rubik's Cube 2025

Reconnaissance du rubik's cube pour le robot avec une seule caméra

version:
V1.0 : version de départ du projet. Cette version contient juste les structures pour afficher une photo du cube.

V1.1 : +  nous renvoyer le code RGB d'un pixel cliqué avec la souris avec sa position.
V1.2 : +  nous renvoyer la moyenne des codes RGB des pixels autour du pixel cliqué.
"""

autor = 'Esteban-angel GONZALEZ-DURAND'
version = '1.2'
date = '09/05/2025'

import cv2
import pygame
import numpy as np

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("Erreur : caméra non accessible.")
    exit()
    
# On ignore les 10 premières frames pour laisser le temps à la caméra de s'ajuster
for i in range(10):
    camera.read()
    
# Affiche les dimensions
largeur = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
hauteur = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f'Taille : {largeur}*{hauteur}')    

# définition de la page
pygame.init()
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Webcam avec Pygame")


def prendre_photo():
    # Maintenant on capture l'image propre
    is_reading, img = camera.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.rot90(img)  # Rotation pour affichage correct si nécessaire
   
    return img

def recuperer_pixel_autour(x0, y0, n):
    '''
    On récupère les n*n pixels autour de celui sur lequel on a cliqué puis en fait la moyenne
    
    return code RGB (ex: [102 87 77])
    '''
    r, v, b = 0, 0, 0
    for x in range(x0 - n // 2 + 1, x0 + n // 2 + 1):
        for y in range(y0 - n // 2 + 1, y0 + n // 2 + 1):
            px = img[x][y]
            r = r + int(px[0])
            v = v + int(px[1])
            b = b + int(px[2])
    moy_r = r // n**2
    moy_v = v // n**2
    moy_b = b // n**2
    return [moy_r, moy_v, moy_b]

# Affichage dans la fenêtre Pygame
img = prendre_photo()
screen.blit(pygame.surfarray.make_surface(img), (0, 0))
pygame.display.flip()

while True:

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            camera.release()
            exit()

        # Appuie sur le clic gauche pour avoir sa position et son code RGB
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.pos) #coordonnées du clique
            u = img[event.pos[0]][event.pos[1]]
#             print(u, type(u), u[0])
#             for c in u:
#                 print(c)
            print(recuperer_pixel_autour(event.pos[0], event.pos[1], 6))
            
                
                
                
#                 cv2.imwrite("capture_depuis_pygame.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
#                 print("Image capturée !")
#                 img_saved = True


