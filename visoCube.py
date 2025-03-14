"""
Yann LANCELIN / Esteban-Angel GONZALEZ-DURAND
03/2025

V1:
Reconnaissance du cube à partir de la caméra
"""
from multiCam import MultiCamera
import time

# todo: commentaires

autor = 'Grégory COUTABLE'
version = '1.4.0_projet'
date = '14/03/2025'

class Reconnaissance:
    def __init__(self):
        pass
    
    def parametrer(self):
        pass
    
    def sauvegardeJSON(self):
        pass 
    
    def recuperationJSON(self):
        pass

class IHMvisio:
    def __init__(self):
        self.camera = Camera()
        self.images = []

    def waitClick(self):
        # if self.camera != None
        return ""

    # todo: afficher sur ihm
    def refresh(self):
        if self.camera is not None:
            del self.images[:]
            for item in 'ABCD':
                img = self.camera.prendrePhoto(item)
                self.images.append(img)

    def appendCamera(self, cam):
        pass
    
class Camera:
    def __init__(self):
        self.multi = MultiCamera()
    
    def prendrePhoto(self, side):       #ABCD (4)
        time.sleep(1)
        return multi.getPillImage(side)

class pointMesure:
    def __init__(self):
        pass