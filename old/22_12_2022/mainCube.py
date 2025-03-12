autor = 'Grégory COUTABLE'
version = '1.1'
date = '15/12/2022'


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
        # un robot
        self.robot = robotCube.Robot()
        # le GUI accede aussi au robot
        self.gui.robot = self.robot 
        
    def run(self):
        while True:
            event = self.gui.waitClick()
            
            if event[:2] == 'BP':
                
                self.gui.clearTxt()
                
                k = int(event[2])
                print(k, ihmCube.TEXTBP[k])
                
                # RECONNAÎTRE
                if k == 0:
                    pass
                
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
