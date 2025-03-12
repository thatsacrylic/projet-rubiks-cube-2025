"""
Projet Robot resolveur de Rubik's Cube 2022

Classes pour la reconnaissance des faces du cube.
Inclus l'écran de paramétrage.

version:
V1.1 :
V1.2 : ajout de la caméra D et de bouton de mouvement pour tester les moteurs
V1.3 : modification de l'algo des knn : un fichier couleur par camera
"""

autor = 'Grégory COUTABLE'
version = '1.2'
date = '27/12/2024'


import pygame
from pygame.locals import *
import ihmCube
from ihmCube import ImgFace, ImgCube, Bouton, Click, CKCUBE, CKBOUTON, CKPOSITION
from modeleCube import Cube
import json
from PIL import Image
import multiCam


import os
pathname = os.path.dirname(__file__)

#on va définir une série de constantes
WSCREEN = ihmCube.WSCREEN
HSCREEN = ihmCube.HSCREEN

WCAMERA = multiCam.WIDTH
HCAMERA = multiCam.HEIGHT

# dimensions du mini cube
WCASEMINI = 30
DFACEMINI = 6
DCUBEMINI = 20
PMX0 = 240
PMY0 = 25
PMDX = 15
PMDY = 15

WBP = ihmCube.WBP
HBP = ihmCube.HBP
YBP = ihmCube.YBP
XBP = ihmCube.XBP + 40
XBP2 = ihmCube.XBP - WBP + 10
DBP = ihmCube.DBP
NBPCLN = 7
TEXTBP = ['CAMÉRA 1', 'CAMÉRA 2', 'CAMÉRA 3', 'CAMÉRA 4', 'RECADRAGE', 'RESET POINT', 'EFFACER POINT', 'MESURER', 'RESET MESURES', 'RECONNAITRE', 'ECLAIRER +', 'ECLAIRER -', 'QUITTER']
print(XBP, XBP2)

WBP3 = 50
HBP3 = 50
YBP3 = 650
XBP3 = 10
DBP3 = 10

WZONETXT1 = 400
HZONETXT1 = 300
XZONETXT1 = 15
YZONETXT1 = 330
COLORTXT1 = pygame.Color('#FFFF00')

COLORPMY = pygame.Color('#00FF00')
COLORPMN = pygame.Color('#FF0000')

WMESURE = 10

class Reconnaissance(object):
    def __init__(self, n, cube, robot = None):
        # nb  de caméra
        self.n = n
        self.visio = IHMvisio()
        
        self.cube = cube
        self.multi = multiCam.MultiCamera()
        
        if robot is None:
            robot = Robot()
        self.robot = robot
        
        for i in range(n):
            self.visio.appendCamera(Camera(i, self.multi))
        
        self.recuperationJSON()
        
        self.numCam = 0
        self.visio.bp[self.numCam].presser()
        self._affiche_nb_mesure()
        
        self.etapeRecadrage = 0
        
    def reconnaitre(self):
        self.visio.reconnaitre(self.cube)

    def _affiche_nb_mesure(self):
        txt = ""
        for f in Camera.dicoCouleur:
            txt += F"{f} : {len(Camera.dicoCouleur[f])} mesures\n"
        self.visio.setText1(txt)        
    
    def parametrer(self):
        pmFocused = None
        
        while True:
            
            pygame.time.Clock().tick(30)
            
            self.visio.refresh(self.numCam)
            
            #if pygame.mouse.get_focused():
            event = self.visio.waitClick()
            
            if isinstance(event, Click):
                print(event)
                
                if event.type == CKBOUTON:
                    # CAMERA 1, 2, 3, 4
                    if 0 <= event.contenu <= 3:
                        self.visio.bp[self.numCam].relacher()
                        self.numCam = event.contenu
                        self.visio.bp[self.numCam].presser()
                        if pmFocused is not None:
                            pmFocused.resetFocus()
                            pmFocused = None
                        self._affiche_nb_mesure()
                    # RECADRAGE        
                    elif event.contenu == 4:
                        # on reinitialise l'echelle
                        self.visio.cameras[self.numCam].y1cut = 0
                        self.visio.cameras[self.numCam].y2cut = 100
                        # attention, les deux prochains click déterminerons le recadrage
                        self.visio.setText1("Cliquez sur le point haut")
                        self.etapeRecadrage = 3
                        
                    # RESET POINT        
                    elif event.contenu == 5:
                        self.visio.cameras[self.numCam].clearPM()
                    # EFFACER POINT    
                    elif event.contenu == 6:
                        if pmFocused is not None:
                            self.visio.cameras[self.numCam].removePM(pmFocused)
                            pmFocused = None
                    # MESURER
                    elif event.contenu == 7:
                        for cam in self.visio.cameras:
                            cam.apprentissage(self.cube)
                        self._affiche_nb_mesure()
                    # RESET MESURES
                    elif event.contenu == 8:
                        Camera.dicoCouleur = {c: [] for c in 'FRUBLD' }
                        self._affiche_nb_mesure()
                    # RECONNAITRE
                    elif event.contenu == 9:
                        self.visio.miniCube.clear()
                        self.visio.reconnaitre(self.visio.miniCube)
                    # ECLAIRAGE +
                    elif event.contenu == 10:
                        self.robot.setLed(self.robot.niveauLed + 50)
                    # ECLAIRAGE -
                    elif event.contenu == 11:
                        self.robot.setLed(self.robot.niveauLed - 50)
                    # QUITTER
                    elif event.contenu == len(TEXTBP) - 1:
                        self.sauvergardeJSON()
                        return
                    
                    elif event.contenu - len(TEXTBP) < 18:
                        i = event.contenu - len(TEXTBP)
                        self.robot.move(TEXTBP3[i])
                        self.cube.rotation(TEXTBP3[i])
                
                elif event.type == CKCUBE and (event.contenu - 4) % 9 != 0:
                    if pmFocused is not None:
                        pmFocused.resetFocus()
                    
                    pmFocused = self.visio.cameras[self.numCam].getPointsMesure(event.contenu)
                    if pmFocused is None:
                        pmFocused = PointMesure(WMESURE, event.contenu)
                        self.visio.cameras[self.numCam].ajoutePM(pmFocused)
                        pmFocused.setCenter((PMX0 + PMDX * (event.contenu % 9), PMY0 + (event.contenu // 9) * PMDY))
                        
                    pmFocused.setFocus()
                    
                elif event.type == CKPOSITION:
                    if self.etapeRecadrage > 0:
                        if self.etapeRecadrage == 3:
                            y1cut = event.contenu[1] * 100 / HSCREEN
                            self.visio.setText1("Cliquez sur le point bas")
                            print(F"y1cut = {y1cut} %")
                        elif self.etapeRecadrage == 2:
                            y2cut = event.contenu[1] * 100 / HSCREEN
                            self.visio.setText1("Cliquez sur le point droit")
                            print(F"y2cut = {y2cut} %")
                        else:
                            self.visio.cameras[self.numCam].y1cut = y1cut
                            self.visio.cameras[self.numCam].y2cut = y2cut
                            wCamInScreen = (WCAMERA * HSCREEN) // HCAMERA 
                            self.visio.cameras[self.numCam].x2cut = (event.contenu[0] - (WSCREEN - wCamInScreen) // 2) * 100 / wCamInScreen
                            print(event.contenu[0])
                            print(F"x2cut = {self.visio.cameras[self.numCam].x2cut} %")
                            self.visio.setText1("")
                        self.etapeRecadrage -= 1
                        
                    elif pmFocused is not None:
                        pmFocused.setCenter(event.contenu)


    def sauvergardeJSON(self):
        structJson = {"cameras": {}, "voisins": Camera.dicoCouleur, "robot": {"tempsPas": self.robot.tempsPas, "tempsPause": self.robot.tempsPause, "niveauLed": self.robot.niveauLed}}
        for cam in self.visio.cameras:
            dicoCam = {"PM": [], "recadrage": (cam.y1cut, cam.y2cut, cam.x2cut)}
            for pm in cam:
                dicoCam["PM"].append((pm.num, pm.getCenter()))
            
            structJson["cameras"][cam.name] = dicoCam

        print(structJson)                      
        with open(os.path.join(pathname, "src", 'data.json'), 'w') as f:
            json.dump(structJson, f)
        
    def recuperationJSON(self):
        with open(os.path.join(pathname, "src", 'data.json'), 'r') as f:
            structJson = json.load(f)
        
        self.robot.tempsPas = structJson["robot"]["tempsPas"]
        self.robot.tempsPause =  structJson["robot"]["tempsPause"]
        self.robot.niveauLed = structJson["robot"]["niveauLed"]
        self.robot.setParam()
        
        Camera.dicoCouleur = structJson["voisins"]
        
        for i in range(self.n):
            self.visio.cameras[i].y1cut = structJson["cameras"]['ABCD'[i]]["recadrage"][0]
            self.visio.cameras[i].y2cut = structJson["cameras"]['ABCD'[i]]["recadrage"][1]
            self.visio.cameras[i].x2cut = structJson["cameras"]['ABCD'[i]]["recadrage"][2]
            self.visio.cameras[i].clearPM()
            for pm in structJson["cameras"]['ABCD'[i]]["PM"]:
                print(pm)
                point = PointMesure(WMESURE, pm[0])
                point.setCenter(pm[1])
                self.visio.cameras[i].ajoutePM(point)
        for f in 'FRUBLD':
            print(Camera.dicoCouleur[f])

# class Robot(object):
#     def __init__(self):
#         self.tempsPas = 650
#         self.tempsPause = 1700
#         self.niveauLed = 100
#         
#         self.setParam()
# 
#     def setParam(self):
#         pass
#     
#     def setLed(self, value):
#         self.niveauLed = value
#         if self.niveauLed > 8191:
#             self.niveauLed = 8191
#         if self.niveauLed < 0:
#             self.niveauLed = 0
#         print(value)

class IHMvisio (object):
    def __init__(self):
        #cube est une instance de la classe Cube
        pygame.init()
        
        self.fenetre = pygame.display.set_mode((WSCREEN, HSCREEN))#, FULLSCREEN)

        pygame.display.set_caption("Vision Rubik's Cube")
        
        self.bp = [Bouton(WBP, HBP, txt) for txt in TEXTBP]
        
        for i in range(NBPCLN):
            self.bp[i].setRect(XBP2, YBP + i * (HBP + DBP))
        
        for i in range(len(self.bp) - NBPCLN):
            self.bp[i + NBPCLN].setRect(XBP, YBP + i * (HBP + DBP))
            
        self.bp_mvt = [Bouton(WBP3, HBP3, txt) for txt in [c + m for c in 'FRUBLD' for m in ("", "'", "2")]]
        
        for xi in range(6):
            for yi in range(3):
                i = yi + 3 * xi
                self.bp_mvt[i].setRect(XBP3 + xi * (HBP3 + DBP3), YBP3 + yi * (HBP3 + DBP3))
        
        
        self.miniCube = Cube()
        self.miniCube.reset()
        
        self.iMiniCube = ImgCube(WCASEMINI, DFACEMINI, DCUBEMINI, DCUBEMINI, self.miniCube)
        
        self.cameras = []
        
        self.surfText1 = None
        self.setText1("")
        
    def appendCamera(self, cam):
        self.cameras.append(cam)
        
    def reconnaitre(self, cube):
        for cam in self.cameras:
            cam.reconnaitre(cube)
                        
    def refresh(self, nCam):
        image = self.cameras[nCam].getImgIHM()
        
        self.fenetre.blit(image, (0, 0))

        for bp in self.bp:
            self.fenetre.blit(bp.image, bp.rect)
            
        for bp in self.bp_mvt:
            self.fenetre.blit(bp.image, bp.rect)

        for pm in self.cameras[nCam]:
            self.fenetre.blit(pm.image, pm.rect)
        
        self.iMiniCube.refresh(self.cameras[nCam])
        self.fenetre.blit(self.iMiniCube.image, self.iMiniCube.rect)
        
        self.fenetre.blit(self.surfText1, pygame.Rect(XZONETXT1, YZONETXT1, WZONETXT1, HZONETXT1))
        
        pygame.display.flip()
        
    def waitClick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                #print(pygame.mouse.get_pos())
                pass

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:   #Si clic gauche ou droit
                    # détection des clicks sur le mini cube
                    caseClick = self.iMiniCube.isCollide(event.pos)
                    if caseClick is not None:
                        return Click(CKCUBE, caseClick)
                    # détection des clicks sur les boutons
                    for i in range(len(self.bp)):
                        if self.bp[i].isCollide(event.pos):
                            return Click(CKBOUTON, i)
                    # détection des clicks sur les boutons de mouvements
                    for i in range(len(self.bp_mvt)):
                        if self.bp_mvt[i].isCollide(event.pos):
                            return Click(CKBOUTON, len(self.bp) + i)
                    return Click(CKPOSITION, event.pos)

    def setText1(self, texte):
        self.surfText1 = pygame.Surface((WZONETXT1, HZONETXT1), pygame.SRCALPHA)
        #self.surfText1.fill(pygame.Color('#BB3F3F'))
        police = pygame.font.SysFont("Arial Black", 28)

        lstTxt = texte.split('\n')
      
        topTxt = 0
        for t in lstTxt:
            txt = police.render(t, True, COLORTXT1)
            rectTexte = txt.get_rect()
            rectTexte.top = topTxt
            topTxt += 30
            self.surfText1.blit(txt, rectTexte)
            
class PointMesure(object):
    def __init__(self, w, numCase):
        # taille du carré de mesure en pixel
        self.w = w
        # n est le numéro de la case

        self.image = pygame.Surface((self.w, self.w))
        self.image.fill(COLORPMN)
        self.rect = self.image.get_rect()
        
        self.num = numCase
        self.focused = False
    
    def setFocus(self):
        self.focused = True
        self.image.fill(COLORPMY)
        
    def resetFocus(self):
        self.focused = False
        self.image.fill(COLORPMN)        
        
    def getCenter(self):
        return (self.rect.left + self.w //2, self.rect.top + self.w //2)
    
    def setCenter(self, pos):
        x, y = pos
        self.rect.left = x - self.w //2
        self.rect.top = y - self.w //2
        
    def getZone(self):
        x, y = self.rect.left, self.rect.top
        return (x, y, x + self.w, y + self.w)
    
    def getColorAverage(self, im):
        imC = im.crop(self.getZone())
        
        # calcul de la couleur moyenne du carré de mesure m * m
        r, v, b = 0, 0, 0
        for x in range(self.w):
            for y in range(self.w):
                px = imC.getpixel((x, y))
                r += px[0]
                v += px[1]
                b += px[2]

        # nb de pixels
        n = self.w ** 2
        
        return (r // n, v // n, b // n)         
        
    def __repr__(self):
        return str(self.numCase) + ' -> ' + str(self.getCenter())
         
class Camera(object):
    # la collection de voisin
    dicoCouleur = {c : [] for c in 'FRUBLD' }    
    
    def __init__(self, n, multi):
        self.n = n
        self.multi = multi
        #le nom de la caméra
        self.name = 'ABCD'[n]
        # la liste des points de mesure
        self._pointsMesure = []
        
        self.y1cut = 25
        self.y2cut = 75
        self.x2cut = 0
        
        #### POUR DEBUGG en attendant les caméras
#         self.nTest = 0
#         self.cmpt = 2 # num fichier image, pour debugg, a supprimer !!
#         self.imgTest = [('im0.png', Cube('xxxxUxxxxUFDLxLBBUDDFFxUFURDFDBxDUUBxxxxLxxxxxxxxBxxxx')),
#                         ('im1.png', Cube('xxxxUxxxxBUDRxBFFUFBRLxBRDRDRUDxRDLLxxxxLxxxxxxxxBxxxx')),
#                         ('im2.png', Cube('xxxxUxxxxUFDFxBBRUFLBRxLRUDDFLBxDRLLxxxxLxxxxxxxxBxxxx')),
#                         ('im3.png', Cube('xxxxUxxxxRBBFxUDRUDLUFxRRBRFRFBxDBLLxxxxLxxxxxxxxBxxxx')),
#                         ('im4.png', Cube('xxxxUxxxxRLFDxBRBRDDDLxRLRUUFFBxRDUBxxxxLxxxxxxxxBxxxx')),
#                         ('im5.png', Cube('xxxxUxxxxRFDBxLRRUBBFLxRLDFURDUxFBBRxxxxLxxxxxxxxBxxxx')),
#                         ('im6.png', Cube('xxxxUxxxxFFDUxDRUFUBDUxFBDDUBBLxLDFUxxxxLxxxxxxxxBxxxx')),
#                         ('im7.png', Cube('xxxxUxxxxUFDLxLBBUDDFFxUFURDFDBxDUUBxxxxLxxxxxxxxBxxxx')),
#                         ('im8.png', Cube('xxxxUxxxxDLRUxLFFRFRLBxLRRUBULUxLLDFxxxxLxxxxxxxxBxxxx')),
#                         ('im9.png', Cube('xxxxUxxxxLLRDxBLFDDBUFxRUFBBLDLxUFRRxxxxLxxxxxxxxBxxxx'))]
        
    def getPointsMesure(self, n):
        for p in self._pointsMesure:
            if p.num == n:
                return p
            
    def removePM(self, pm):
        self._pointsMesure.remove(pm)
            
    def ajoutePM(self, pm):
        self._pointsMesure.append(pm)
        
    def clearPM(self):
        self._pointsMesure = []

    def __iter__(self):
        self.num = -1
        return self

    def __next__(self):
        if (self.num >= self.__len__() - 1):
            raise StopIteration
        self.num += 1
        return self._pointsMesure[self.num]
    
    def __getitem__(self, k):
        return self._pointsMesure[k]
    
    def __len__(self):
        return len(self._pointsMesure)
        
    def getImgPILL(self):
        #image = Image.open(os.path.join(pathname, "Images_test", "img_2592x1944.jpg"))
        image = self.multi.getPillImage(self.name)
        
        # calcul l'echelle a appliquer pour que ce que l'on veut afficher occupe tout l'écran
        hImg = (self.y2cut - self.y1cut) * HCAMERA / 100
        rapXY = HSCREEN / hImg
        # applique ce recadrage
        WimgRecad = int(WCAMERA * rapXY)
        HimgRecad = int(HCAMERA * rapXY)
        image = image.resize((WimgRecad, HimgRecad), resample = 0) 
        # Découpe l'image a la taille de l'écran
        if WimgRecad <= WSCREEN:
            # l'image restante n'est pas assez large, on la recolle sur une de la bonne largeur
            img = image.copy()
            image = Image.new('RGB', (WSCREEN, int(HCAMERA * rapXY)))
            image.paste(img, (int((WSCREEN - WimgRecad) / 2), 0))
            #on coupe les bords gauche et droite si besoin
            image = image.crop((0, int(HimgRecad * self.y1cut / 100), WSCREEN, int(HimgRecad * self.y2cut / 100)))
        else:
            # calcul du point x2 sur l'image recadrée
            x2 = (WimgRecad * self.x2cut) // 100 - int((WimgRecad - WSCREEN) / 2)

            # calcul du delta eventuel
            if x2 > XBP2:
                delta = x2 - XBP2
            else:
                delta = 0
            # on coupe ce qui dépasse
            
            image = image.crop((int((WimgRecad - WSCREEN) / 2) + delta, int(HimgRecad * self.y1cut / 100), int((WimgRecad + WSCREEN) / 2) + delta, int(HimgRecad * self.y2cut / 100)))
        
        return image

    def getImgIHM(self):
        image = self.getImgPILL()
        # converion en objet Pygame
        mode = image.mode
        size = image.size
        data = image.tobytes()
        
        return pygame.image.fromstring(data, size, mode)

    def getImgIHM2(self):
        return pygame.image.load(os.path.join(pathname, "Images_test", self.imgTest[self.n][0])).convert()

#     def getImgPILL2(self):
#         self.cmpt += 1
#         print(F"im{self.cmpt}.png -> Camera N°{self.n}")
#         # ouverture et redimensionnement du fichier image
#         im = Image.open(os.path.join(pathname, "Images_test", self.imgTest[self.cmpt][0]))
#         # im = im.resize((1600, 900),Image.Resampling.LANCZOS)
#         # cube correspondant
#         # cube = self.imgTest[self.cmpt][1]
#         return im

    def apprentissage(self, cube):
        
        im = self.getImgPILL()
        # pour les tests, on prend un faux cube
#         cube = self.imgTest[self.cmpt][1]
        
        cubeTxt = repr(cube)
        
        # pour chaque point de mesure
        for pm in self._pointsMesure:
            if cubeTxt[pm.num] in 'FRUBLD':
                Camera.dicoCouleur[cubeTxt[pm.num]].append(pm.getColorAverage(im))
        #print(Camera.dicoCouleur)

    def reconnaitre(self, cube):
        # ouverture
        #im = Image.open(os.path.join(pathname, "Images_test", self.imgTest[self.nTest][0]))
        im = self.getImgPILL()
        #im = im.resize((1600, 900),Image.Resampling.LANCZOS)
        
        cubeLst = ['x'] * 54
        # pour chaque point de mesure
        for pm in self._pointsMesure:
            c = pm.getColorAverage(im)
            cubeLst[pm.num] = self.kVoisins(c)
        
        cube.str2cube("".join(cubeLst))
        
    def kVoisins(self, c):
        """
        Algo des knn.
        
        PARAMETERS
            c : tuple
                (R, V, B) couleur a comparer aux voisins
            
        RETURN
            str
                couleur probable sous forme d'une lettre
        """
        dicoDist = {c : float('inf') for c in 'FRUBLD'}

        for k in 'FRUBLD':
            # calcul la distance moyenne avec cette couleur
            if len(Camera.dicoCouleur[k]) != 0:
                d = 0
                for c2 in Camera.dicoCouleur[k]:
                    d += ((c[0] - c2[0]) ** 2 + (c[1] - c2[1]) ** 2 + (c[2] - c2[2]) ** 2) ** 0.5
                dicoDist[k] = d / len(Camera.dicoCouleur[k])

        #print(dicoDist)
        mini = min(dicoDist.values())
        for k in dicoDist:
            if dicoDist[k] == mini:
                return k

if __name__ == '__main__':
    from modeleCube import Face, Cube

    
    visio = IHMvisio()
#    
#     visio.appendCamera(Camera(0))
#     visio.appendCamera(Camera(1))
#     visio.appendCamera(Camera(2))
# 
#     visio.refresh(0)
# 
#     while True:
#         #if pygame.mouse.get_focused():
#         event = visio.waitClick()
#         if event is not None:
#             print(event)
# 
#     c = Cube()
#     c.reset()
# 
#     reco = Reconnaissance(3, c)
#     reco.parametrer()
        
#     imgTest = [("im0.png", ['DDFFxUFUR', 'UFDLxLBBU', 'DFDBXDUUB']),
#                         ("im1.png", ['FBRLxBRDR', 'BUDRxBFFU', 'DRUDxRDLL']),
#                         ("im2.png", ['FLBRxLRUD', 'UFDFxBBRU', 'DFLBxDRLL']),
#                         ("im3.png", ['DLUFxRRBR', 'RBBFxUDRU', 'FRFBxDBLL']),
#                         ("im4.png", ['DDDLxRLRU', 'RLFDxBRBR', 'UFFBxRDUB']),
#                         ("im5.png", ['BBFLxRLDF', 'RFDBxLRRU', 'URDUxFBBR']),
#                         ("im6.png", ['UBDUxFBDD', 'FFDUxDRUF', 'UBBLxLDFU']),
#                         ("im7.png", ['DDFFxUFUR', 'UFDLxLBBU', 'DFDBxDUUB']),
#                         ("im8.png", ['FRLBxLRRU', 'DLRUxLFFR', 'BULUxLLDF']),
#                         ("im9.png", ['DBUFxRUFB', 'LLRDxBLFD', 'BLDLxUFRR'])]
#     imgTest2 = []    
#     for u in imgTest:
#         txt = 'xxxxUxxxx' + u[1][1] + u[1][0] + u[1][2] + 'xxxxLxxxxxxxxBxxxx'
#         imgTest2.append((u[0], txt))
#     print(imgTest2)
    
        

        
