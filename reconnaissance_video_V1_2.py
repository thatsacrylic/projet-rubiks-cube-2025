"""
Version V1

Projet Robot resolveur de Rubik's Cube 2024-2025

Reconnaissance du rubik's cube pour le robot avec une seule caméra

version:
V1.0 : version de départ du projet. Cette version contient juste les structures pour afficher une photo du cube.

V1.1 : +  nous renvoyer le code RGB d'un pixel cliqué avec la souris avec sa position.
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

# 
pygame.init()
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Webcam avec Pygame")


def prendre_photo():
    # Maintenant on capture l'image propre
    is_reading, img = camera.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.rot90(img)  # Rotation pour affichage correct si nécessaire
   
    return img

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

        # Appuie sur la touche ESPACE pour capturer une image
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.pos) #coordonnées du clique
            print(img[event.pos[0]][event.pos[1]])
            
                
                
                
#                 cv2.imwrite("capture_depuis_pygame.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
#                 print("Image capturée !")
#                 img_saved = True
