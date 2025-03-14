"""
Projet Robot resolveur de Rubik's Cube 2022

Classes pour l'IHM

version:
V1.0 : version de départ du projet.
V1.1 : replacement pour test classe face
V1.2 : Correction des classes pour y ajouter en attribut les instances du modele de cube
V1.3 :
V1.4 : intégration de la méthode animation et d'un attribut robot
V1.5 : Quelques modifs sur les couleurs pour régler des pb de compatibilité avec linux.
V1.6 : Intégration de la partie configuration caméra
V1.7 : Ajout d'une méthode setRobot, affichage de la confiance
"""

autor = 'Grégory COUTABLE'
version = '1.7'
date = '28/12/2024'


import pygame
from pygame.locals import *

import os
pathname = os.path.dirname(__file__)

#on va définir une série de constantes ici, pour alléger le programme
WSCREEN = 1600
HSCREEN = 900
#position et dimensions du cube
WCASE = 75
DCASE = 2 # espace entre deux cases de la même face
DFACE = 12 # espace entre deux faces
WFACE = (WCASE * 3 + DCASE * 2)
WCUBE = WFACE * 4 + DFACE * 3
HCUBE = WFACE * 3 + DFACE * 2
XCUBE = (WSCREEN - WCUBE) // 2
YCUBE = (HSCREEN - HCUBE) // 2

# dimensions du mini cube
WCASEMINI = 30
DFACEMINI = 6
DCUBEMINI = 20

WBP = 200
HBP = 60
YBP = 50
XBP = XCUBE + WCUBE + (XCUBE - WBP) // 2
DBP = 40

DEFAULTCOLORSCREEN = pygame.Color('#214761')#'#21618C'
ERRORCOLORSCREEN = pygame.Color('#D46262')
COLORBPR = pygame.Color('#BB3F3F') # #DFA5A5
COLORBPP = pygame.Color('#662222')
COLORBPD = pygame.Color('#AFAFAF')
COLORTXT = pygame.Color('#FFFFFF')
COLORTXT1 = pygame.Color('#DFA5A5') #
COLORTXT2 = pygame.Color('#FFFF00')
COLORTXT3 = pygame.Color('#000000')

WZONETXT1 = WFACE * 2 + DFACE * 2
HZONETXT1 = WFACE + DFACE
XZONETXT1 = XCUBE + WFACE * 2 + DFACE
YZONETXT1 = YCUBE + WFACE * 2 + DFACE

WZONETXT2 = WFACE * 2
HZONETXT2 = WFACE 
XZONETXT2 = 10
YZONETXT2 = 10

XCHRONO = 60
YCHRONO = 30

TEXTBP = ['RECONNAÎTRE', 'MÉLANGER', 'RÉSOUDRE', 'RESET', 'CLEAR', 'SUPER FLIP', "R L' D U' F B' R L'"]

CKCUBE = 0
CKBOUTON = 1
CKPOSITION = 2

class IHM (object):
    
    def __init__(self, cube, robot=None):
        #cube est une instance de la classe Cube
        pygame.init()
        
        self.fenetre = pygame.display.set_mode((WSCREEN, HSCREEN))#, FULLSCREEN)

        pygame.display.set_caption("Robot Rubik's Cube")
        
        self.robot = robot
        self.cube = cube
        self.iCube = ImgCube(WCASE, DFACE, XCUBE, YCUBE, cube)
        
        self.bp = [Bouton(WBP, HBP , TEXTBP[i]) for i in range(len(TEXTBP))]
        for i in range(len(self.bp)):
            self.bp[i].setRect(XBP, YBP + i * (HBP + DBP))
            
        self.surfText1 = None
        self.surfText2 = None
        self._blitText2("")
        
        self.enableChrono = False
        self.backgroundColor = DEFAULTCOLORSCREEN

        self.clearTxt()
        self.refresh()
    
    def setRobot(self, robot):
        self.robot = robot

    def clearTxt(self):
        self._blitText1("", "")
        self.enableChrono = False

    def setBackgroundColor(self, color):

        if color == 0:
            self.backgroundColor = ERRORCOLORSCREEN
        else:
            self.backgroundColor = DEFAULTCOLORSCREEN

    def _blitText1(self, titre, mvts):

        police = pygame.font.SysFont("Arial Black", 32)

        lstTxt = []
        lst = []
        idxSpace = 0
        
        while len(mvts) > 18:
            try:
                idxSpace = mvts.index(' ', 18)
            except:
                break
            lstTxt.append(police.render(mvts[:idxSpace], True, COLORTXT1))
            lst.append(mvts[:idxSpace])
            mvts = mvts[idxSpace + 1:]
            
        lstTxt.append(police.render(mvts, True, COLORTXT1))
        lst.append(mvts)
        
        #Une surface pour centrer le texte
        self.surfText1 = pygame.Surface((WZONETXT1, HZONETXT1), pygame.SRCALPHA)
        #self.surfText1.fill(COLORSCREEN)
        
        titre = police.render(titre, True, COLORTXT1)
        self.surfText1.blit(titre, (20, 10)) 

        #pour centrer le texte
        topTxt = 60
        for t in lstTxt:
            rectTexte = t.get_rect()
            rectTexte.center = self.surfText1.get_rect().center
            rectTexte.top = topTxt
            topTxt += 40
            self.surfText1.blit(t, rectTexte)
            
    def afficheMessage(self, texte):
        self._blitText2(texte)
        self.refresh()
        
    def _blitText2(self, texte):
        police = pygame.font.SysFont("Arial Black", 40)
        self.surfText2 = pygame.Surface((WZONETXT2, HZONETXT2), pygame.SRCALPHA)
        
        lstTxt = [police.render(t, True, COLORTXT) for t in texte.split('\n')]

        topTxt = 0
        for t in lstTxt:
            rectTexte = t.get_rect()
            rectTexte.top = topTxt
            topTxt += 30
            self.surfText2.blit(t, rectTexte)        
        
        
        
        
#         #Une surface pour centrer le texte
#         self.surfText2 = pygame.Surface((WZONETXT2, HZONETXT2), pygame.SRCALPHA)
#         #self.surfText2.fill(COLORSCREEN)
#         
#         texte = police.render(texte, True, COLORTXT)
#         self.surfText2.blit(texte, (40, 30)) 


    def refresh(self):
        
        self.fenetre.fill(self.backgroundColor)

        for bp in self.bp:
            self.fenetre.blit(bp.image, bp.rect)
        
        self.iCube.refresh()
        self.fenetre.blit(self.iCube.image, self.iCube.rect)

        if self.robot is not None and self.enableChrono:
            police = pygame.font.SysFont("Arial Black", 70)
            txt = str(round(self.robot.getChrono(), 2))
            while len(txt) < 4:
                txt += '0'
            txtChrono = police.render(txt + 's', True, COLORTXT2)
            self.fenetre.blit(txtChrono, (XCHRONO, YCHRONO))
        
        self.fenetre.blit(self.surfText1, pygame.Rect(XZONETXT1, YZONETXT1, WZONETXT1, HZONETXT1))
        self.fenetre.blit(self.surfText2, pygame.Rect(XZONETXT2, YZONETXT2, WZONETXT2, HZONETXT2))
        
        pygame.display.flip()
        
    def animation(self, seq, txt = None):
        
        if txt is not None:
            self._blitText1(txt, seq)
        else:
            self._blitText1('', '')

        #execution des mouvements par le robot et calcul du temps de l'animation
        tmov = self.robot.move(seq)
        t = tmov / (seq.count(' ')  + 1)
        #t = tmov / len(seq.split(' '))
        

        for m in seq.split(' '):
            self.cube.rotation(m)
            self.enableChrono = True
            self.refresh()
            # pour corriger le temps de l'animation
            tsup = 12
            pygame.time.Clock().tick(1 / t + tsup)
            
        while self.robot.busy:
            self.refresh()
            pygame.time.Clock().tick(30)
        
    def waitClick(self, nDiziemeSeconde = None):
        
        while nDiziemeSeconde is None or nDiziemeSeconde > 0:
            if nDiziemeSeconde is not None:
                nDiziemeSeconde -= 1
            
            pygame.time.Clock().tick(30)
        
            for event in pygame.event.get():    #Attente des événements
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        exit()
                    
                    if event.type == MOUSEBUTTONDOWN:
                        #self._blitText2(str(event.pos))
                        self.refresh()
                        print(str(event.pos))
                        if event.button == 1 or event.button == 3:   #Si clic gauche ou droit
                            for i in range(len(self.bp)):
                                if self.bp[i].isCollide(event.pos):
                                    return Click(CKBOUTON, i)                       
       
class Bouton(object):
    def __init__(self, w, h, nom):
        self.w = w
        self.h = h
        self.nom = nom.split('#') # si deux noms différents pour pressé#relaché le # sépare les noms
        self._pressed = False
        self._enable = True
        self.image = None
        self.setImg()
        self.rect = self.image.get_rect()

    def enable(self):
        self._enable = True
        self.setImg()
        
    def disable(self):
        self._enable = False
        self.setImg()

    def setImg(self):
        police = pygame.font.SysFont("Arial Black.ttf", 32)
        if not self._enable:
            clrCase = COLORBPD
            texte = police.render(self.nom[0], True, COLORTXT)
        elif self._pressed :
            clrCase = COLORBPP
            texte = police.render(self.nom[-1], True, COLORTXT)
        else :
            clrCase = COLORBPR
            texte = police.render(self.nom[0], True, COLORTXT)
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(clrCase)        
        rectTexte = texte.get_rect()
        rectTexte.center = self.image.get_rect().center
        self.image.blit(texte, rectTexte)        
    
    def setRect(self, left, top):
        self.rect.left = left
        self.rect.top = top
        
    def setName(self, nom):
        self.nom = nom
        self.setImg()
        
    def presser(self):
        self._pressed = True
        self.setImg()

    def relacher(self):
        self._pressed = False
        self.setImg()
        
    def isCollide(self, pos):
        return self._enable and self.rect.collidepoint(pos)

class ImgFace(object):
    def __init__(self, wCase, x, y, face):
        self.x = x
        self.y = y
        # face = instance de la classe face
        self.face = face
        
        self.WCASE = wCase
        self.DCASE = DCASE # espace entre deux cases de la même face
        
        self.image = pygame.Surface((3 * self.WCASE + 2 * self.DCASE, 3 * self.WCASE + 2 * self.DCASE))
        self.image.fill(DEFAULTCOLORSCREEN)
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y
        
        self.casesRect = [None for i in range(9)]

        self.colors = {"F":'#FF0000', "B":'#FF6800', "D":'#FFFF00', "R":'#0000FF', "L":'#00FF00', 'U':'#FFFFFF', 'x':'#7F7F7F'}
        self.imgCoche = pygame.transform.scale(pygame.image.load(os.path.join(pathname, "src", "coche.png")).convert_alpha(), (self.WCASE, self.WCASE))
        self.imgCroix = pygame.transform.scale(pygame.image.load(os.path.join(pathname, "src", "croix.png")).convert_alpha(), (self.WCASE, self.WCASE))
        
        self.refresh()
        
    def refresh(self, cam=None, aff_conf=False):            
        for x in range (3):
            for y in range (3):
                imgCase = pygame.Surface((self.WCASE , self.WCASE))
                imgCase.fill(pygame.Color(self.colors[self.face.getPiece(x, y)]))
                self.casesRect[y * 3 + x] = imgCase.get_rect()
                self.casesRect[y * 3 + x].left = x * (self.WCASE + self.DCASE)
                self.casesRect[y * 3 + x].top = y * (self.WCASE + self.DCASE)
                if cam is not None:
                    numCase = 'URFDLB'.index(self.face.name) * 9 + y * 3 + x
                    pm = cam.getPointsMesure(numCase)
                    if pm is not None:
                        if aff_conf:
                            police = pygame.font.SysFont("Arial Black.ttf", 24)
                            if self.face.getPiece(x, y) == 'R':
                                texte = police.render(str(self.face.getConf(x, y)), True, COLORTXT)
                            else:
                                texte = police.render(str(self.face.getConf(x, y)), True, COLORTXT3)
                            rectTexte = texte.get_rect()
                            rectTexte.center = imgCase.get_rect().center
                            imgCase.blit(texte, rectTexte)
                        elif pm.focused:
                            imgCase.blit(self.imgCoche, (0, 0))
                        else:
                            imgCase.blit(self.imgCroix, (0, 0))
                self.image.blit(imgCase, self.casesRect[y * 3 + x])

    def isCollide(self, pos):
        for i in range(9):
            if self.casesRect[i].collidepoint((pos[0] - self.x, pos[1] - self.y)):
                return 'URFDLB'.index(self.face.name) * 9 + i    # self.face.name, i
        return None

class ImgCube:
    def __init__(self, wCase, dFace, x, y, cube):
        self.x = x
        self.y = y
        # cube = instance de la classe Cube
        self.cube = cube
        
        self.WCASE = wCase
        self.DCASE = DCASE # espace entre deux cases de la même face
        self.DFACE = dFace # espace entre deux faces

        #taille d'une unité face
        u = 3 * self.WCASE + 2 * self.DCASE + self.DFACE
        #liste des positions des pièces dans le dessin selon leur nom
        positionFaces = {"F":(u, u), "B":(3 * u, u), "D":(u, 2 * u), "R":(2 * u, u), "L":(0, u), 'U':(u, 0)}
        #la liste des instances d'image de face
        # Attention, c'est chaud a suivre :
        # self.cube -> instance de la classe Cube
        # self.cube.cube -> dictionnaire des faces d'un Cube
        # self.cube.cube[f] -> une des 6 faces du Cube, instance de la classe Face
        self.iFaces = [ImgFace(wCase, positionFaces[f][0], positionFaces[f][1], self.cube.cube[f]) for f in self.cube.cube]

        self.image = pygame.Surface((12 * self.WCASE + 8 * self.DCASE + 3 * self.DFACE, 9 * self.WCASE + 6 * self.DCASE + 2 * self.DFACE), pygame.SRCALPHA)
        #self.image.fill(COLORSCREEN) 
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.refresh()
        
    def refresh(self, cam=None, aff_conf=False):

        for iFace in self.iFaces:
            iFace.refresh(cam, aff_conf)
            self.image.blit(iFace.image, iFace.rect)    


    def isCollide(self, pos):
        
        for f in self.iFaces:
            caseClick = f.isCollide((pos[0] - self.x, pos[1] - self.y))
            if caseClick is not None:
                return caseClick
        return None
         
class Click(object):
    def __init__(self, t, contenu):
        self.type = t
        self.contenu = contenu
        self.txt = ('CUBE', 'BOUTON', 'POSITION')
        
    def __repr__(self):
        return self.txt[self.type] + ' -> ' + str(self.contenu)

if __name__ == '__main__':
    from modeleCube import Face, Cube
    from robotCube import Robot
    #Un cube pour l'exemple
    c = Cube()
    c.str2cube('UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB')

    #une fenetre pygame pour dessiner dedant
#    fenetre = pygame.display.set_mode((WSCREEN, HSCREEN))
#    pygame.display.set_caption("Robot Rubik's cube")
    
    # pour dessiner une face, on créé un objet Imgface en lui associant un face (instance de Face) et en indiquant sa position
    
#     iface1 = ImgFace(100, 100, c.cube['F'])
#     iface2 = ImgFace(100, 400, c.cube['U'])
# 
#     fenetre.blit(iface1.image, iface1.rect)
#     fenetre.blit(iface2.image, iface2.rect)
#     
#     icube = ImgCube(500, 50, c)
#     fenetre.blit(icube.image, icube.rect)
#     
#     
#     pygame.display.flip()
    
    ihm = IHM(c)
#     r = Robot()
#     ihm.robot = r
    
#     m = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
#     #print(r.move(m))
#     ihm.enableChrono = True
#     while r.busy:
#         ihm.refresh()

            
#             event = ihm.waitClick()
#             print(event)
        


        