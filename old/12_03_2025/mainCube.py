autor = 'Grégory COUTABLE', '...', '...'
version = '1.3.0_projet'
date = '28/12/2024'

import time
from threading import Thread

import ihmCube
import modeleCube
import robotCube




class Main:
    """
    Application Robot Rubik's cube.
    aucun paramètre reçu, aucun attribut publique.
                    
    Méthodes :
    run : lance l'application
    """
    def __init__(self):
        # Un cube
        self.cube = modeleCube.Cube()
        # un GUI qui accède au cube
        self.gui = ihmCube.IHM(self.cube)
        self.aff_log(0)
        # un robot
        self.robot = robotCube.Robot()
        # le GUI accede aussi au robot
        self.gui.setRobot(self.robot)
        self.aff_log(1)        

    def aff_log(self, etape):
        if etape == 0:
            self.log = 'Initialisation :\nrobot '
            self.gui.afficheMessage(self.log)
            self.enable_point = True
            self.proc_point = Thread(target=self.aff_point)
            self.proc_point.start()            
        if etape >= 1:
            self.enable_point = False
            self.proc_point.join()            
            self.log += ' ok\nterminée !!'
            self.gui.afficheMessage(self.log)
            time.sleep(2)
            self.gui.afficheMessage("")        

    def aff_point(self):
        while self.enable_point:
            self.log += '.'
            self.gui.afficheMessage(self.log)
            time.sleep(0.5)

    def run(self):
        while True:
            event = self.gui.waitClick()
            
            if event.type == ihmCube.CKBOUTON:
                
                self.gui.clearTxt()
                
                k = event.contenu
                print(k, ihmCube.TEXTBP[k])
                
                # RECONNAÎTRE
                if k == 0:
                    self.cube.clear()
                    # TODO : ecrire une méthode
                
                # MÉLANGER
                elif k == 1:
                    seq = self.cube.melange()
                    self.gui.animation(seq, "Mélange :")
                
                # RÉSOUDRE
                elif k == 2:
                    seq = self.cube.resoudreTwoPhase()
                    nMvts = modeleCube.cmptMvtSeq(seq)
                    if nMvts > 0:
                        self.gui.animation(seq, F"Solution en {nMvts} mouvements :")
                    else:
                        self.gui.animation("", F"Pas de solution !")
                
                # RESET
                elif k == 3:
                    self.cube.reset()
                    
                #CLEAR    
                elif k == 4:
                    self.cube.clear()
                
                # SUPER FLIP
                elif k == 5:
                    self.gui.animation("U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2", "Séquence :")
                
                # R L' D U' F B' R L'
                elif k == 6:
                    self.gui.animation("R L' D U' F B' R L'", "Séquence :")

            self.gui.refresh()

if __name__ == "__main__":
    print("module ihmCube version :", ihmCube.version)
    print("module robotCube version :", robotCube.version)
    print("module modeleCube version :", modeleCube.version)

    appli = Main()
    appli.run()

