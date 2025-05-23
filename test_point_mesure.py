from modeleCube import Cube
#from reconnaissance_video_V1_8 import Reference_color

autor = 'Esteban-angel GONZALEZ-DURAND'
version = '1.1'
date = '21/05/2025'

import cv2
import pygame
import numpy as np
from math import sqrt

# Variables globales
camera = cv2.VideoCapture(1) # saisi de la caméra utilisé
image = [] # c'est l'image
color = {} # dictionnaire qui contient les différentes couleurs
color = {'F':[170, 30, 16],'U':[178, 189, 197],'L':[31, 141, 19],'D':[160, 196, 24],'B':[255, 152, 55],'R':[10, 60, 166]}

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


class PointDeMesure:
    def __init__(self, pos, face_img, num_piece):
        self.position = pos
        self.face_img = face_img
        self.num_piece = num_piece
        
    def distance(self, point):
        #print(self.position, point.position)
        return ((self.position[0] - point.position[0])**2 + (self.position[1] - point.position[1])**2) ** 0.5

    def __repr__(self):
        return str(self.position)# + str(self.num_piece)
    
    def recuperer_pixel_autour(self, pos, n=10):
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
    
    def couleur(self, image):
        face = 'FRUBLD'
        distances = [float('inf') for i in range(6)]
        
        R2, G2, B2 = self.recuperer_pixel_autour(self.position)
        
        for i in range(6):
            R1, G1, B1 = color.get(face[i])
            distances[i] = sqrt((R2 - R1)**2 + (G2 - G1)**2 + (B2 - B1)**2)
            
        i_mini = 0
        for i in range(6):
            if distances[i] < distances[i_mini]:
                i_mini = i
                    
        return face[i_mini]


points_de_mesure = []
points_de_mesure.append(PointDeMesure((195, 80), 'U', 0))
points_de_mesure.append(PointDeMesure((220, 140), 0, 3))
points_de_mesure.append(PointDeMesure((270, 221), 0, 6))
points_de_mesure.append(PointDeMesure((400, 170), 0, 7))
points_de_mesure.append(PointDeMesure((500, 150), 0, 8))
points_de_mesure.append(PointDeMesure((435, 70), 0, 5))
points_de_mesure.append(PointDeMesure((390, 35), 0, 2))
points_de_mesure.append(PointDeMesure((280, 50), 0, 1))

points_de_mesure.append(PointDeMesure((300, 280), 'F', 0))
points_de_mesure.append(PointDeMesure((310, 370), 1, 3))
points_de_mesure.append(PointDeMesure((310, 435), 1, 6))
points_de_mesure.append(PointDeMesure((400, 410), 1, 7))
points_de_mesure.append(PointDeMesure((500, 355), 1, 8))
points_de_mesure.append(PointDeMesure((500, 300), 1, 5))
points_de_mesure.append(PointDeMesure((520, 220), 1, 2))
points_de_mesure.append(PointDeMesure((420, 250), 1, 1))



prendre_photo()

c = Cube()

while True:

    c = wait_click()
    print(c)
    
    if c == '#E':
        ...
        print(c)




