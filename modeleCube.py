"""
Version V1.5

Projet Robot resolveur de Rubik's Cube 2022

Classes pour la modélisation d'un rubik's cube

version:
V1.0 : version de départ du projet. Cette version contient juste les structures de données
        minimale et les quelques méthodes de représentation en console d'une face et d'un cube.

V1.1 : + methodes Cube.rotations
V1.2 : + methodes Cube.melange  (random)
V1.3 : + methodes evalSolutions
V1.4 : + methodes Cube.resoudreKociemba + Cube.resoudreTwoPhase + test1 (timer) + test2 (graphique du nombre de mouvement)
V1.5 : la conversion en chaine pour le robot est intégrée ... au robot
V1.6 : un attribut confiance est ajouté a chaque case du cube, ajout d'une méthode setPiece pour modifier une case du cube
"""

autor = 'Grégory COUTABLE'
version = '1.6'
date = '28/12/2024'

from timeit import timeit
import random
import time
from itertools import product

#importation des solveurs
# pip install kociemba
#import kociemba
# pip install RubikTwoPhase
#import twophase.solver  as sv

#bibliotheque pour les graphique
#import numpy as np
#import matplotlib.pyplot as plt

class Face:
    """
    Classe permettant de modéliser une face du cube.
    Reçoit  1 à 3 paramètres :
    - f (str): le nom de la face, 1 caractère parmi FRLBDU, c'est la couleur du centre.
    - full (bool) : optionnel, si True toutes les pièces seront identiques au centre.
                    si False, toutes les pièces vide ('x') sauf le centre.
    - strFace (str) : optionel, une chaine de 9 caractères parmi FRLBDU qui représente
                    la face complète. Par exemple 'UUUUUUUUU' pour la face U complète,
                    'FRUDUBLDF' exemple de face U mélangée.
                    
    Attributs publiques:
    - name (str) : une lettre pour le nom de la face parmi FRLBDU.
    - face (list) : une liste contenant 3 listes contenant les trois couleurs de chaque ligne.
    - conf (list) : une liste contenant 3 listes contenant les valeurs de confiance associées achaque case
    """
    def __init__(self, f, full = False, strFace = ''):
        self.name = f
        self.face = [['x' for i in range(3)] for j in range(3)]
        self.face[1][1] = self.name
        self.reset_conf()
        
        #couleur de la face opposée
        mvts = {'F':'B', 'B':'F', 'R':'L', 'L':'R', 'U':'D', 'D':'U'}
        self.nameOpp = mvts[f]
       
        if full:
            self.reset()
        elif isinstance(strFace, str) and len(strFace) == 9:
            self.str2face(strFace)
            
    def reset_conf(self):
        # L'attribut conf permet de stocker la confiance que l'on attribue a la couleur donnée a la pièce
        # permet de choisir entre plusieurs valeurs lors de la reconnaissance
        # attention cet attribut n'a de valeur qu'en statique, il est réinitialisé a 0 a chaque mouvement du cube.
        self.conf = [[0 for i in range(3)] for j in range(3)]

    def str2face(self, strFace):
        """
        Convertit le str reçu en argument en liste de liste. Par exemple 'FRUBLDLFU'.
        Modifie l'attribut publique face.
        """
        for j in range(3):
            for i in range(3):
                if strFace[3*j + i] in 'FRUBLD':
                    self.face[j][i] = strFace[3*j + i]
        # au cas où, on remet le centre
        self.face[1][1] = self.name
        self.reset_conf()

    def setPiece(self, num, couleur, conf=0):
        if couleur in 'FRUBLD' and conf >= self.conf[num // 3][num % 3]:
            self.face[num // 3][num % 3] = couleur
            self.conf[num // 3][num % 3] = conf
            
    def getPiece(self, x, y):
        return self.face[y][x]
    
    def getConf(self, x, y):
        return self.conf[y][x]

    def __repr__(self):
        """
        retourne une chaine de 9 caractères représentant la face en partant du haut à gauche
        jusqu'au bas à droite. Exemple, pour une face :
        
        F R U
        B L D
        L F U
        
        retourne 'FRUBLDLFU'
         """
        txt = ''
        for ligne in self.face:
            for p in ligne:
                txt += str(p)
        return txt
        
    def __str__(self):
        """
        retourne une chaine représentant la face sur 3 lignes de texte.
        Exemple, pour une face :
        
        F R U
        B L D
        L F U
        
        retourne 'F R U\nB L D\nL F U'
         """        
        txt = ''
        for ligne in self.face:
            for p in ligne:
                txt += str(p) + ' '
            txt += '\n'
        return txt
    
    def reset(self):
        """
        Fixe toutes les pièces de la face à la même couleur que le centre.
        """
        self.face = [[self.name for i in range(3)] for j in range(3)]
        self.reset_conf()

    def clear(self):
        """
        Efface toutes les pièces de la face sauf le centre.
        """
        self.face = [['x' for i in range(3)] for j in range(3)]
        self.face[1][1] = self.name
        self.reset_conf()

    def getEdge(self, card):
        """
        Méthode qui renvoie une arrête de la face.
        Reçoit 1 argument :
        card (str) : cardinal de l'arrete demandée, 1 caractère parmi WNES, pour
                    ouest, nord, est, et sud.
        renvoi une liste de 3 éléments.
        Par exemple pour un cube :
        
        F R U
        B L D
        L F R
        
        getEdge('W') retourne ['F', 'B', 'L']
        getEdge('N') retourne ['U', 'R', 'F']
        getEdge('E') retourne ['R', 'D', 'U']
        getEdge('S') retourne ['L', 'F', 'R']
        """
        if card == 'W':
            return [self.face[0][0], self.face[1][0], self.face[2][0]]
        elif card == 'N':
            e = self.face[0].copy()
            e.reverse()
            return e
        elif card == 'E':
            return [self.face[2][2], self.face[1][2], self.face[0][2]]
        elif card == 'S':
            return self.face[2].copy()
        
    def setEdge(self, ligne, card):
        """
        Méthode qui modifie une arrête de la face. Modifie l'attribut publique face
        Reçoit 2 argument :
        card (str) : cardinal de l'arrete visée, 1 caractère parmi WNES, pour
                    ouest, nord, est, et sud.
        ligne (liste) : Une liste des 3 couleurs de l'arrête a modifier.
        renvoi None.
        
        Par exemple, pour une face U initialisée (toutes les pièces U) avant
        chaque exécution de la méthode :
        
        setEdge(['F', 'R', 'D'], 'W') transforme le cube comme ceci :
        
        F U U 
        R U U 
        D U U

        setEdge(['F', 'R', 'D'], 'N') transforme le cube comme ceci :
        
        D R F 
        U U U 
        U U U 

        setEdge(['F', 'R', 'D'], 'E') transforme le cube comme ceci :
        
        U U D 
        U U R 
        U U F 
        
        setEdge(['F', 'R', 'D'], 'S') transforme le cube comme ceci :
        
        U U U 
        U U U 
        F R D
        
        """
        if card == 'W':
            self.face[0][0] = ligne[0]
            self.face[1][0] = ligne[1]
            self.face[2][0] = ligne[2]
        elif card == 'N':
            e = ligne.copy()
            e.reverse()
            self.face[0] = e
            return e
        elif card == 'E':
            self.face[2][2] = ligne[0]
            self.face[1][2] = ligne[1]
            self.face[0][2] = ligne[2]
        elif card == 'S':
            self.face[2] = ligne.copy()
        self.reset_conf()
            
    def rotation(self):
        """
        Fait tourner la face d'un quart de tour dans le sens horaire.
        Modifie l'attribut face.
        """
        self.face[0][0], self.face[0][1], self.face[0][2],\
                         self.face[1][2], self.face[2][2],\
                         self.face[2][1], self.face[2][0], self.face[1][0] = self.face[2][0],\
                         self.face[1][0], self.face[0][0],\
                         self.face[0][1], self.face[0][2],\
                         self.face[1][2], self.face[2][2], self.face[2][1]
        self.reset_conf()

        

class Cube:
    """
    Classe permettant de modéliser un cube entier.
    Ne reçoit  aucun paramètre.
                   
    Attributs publiques:
    - cube (dic) : un dictionnaire contenant 6 clés de type str : 1 caractère parmi 'LFRBUD'
                    les valeurs correspondantes sont des objets de la classe Face.
    """
    def __init__(self, strCube = None):
        self.cube = {}
        #une constante
        self.faceName = 'LFRBUD'
        
        for n in self.faceName:
            self.cube[n] = Face(n)
            
        self.lstMvts = []
        
        if strCube is not None:
            self.str2cube(strCube)
            
    def setPiece(self, num, couleur, conf=0):
        self.cube['URFDLB'[num // 9]].setPiece(num % 9, couleur, conf)

    def str2cube(self, strCube):
        """
        Conversion d'une chaine reçu en paramètre, strCube (str), en cube.
        L'ordre des faces est URFDLB.
        Modifie l'attribut cube.
        Exemple :
        le str d'un cube complet :
        'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
        la chaine correspondant à un super flip :
        'UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB'
        """
        for i in range(6):
            strFace = strCube[9 * i: 9 * (i + 1)]
            self.cube['URFDLB'[i]].str2face(strFace)


    def __repr__(self):
        """
        Retourne un str représentant le cube sur une seule ligne sans espace.
        L'ordre des faces est URFDLB.
        Par exemple un cube en position initiale :
        'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
        un super flip
        'UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB'
        """
        txt = ''
        for f in 'URFDLB':
            for lgn in self.cube[f].face:
                for p in lgn:
                    txt += str(p)
        return txt


    def __str__(self):
        """
        Retourne un str représentant le cube sur plusieurs lignes comme un cube déplié.

        Par exemple un cube en position initiale :
        
                U U U 
                       #à coder
        #pour perdre du temps et montrer timeit
        a = 0
        for i in range(100000):
            a += a**3
        #return juste pour l'exemple
        return "U2 F U' D R U L D' R F' L D2 B' U' D L' D' R' U L' B R'"
                U U U
                U U U 
                U U U 

        L L L   F F F   R R R   B B B   
        L L L   F F F   R R R   B B B   
        L L L   F F F   R R R   B B B   

                D D D 
                D D D 
                D D D
        
        un super flip :
        
                U B U 
                L U R 
                U F U 

        L U L   F U F   R U R   B U B   
        B L F   L F R   F R B   R B L   
        L D L   F D F   R D R   B D B   

                D F D 
                L D R 
                D B D 
        """
        txt = '\n'
        for ligne in self.cube['U'].face:
            txt += ' ' * 8
            for p in ligne:
                txt += str(p) + ' '
            txt += '\n'
        txt += '\n'
        
        for i in range(3):
            for f in 'LFRB':
                for p in self.cube[f].face[i]:
                    txt += str(p) + ' '
                txt += '  '
            txt += '\n'
        txt += '\n'
            
        for ligne in self.cube['D'].face:
            txt += ' ' * 8
            for p in ligne:
                txt += str(p) + ' '
            txt += '\n'
        txt += '\n'
        
        return txt
    
    def reset(self):
        """
        reset le cube : cube en position initiale, résolu
        """
        
        for face in self.cube:
            self.cube[face].reset()
        
    def clear(self):
        """
        efface le cube : pièces inconnues ('x') sauf les centres
        """
        for face in self.cube:
            self.cube[face].clear()
            
    def isNotClear(self):
        return not 'x' in self.__repr__()

    def rotation(self, fDir):
        """
        Rotation d'une face du cube, entrainant automatiquement les arrêtes des faces adjacentes.
        Reçoit un paramètre :
        fDir (str) : une chaine de 1 ou deux caractères : par exemple "F", "F'" ou "F2"
                    pour la face F. Correspond respectivement à 1/4 de tour dans le sens horaire,
                    1/4 de tour dans le sens anti horaire, et 1/2 tour.
                    Applicable a chaque face soit 18 mouvements possibles.
        
        """
        if fDir == "":
            return
        
        self.lstMvts.append(fDir)
        
        f = fDir[0]
        
        if "'" in fDir:
            nbRotation=3
        elif "2" in fDir:
            nbRotation=2
        else :
            nbRotation=1
            
        for i in range (nbRotation):
            
            self.cube[f].rotation()
            
            if f=='F':
                ordre = 'LDRU'
                card = 'ENWS'
            if f=='R':
                ordre = 'FDBU'
                card = 'EEWE'
            if f=='B':
                ordre = 'RDLU'
                card = 'ESWN'
            if f=='L':
                ordre = 'BDFU'
                card = 'EWWW'
            if f=='U':
                ordre = 'LFRB'
                card = 'NNNN'
            if f=='D':
                ordre = 'LBRF'
                card = 'SSSS'
                
            edgeW = self.cube[ordre[0]].getEdge(card[0])
            
            self.cube[ordre[0]].setEdge(self.cube[ordre[1]].getEdge(card[1]), card[0])
            self.cube[ordre[1]].setEdge(self.cube[ordre[2]].getEdge(card[2]), card[1])
            self.cube[ordre[2]].setEdge(self.cube[ordre[3]].getEdge(card[3]), card[2])
            self.cube[ordre[3]].setEdge(edgeW, card[3])
        
    def rotations(self, lstfDir):
        """
        Applique une série de rotations. Reçoit un argument (str) contenant les mouvements
        séparés par des espaces. Par exemple, pour mettre le cube en super flip :
        "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
        """
        
        #print(lstfDir)
        listMouvement = lstfDir.split()
        for m in listMouvement:
            self.rotation(m)
            
    def melange(self, nb = 20):
        """
        Applique une série de rotations aléatoires. Reçoit un argument (int) optionnel
        pour fixer le nombre de mouvement demandés, par défaut 20.
        Les mouvements réalisés inclus les demi tours : 18 mouvements possibles.
        Retourne un str des mouvements réalisés sépars par des espaces.
        """
    
        mouveMelange=""
        coeficientMouve=["","2","'"]
        lastM = ""
        i = 0
        while i < nb:
            newM = random.choice(self.faceName)
            if newM != lastM:
                mouveMelange = mouveMelange + newM
                lastM = newM
                mouveMelange = mouveMelange + random.choice(coeficientMouve) + " "
                i += 1
        mouveMelange = mouveMelange[:-1]
        self.rotations(mouveMelange)
        return mouveMelange
        
        
    def resoudreKociemba(self):
        """
        Résouds le cube : renvoi la suite de mouvements a réaliser pour passer le position actuelle
        à la position initiale du cube.
        Les mouvements sont renvoyés sous forme d'une chaine (str) contenant les mouvements
        séparés par des espaces. Par exemple :
        "U2 F U' D R U L D' R F' L D2 B' U' D L' D' R' U L' B R'"
        
        Kociemba
        
        """
        resolution = kociemba.solve(self.__repr__())
        #self.rotations(resolution)
        return resolution
    
    
    def resoudreTwoPhase(self):
        """
        Résouds le cube : renvoi la suite de mouvements a réaliser pour passer le position actuelle
        à la position initiale du cube.
        Les mouvements sont renvoyés sous forme d'une chaine (str) contenant les mouvements
        séparés par des espaces. Par exemple :
        "U2 F U' D R U L D' R F' L D2 B' U' D L' D' R' U L' B R'"
        
        TwoPhase
        
        """
        if self.isNotClear():

            resolution = sv.solve(self.__repr__(), 1, 1)
            
            if resolution == '(0f)':
                return ""
            
            # permet d'adapter la notation de sv.solve :
            # ex : U1 F3 L1 B1 R1 F3 R2 U2 L1 D2 B1 U1 D3 F2 D1 R2 L2 U2 F2 B2 R2 (21f)
            # les 3 sont remplacés par ' et les 1 sont suprimés
            # le nombre de mouvement à la fin est également suprimé
        
            resolution = resolution.replace('3',"'")
            resolution = resolution.replace('1',"")
            resolution = resolution[:-5] #peut laisser un caractère : " " si il y a plus de 10 mouvements
            if resolution[len(resolution)-1] == " ":
                resolution = resolution[:-1] # enleve le dernier espace si il y a plus de 10 mouvements
            # self.rotations(resolution)
            return resolution
        else:
            return ""
   
def cmptMvtSeq(seq):
    if seq == "":
        return 0
    return seq.count(' ') + 1


def evalSolution(lstfDir):
    """
    Reçoit une liste de mouvements (str), retourne le nombre de cycle du robot, compté en quart de tour. Tient compte
    des mouvements réalisés simultanément par le robot.
    Exemple :
    >>> evalSolution("L R F B")
    2
    >>> evalSolution("L R F B2")
    3
    >>> evalSolution("L U F B")
    3
    >>> evalSolution("L2 B2")
    4
    >>> evalSolution("L2 R2")
    2
    """
    mvts = {'F':'B', 'B':'F', 'R':'L', 'L':'R', 'U':'D', 'D':'U'}
    
    nbMouvements=0
    lstMouvements = lstfDir.split(" ")
    i=0
    quantiteMove=len(lstMouvements)
    
    while (i<quantiteMove):
        
        if (quantiteMove==i+1):        # rajoute un caractère à la liste lorsque i+1 ne possede plus de caractère
            lstMouvements.append(" ")
            
        fi = lstMouvements[i][0]  # mouvement actuel
        fip1 = lstMouvements[i + 1][0] # mouvement suivent
        
        if mvts[fi] != fip1:
            if ("2" in lstMouvements[i]):
                nbMouvements += 2
            else :
                nbMouvements += 1
                
        elif ("2" in lstMouvements[i] or "2" in lstMouvements[i+1]):
            nbMouvements += 2
            i += 1
        
        else :
            nbMouvements += 1
            i += 1
        i+=1
    return nbMouvements



def test():    
    c.melange()
    return c.resoudreTwoPhase()
#n = 1000    
#print(test())
#print(timeit("test()", number = n, globals = globals()) / n)

if __name__ == '__main__':
#    c=Cube()
#    r=Robot()
#    r.tempsPas(650)
#    r.eclairage(8191)
    #r.mouvement("F R U B L D")
    #r.mouvement("F B' L R' U D' F B'")
#     for i in range (3):
#         r.mouvement(c.melange())
#         time.sleep(2)
#         m=c.resoudreTwoPhase()
#         print(timeit('r.mouvement(m)', number = 1, globals = globals()))
#         time.sleep(2)
    
#     for i in range (10) :
#         r.mouvement("F R2 B L R' F2 B L2 U' D L R2 B D' U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2 B L2 U' D L")
#         
#         time.sleep(3)
#         print(timeit('r.mouvement(c.melange())', number = 1, globals = globals()))
#         time.sleep(3)
#         m=c.resoudreTwoPhase()
#         print(timeit('r.mouvement(m)', number = 1, globals = globals()))
    #print(timeit(r.mouvement("U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"), number = 1, globals = globals()))
    
#     print(F)
#     print()
#     F.rotation()
#     print(F)
#     print(F.getEdge('W'))
#     print()
#     print(F.getEdge('N'))
#     print()
#     print(F.getEdge('E'))
#     print()
#     print(F.getEdge('S'))
#     print()
#     F.reset()
#     print(F)
#     
    c = Cube()
    
    #c.str2cube('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')
    c.cube['F'].setPiece(2, 'R')
    c.cube['D'].setPiece(8, 'U')
    print(c)
    
    # txt = ''
    # for i in range(54):
    #     txt += chr(i + 40)
    # print(txt)
    
    # c.str2cube(txt)
    
    # print(c)  
    # c.rotation('F')  
    # print(c.__repr__())
    
    
    # transformation = []
    # mvts = []
    
    # ind = ("", "'", "2")

    # for m in 'URFDLB':
    #     for i in range(3):
    #         c.rotation(m + ind[i])
    #         mvts.append(m + ind[i])
    #         lst = [i for i in range(54)]
    #         txt = c.__repr__()
            
    #         for i in range(54):
    #             if i not in (4, 13, 22, 31, 40, 49):
    #                 lst[i] = ord(txt[i]) - 40
    #         transformation.append(lst)
    # print(len(transformation))        
    # for u in transformation:
    #     print(u)
    
    #c.str2cube('LUBFRDLUBFRDLUBFRDLUBFRDLUBFRDLUBFRDLUBFRDLUBFRDLUBFRD')
#     print(c.__repr__())
#     print(c)
#     print(c.isG1())
#     
#     c.rotations("U2 B L2 R2 F U2 B D2 U2 R2 L2 F R2 L2 F")
#     print(c)
    
#     print(c.isG1())
#     c.rotations("U2 B L2 R2 F U2 B D2 U2 R2 L2 F R2 L2 F")
#     c.rotations("U'")
#     c.melange()
#     print(c)
#     print(c.isG1())
#     print(timeit("c.resoudrePerso()", number = 1, globals = globals()))
    
    
#     #c.rotation("U")
#     c.rotations("U R2 ")
#     
#     print(c)
#     c.str2cube('UBULURUFURURFRBRDRFUFLFRFDFDFDLDRDBDLULBLFLDLBUBRBLBDB')
#     F = Face('F', False, 'RDUBFLUBD')
#     c = Cube()

#     print(c.__repr__())
#     print(c)
#     c.rotation("F'")
#     print(c)

#     comment chronométrer l'exécution d'un bout de code
#     print(c.resoudre())
#     print(timeit("c.resoudre()", number = 1, globals = globals()))
    
#     print(evalSolution("U2 F B' D R U L D' R2 F' L2 R2 B' U' D L' D' R' U L' B R'"))
#     
#     import doctest   
#     doctest.testmod()  

    
#    print(transmition())
    
    
    
    
    
    
    
    
    
    
    
    