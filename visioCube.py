"""
Yann LANCELIN / Esteban-Angel GONZALEZ-DURAND
03/2025 - 07/05/2025

-------

Descriptif:
    Permet de déterminer le cube par reconnaissance de couleur
    à l'aide des librairies:
        - OpenCV
        - Numpy
        - MultiCam (interne)

-------

Changelog:
    V1.0.0 (Version projet global: V1.4.0):
        Reconnaissance du cube à partir de la caméra et de l'interface image OpenCV
"""
import time
import json
import cv2
import numpy as np
import modeleCube

# CAM 0/A: B-R-D
# CAM 1/B: U-R-F
# CAM 2/C: U-B-L
# CAM 3/D: L-F-D

autor = 'Grégory COUTABLE'
version = '1.4.0_projet'
date = '14/03/2025'

# Couleurs de base
base_couleurs = {
    0: [50, 30, 172],   # Rouge
    1: [123, 62, 7],    # Bleu
    2: [52, 134, 40],   # Vert
    3: [17, 190, 182],  # Jaune
    4: [63, 90, 193],   # Orange
    5: [212, 211, 216], # Blanc
}

# Noms des couleurs
nom_couleurs = {
    0: 'F',
    1: 'R',
    2: 'L',
    3: 'D',
    4: 'B',
    5: 'U'
}

# Ordre des faces
ordre_faces = 'LFRBUD'

# Caméras et faces respectives
cam_faces = {
    0: ['D', 'R', 'B'],     # Cam A
    1: ['U', 'R', 'F'],     # Cam B
    2: ['U', 'B', 'L'],     # Cam C
    3: ['L', 'F', 'D']      # Cam D
}

class PointMesure:
    """
    Classe représentant un point de mesure sur le Rubik's cube.
    Contient les coordonnées, l'identifiant de la face et la couleur mesurée.
    Attributs:
        - x: Coordonnée x du point.
        - y: Coordonnée y du point.
        - face_id: Identifiant de la face (U, D, F, B, L, R).
        - couleur: Couleur mesurée (0-5).
    Méthodes:
        - __init__(): Initialise le point de mesure.
        - __str__(): Représentation en chaîne du point de mesure.
        - capture(x, y, face_id, couleur): Capture les données du point de mesure.
    """
    def __init__(self, x=0, y=0, face_id=''):
        """
        Initialisation du point de mesure.
        """
        self.x = x
        self.y = y
        self.face_id = face_id

    def __str__(self):
        """
        Représentation en chaîne du point de mesure.
        :return: Chaîne formatée.
        """
        return f"PointMesure(x={self.x}, y={self.y}, face_id='{self.face_id}', couleur={self.couleur})"

    def capture(self, x, y, face_id, couleur):
        """
        Capture les données du point de mesure.
        :param x: Coordonnée x.
        :param y: Coordonnée y.
        :param face_id: Identifiant de la face.
        :param couleur: Couleur mesurée.
        """
        self.x = x
        self.y = y
        self.face_id = face_id
        print(f"PointMesure capturé: {self}")

# Pixels à check pour chaque caméra
pixels_check = [
    PointMesure(x=190, y=229, face_id='R'),
    PointMesure(x=214, y=197, face_id='R'),
    PointMesure(x=245, y=154, face_id='R'),
    PointMesure(x=213, y=297, face_id='R'),
    PointMesure(x=232, y=237, face_id='R'),
    PointMesure(x=270, y=205, face_id='R'),
    PointMesure(x=247, y=339, face_id='R'),
    PointMesure(x=275, y=284, face_id='R'),
    PointMesure(x=304, y=238, face_id='R'),

    PointMesure(x=274, y=131, face_id='B'),
    PointMesure(x=319, y=138, face_id='B'),
    PointMesure(x=338, y=138, face_id='B'),
    PointMesure(x=309, y=179, face_id='B'),
    PointMesure(x=368, y=304, face_id='B'),
    PointMesure(x=394, y=194, face_id='B'),
    PointMesure(x=341, y=214, face_id='B'),
    PointMesure(x=381, y=218, face_id='B'),
    PointMesure(x=418, y=222, face_id='B'),

    PointMesure(x=348, y=267, face_id='D'),
    PointMesure(x=383, y=262, face_id='D'),
    PointMesure(x=415, y=266, face_id='D'),
    PointMesure(x=320, y=298, face_id='D'),
    PointMesure(x=365, y=175, face_id='D'),
    PointMesure(x=392, y=296, face_id='D'),
    PointMesure(x=278, y=341, face_id='D'),
    PointMesure(x=322, y=344, face_id='D'),
    PointMesure(x=349, y=342, face_id='D'),

    PointMesure(x=208, y=275, face_id='F'),
    PointMesure(x=240, y=269, face_id='F'),
    PointMesure(x=297, y=269, face_id='F'),
    PointMesure(x=237, y=297, face_id='F'),
    PointMesure(x=282, y=313, face_id='F'),
    PointMesure(x=332, y=317, face_id='F'),
    PointMesure(x=285, y=350, face_id='F'),
    PointMesure(x=316, y=349, face_id='F'),
    PointMesure(x=342, y=342, face_id='F'),

    PointMesure(x=271, y=145, face_id='U'),
    PointMesure(x=312, y=139, face_id='U'),
    PointMesure(x=350, y=130, face_id='U'),
    PointMesure(x=242, y=190, face_id='U'),
    PointMesure(x=288, y=176, face_id='U'),
    PointMesure(x=315, y=173, face_id='U'),
    PointMesure(x=211, y=226, face_id='U'),
    PointMesure(x=248, y=230, face_id='U'),
    PointMesure(x=279, y=226, face_id='U'),

    PointMesure(x=338, y=228, face_id='L'),
    PointMesure(x=357, y=178, face_id='L'),
    PointMesure(x=401, y=158, face_id='L'),
    PointMesure(x=366, y=279, face_id='L'),
    PointMesure(x=391, y=243, face_id='L'),
    PointMesure(x=420, y=193, face_id='L'),
    PointMesure(x=392, y=312, face_id='L'),
    PointMesure(x=423, y=287, face_id='L'),
    PointMesure(x=443, y=256, face_id='L'),
]

def preprocess_image(image):
    """
    Prétraitement de l'image : conversion RGB vers BGR, redimensionnement, lissage.
    :param image: Image brute.
    :return: Image prétraitée ou None si erreur.
    """
    if image is None:
        return None
    img = np.array(image)[:, :, ::-1].copy()  # RGB vers BGR
    img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)
    img = cv2.GaussianBlur(img, (5, 5), 0)  # Réduction du bruit
    return img

class Camera:
    """
    Classe de gestion des caméras.
    Gère l'initialisation, la capture d'images et la vérification de l'état.
    Méthodes:
        - __init__(): Initialise la caméra et vérifie son état.
        - prendrePhoto(side): Prend une photo pour le côté donné (A, B, C, D).
    """
    def __init__(self):
        """
        Initialisation de la caméra avec vérification.
        """
        try:
            from multiCam import MultiCamera
            self.multi = MultiCamera()
            test_img = self.multi.getPillImage('A')
            if test_img is None:
                raise ValueError("Caméra A non détectée")
        except Exception as e:
            print(f"Erreur d'initialisation des caméras : {e}")
            self.multi = None

    def prendrePhoto(self, side):
        """
        Prend une photo pour le côté donné.
        :param side: Côté de la caméra (A, B, C, D).
        :return: Image capturée ou None si erreur.
        """
        if self.multi is None:
            print(f"Caméra non disponible pour le côté {side}")
            return None
        time.sleep(1)  # Stabilisation
        return self.multi.getPillImage(side)

class IHMvisio:
    """
    Classe d'interface de visualisation pour la reconnaissance des couleurs.
    Gère la capture d'images, le traitement et l'affichage.
    Méthodes:
        - refresh(): Récupère les nouvelles images des caméras.
    """
    def __init__(self):
        """
        Initialisation de l'interface de visualisation.
        """
        self.camera = Camera()
        time.sleep(2)
        self.images = []

    def refresh(self):
        """
        Récupère les nouvelles images des caméras.
        :return: Liste des images ou None si erreur.
        """
        if self.camera is None or self.camera.multi is None:
            print("Aucune caméra disponible")
            return None
        del self.images[:]
        for side in 'ABCD':
            img = self.camera.prendrePhoto(side)
            img = preprocess_image(img)
            if img is not None:
                self.images.append(img)
            else:
                print(f"Échec capture pour la caméra {side}")
        return self.images

class Reconnaissance:
    """
    Classe de reconnaissance des couleurs du Rubik's cube.
    Gère la capture d'images, le traitement des couleurs et l'affichage.
    """
    def __init__(self):
        """
        Initialisation de la reconnaissance des couleurs.
        :return: None
        """
        self.ihm_visio = IHMvisio()                                             # Initialisation de l'IHM visio
        self.imgs = self.ihm_visio.refresh()                                    # Récupération des images
        if not self.imgs or len(self.imgs) != 4:
            raise ValueError("Échec de la capture des images des caméras")

        self.cube = modeleCube.Cube()                                           # Initialisation du cube
        self.faces = {'U': [], 'D': [], 'F': [], 'B': [], 'L': [], 'R': []}     # Initialisation des faces
        self.maxi = 9 * len(self.faces)                                         # 54 cases
        self.current_index = 0                                                  # Index de la caméra actuelle
        self.current_img = self.imgs[self.current_index]                        # Image actuelle
        self.len_rect = 3                                                       # Longueur du rectangle affiché quand on clique
        self.current_face_index = 0                                             # Index de la face actuelle
        self.current_piece_index = 0                                            # Index de la pièce actuelle

        import os
        try:
            os.remove('cube.json')
        except FileNotFoundError:
            print("cube.json introuvable, création nouveau fichier")
        except Exception as e:
            print(f"Erreur suppression cube.json: {e}")

    def load_img(self, index):
        """
        Charge l'image de la caméra spécifiée.
        :param index: Index de la caméra (0-3)
        :return: Image chargée ou None si erreur
        """
        self.current_index = index
        if self.current_index >= len(self.imgs):
            print("Erreur: index de l'image hors limites")
            return None
        self.current_img = self.imgs[self.current_index]
        if self.current_img is None:
            print("Erreur lors du chargement de l'image")
            return None
        self.current_face_index = 0
        return self.current_img

    def check_pixel(self, x, y, face_id=None):
        # Vérifier si la face actuelle est complète
        if face_id is None:
            if self.current_index >= len(cam_faces) or self.current_face_index >= len(cam_faces[self.current_index]):
                print("Erreur: toutes les faces ont été traitées")
                return
            current_face = cam_faces[self.current_index][self.current_face_index]
        else:
            current_face = face_id

        if len(self.faces[current_face]) >= 9:
            self.current_face_index += 1
            if self.current_face_index >= len(cam_faces[self.current_index]):
                print(f"Toutes les faces de la caméra {self.current_index} sont complètes")
                self.current_index += 1
                return
            current_face = cam_faces[self.current_index][self.current_face_index]

        # Calcul de la couleur moyenne sur le rectangle 3x3
        pixels = self.current_img[y:y+self.len_rect, x:x+self.len_rect]
        if pixels.size == 0:
            print("Clic hors de l'image")
            return
        mean_color = np.mean(pixels, axis=(0, 1)).astype(int)

        # Calcul de la distance couleurs
        distances = []
        for couleur in base_couleurs.values():
            dist = np.sqrt(
                (mean_color[0] - couleur[0]) ** 2 +
                (mean_color[1] - couleur[1]) ** 2 +
                (mean_color[2] - couleur[2]) ** 2
            )
            distances.append(dist)

        # Identification de la couleur
        index = distances.index(min(distances))
        if min(distances) > 80:  # Seuil ajustable
            print("Couleur non reconnue")
            return
        couleur = nom_couleurs[index]

        # Ajouter la couleur à la case correspondante
        face_pos = self.current_piece_index
        self.cube.cube[current_face].setPiece(face_pos, couleur)
        print(f"{current_face}[{face_pos}]: {couleur} ({nom_couleurs[index]}), {distances[index]}), {x}, {y}")

        # Vérifier si la face est complète
        self.current_piece_index += 1
        if self.current_piece_index >= 9:
            self.current_face_index += 1
            self.current_piece_index = 0
            if self.current_face_index >= len(cam_faces[self.current_index]):
                self.current_index += 1

        # Vérifier si le cube est complet
        if sum(len(self.cube.cube[face].__repr__().replace('x', '')) for face in self.cube.cube) >= self.maxi:
            print("Cube complet")
            with open('cube.json', 'w') as f:
                json.dump({face: self.cube.cube[face].__repr__() for face in ordre_faces}, f)

    def start(self):
        """
        Démarre la reconnaissance des couleurs.
        :return: None
        """
        for point in pixels_check:
            self.check_pixel(point.x, point.y, point.face_id)

    def cube2str(self):
        """
        Convertit le cube en chaîne de caractères compatible avec Cube.__repr__.
        :return: Représentation en chaîne du cube (54 caractères, ordre URFDLB).
        """
        return self.cube.__repr__()

if __name__ == "__main__":
    """
    Point d'entrée principal pour la reconnaissance des couleurs.
    """
    recon = Reconnaissance()
    recon.start()
    print("Reconnaissance terminée")
    print(recon.cube2str())