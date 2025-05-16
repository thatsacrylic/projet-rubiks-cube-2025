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
    5: [172, 167, 157], # Blanc
}

# Juste pour le debug
nom_couleurs = {
    0: 'Rouge',
    1: 'Bleu',
    2: 'Vert',
    3: 'Jaune',
    4: 'Orange',
    5: 'Blanc'
}

# Ordre des faces (U, D, F, B, L, R)
ordre_faces = ['U', 'D', 'F', 'B', 'L', 'R']

# Caméras et faces respectives
cam_faces = {
    0: ['D', 'R', 'B'],     # Cam A
    1: ['U', 'R', 'F'],     # Cam B
    2: ['U', 'B', 'L'],     # Cam C
    3: ['L', 'F', 'D']      # Cam D
}

#TODO JSON

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
    def __init__(self):
        """
        Initialisation du point de mesure.
        """
        self.x = 0
        self.y = 0
        self.face_id = ''
        self.couleur = 0
    
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
        self.couleur = couleur
        print(f"PointMesure capturé: {self}")

class Reconnaissance:
    """
    Classe de reconnaissance des couleurs du Rubik's cube.
    Gère la capture d'images, le traitement des couleurs et l'affichage.

    Méthodes:
        - load_img(index): Charge l'image de la caméra spécifiée.
        - draw_rect(x, y): Dessine un rectangle sur l'image aux coordonnées données.
        - get_click(event, x, y, flags, param): Gère les clics de souris pour identifier les couleurs.
        - next_camera(): Passe à la caméra suivante si disponible.
        - open_img_window(): Ouvre la fenêtre d'affichage de l'image.
        - update_display(): Met à jour l'affichage avec les faces et les instructions.
        - img_update(): Gère les entrées clavier et met à jour l'affichage.
    Utilisation:
        - Créer une instance de la classe et appeler load_img(index de base, 0 par exemple) pour commencer.
        - Boucle principale pour gérer les événements jusqu'à ce que l'utilisateur quitte.
        - Les résultats sont enregistrés dans un fichier JSON 'cube.json'.
    Exemple:
        recon = Reconnaissance()
        recon.load_img(0)
        while recon.running:
            recon.img_update()
            if not recon.running:
                break
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
        self.points_global = []                                                 # Liste des points sélectionnés
        self.running = True                                                     # État de l'application
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
        self.open_img_window()
        return self.current_img

    def draw_rect(self, x, y):
        """
        Dessine un rectangle sur l'image aux coordonnées données.
        :param x, y: Coordonnées du coin supérieur gauche.
        :return: None
        """
        cv2.rectangle(self.current_img, (x, y), (x + self.len_rect, y + self.len_rect), (100, 100, 100), -1)

    def get_click(self, event, x, y, flags, param):
        """
        Gère les clics de souris pour identifier les couleurs.
        :param event: Événement OpenCV
        :param x, y: Coordonnées du clic
        :return: None
        """
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        # Vérifier si la face actuelle est complète
        current_face = cam_faces[self.current_index][self.current_face_index]
        if len(self.faces[current_face]) >= 9:
            self.current_face_index += 1
            if self.current_face_index >= len(cam_faces[self.current_index]):
                print(f"Toutes les faces de la caméra {self.current_index} sont complètes")
                self.next_camera()
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
        couleur = list(base_couleurs.keys())[index]
        self.points_global.append([x, y])

        # Ajouter la couleur à la case correspondante
        face_pos = self.current_piece_index
        self.cube.cube[current_face].setPiece(face_pos, couleur)
        print(f"{current_face}[{face_pos}]: {couleur} ({nom_couleurs[index]})")
        self.draw_rect(x, y)
        self.update_display()

        # Vérifier si la face est complète
        self.current_piece_index += 1
        if self.current_piece_index >= 9:
            self.current_face_index += 1
            self.current_piece_index = 0
            if self.current_face_index >= len(cam_faces[self.current_index]):
                self.next_camera()

        # Vérifier si le cube est complet
        if sum(len(self.cube.cube[face].__repr__().replace('x', '')) for face in self.cube.cube) >= self.maxi:
            print("Cube complet")
            self.running = False
            with open('cube.json', 'w') as f:
                json.dump({face: self.cube.cube[face].__repr__() for face in ordre_faces}, f)
            cv2.destroyAllWindows()

    def next_camera(self):
        """
        Passe à la caméra suivante si disponible.
        :return: None
        """
        self.current_index += 1
        if self.current_index < len(self.imgs):
            self.load_img(self.current_index)
        else:
            print("Toutes les caméras ont été traitées")
            self.running = False

    def open_img_window(self):
        """
        Ouvre la fenêtre d'affichage de l'image.
        :return: None
        """
        cv2.namedWindow('Rubiks Cube')
        cv2.resizeWindow('Rubiks Cube', self.current_img.shape[1], self.current_img.shape[0])
        cv2.setMouseCallback('Rubiks Cube', self.get_click)
        self.update_display()

    def update_display(self):
        """
        Met à jour l'affichage avec les faces et les instructions.
        :return: None
        """
        display_img = self.current_img.copy()
        for point in self.points_global:
            self.draw_rect(point[0], point[1])
        # Afficher les faces complétées
        for i, face in enumerate(ordre_faces):
            if len(self.faces[face]) > 0:
                cv2.putText(display_img, face, (10 + i * 25, 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        # Instruction pour la face en cours
        if self.current_face_index < len(cam_faces[self.current_index])-1:
            current_face = cam_faces[self.current_index][self.current_face_index]
            cv2.putText(display_img, f"Cliquez sur la face {current_face}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.imshow('Rubiks Cube', display_img)

    def img_update(self):
        """
        Gère les entrées clavier et met à jour l'affichage.
        :return: None
        """
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Échap
            self.running = False
            cv2.destroyAllWindows()
        elif key == 8:  # Retour arrière
            if self.points_global:
                # Supprimer la dernière couleur ajoutée
                current_face = cam_faces[self.current_index][self.current_face_index]
                if len(self.faces[current_face]) > 0:
                    self.faces[current_face].pop()  # Supprimer la dernière couleur
                    self.points_global.pop()        # Supprimer le dernier point
                    self.update_display()
                elif self.current_face_index > 0:
                    self.current_face_index -= 1
                    current_face = cam_faces[self.current_index][self.current_face_index]
                    if len(self.faces[current_face]) > 0:
                        self.faces[current_face].pop()
                        self.points_global.pop()
                    self.update_display()
        
    def cube2str(self):
        """
        Convertit le cube en chaîne de caractères compatible avec Cube.__repr__.
        :return: Représentation en chaîne du cube (54 caractères, ordre URFDLB).
        """
        return self.cube.__repr__()

if __name__ == "__main__":
    try:
        recon = Reconnaissance()
        recon.load_img(0)
        while recon.running:
            recon.img_update()
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        cv2.destroyAllWindows()