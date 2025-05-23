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
version = '1.9'
date = '21/05/2025'

import cv2
import pygame
import numpy as np
from math import sqrt

# Variables globales
camera = cv2.VideoCapture(1) # saisi de la caméra utilisé
image = [] # c'est l'image
color = {} # dictionnaire qui contient les différentes couleurs


if not camera.isOpened(): # si caméra non disponible
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
    global image
    # Maintenant on capture l'image propre
    is_reading, img = camera.read()
    if is_reading:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = np.rot90(img)  # Rotation pour affichage correct si nécessaire
        screen.blit(pygame.surfarray.make_surface(image), (0, 0))
        pygame.display.flip()


def recuperer_pixel_autour(pos, n=10):
    '''
    On récupère les n*n pixels autour de celui sur lequel on a cliqué puis en fait la moyenne
    
    return code RGB (ex: [102 87 77])
    '''
    x0, y0 = pos
    r, v, b = 0, 0, 0
    for x in range(x0 - n // 2 + 1, x0 + n // 2 + 1):
        for y in range(y0 - n // 2 + 1, y0 + n // 2 + 1):
            px = image[x][y]
            r = r + int(px[0])
            v = v + int(px[1])
            b = b + int(px[2])
    moy_r = r // n**2
    moy_v = v // n**2
    moy_b = b // n**2
    
    return [moy_r, moy_v, moy_b]


def wait_click():
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                prendre_photo()
                return None
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                camera.release()
                exit()

            # Appuie sur le clic gauche pour avoir sa position et son code RGB
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return event.pos
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return '#E'
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                new_click = event.pos
                return new_click

def moyenne_n_points(pts):
    '''
    fonction qui fait la moyenne des n points séléctionnés
    
    return list (ex:[193, 208, 219])
    '''
    a = len(points)
    r,v,b = 0,0,0
    for o in range(a):
        color_pts = points[o]
        r = r + int(color_pts[0])
        v = v + int(color_pts[1])
        b = b + int(color_pts[2])
    moy_r = r // a
    moy_v = v // a
    moy_b = b // a
    return [moy_r, moy_v, moy_b]

def stocker_moy_dans_color(col, face):
    '''
    fonction qui stocke les moyennes des n points séléctionnés
    color (ex:{'color_red':[193, 208, 219], ... ,'color_orange':[193, 208, 219]})
    '''
    assert face in 'FRUBLD', 'couleur non valide'
    assert isinstance(col, list) and len(col) == 3, 'typeError'
    global color
    color[face] = col

def calc_dist_couleur(new_click):
    
    face = 'FRUBLD'
    distances = [float('inf') for i in range(6)]
    
    R2, G2, B2 = recuperer_pixel_autour(new_click)
    
    for i in range(6):
        R1, G1, B1 = color.get(face[i])
        distances[i] = sqrt((R2 - R1)**2 + (G2 - G1)**2 + (B2 - B1)**2)
        
    i_mini = 0
    for i in range(6):
        if distances[i] < distances[i_mini]:
            i_mini = i
                
    return face[i_mini]
    

# Affichage dans la fenêtre Pygame


prendre_photo()

points = []

while True:

    c = wait_click()
    print(c)
    
    if c == '#E':
        print(points)
        col = moyenne_n_points(points)
        print(col)
        face = input('Quelle face dans FRUBLD ? ')
        stocker_moy_dans_color(col, face)
        points = []
    
    if isinstance(c, tuple):
        px_moy = recuperer_pixel_autour(c)
        print(px_moy)
        points.append(px_moy)
        
        if len(color) == 6 :
            print(c)
            print(calc_dist_couleur(c))
            
       
       
#                 cv2.imwrite("capture_depuis_pygame.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
#                 print("Image capturée !")
#                 img_saved = True


