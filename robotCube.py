"""
Milane Hamidouche 
06/2022

V2.1 : Communication entre l'esp32 et le programme de résolution
        Classe Robot qui permet :

            - De trouver automatiquement le port de l'arduino sur le rasberry
            - De régler l'éclairage du robot
            - De régler le temps par pas
            - De transformer la trame de résolution pour l'arduino
            
        Chaque trames se termine avec un "$" et commence par une lettre différente pour chaque fonctions

Grégory Coutable
07/2022
V2.2 : gestion du busy sur un thread autonome. Connexion au robot totalement revue.
"""

autor = 'Grégory COUTABLE'
version = '2.2'
date = '15/12/2022'

#bibliotheque pour se connecter à l'arduino
import sys
import glob
import serial
import time
from threading import Thread

from timeit import timeit




class Robot:
    """
    Classe permettant de se connecter au robot, de gérer l'éclairage et de lui envoyer la liste des mouvements, etc ... Aucun paramètre reçu.
                   
    Attributs publiques:
    
        - busy : booléen qui indique si le robot est occupé
        - error : booléen qui indique qu'une erreur de communication a eu lieu. Cette erreur doit être acquittée en exécutant la méthode acquitError()

        
     
    """
    

    def __init__(self):
        
        # Objet de connexion Serial, mis a jour par la méthode _foundPorts
        self._serConnect = None
        self._foundPorts()
        
        # Lancement du thread de surveillance des réponses du robot
        self.busy = False
        self.error = False
        survOK = Thread(target = self._watchOK)
        survOK.start()
        
        self.tempsPas = 650
        self.tempsPause = 1700
        self.niveauLed = 100
        
        self.setParam()

        #des attributs pour le chronométrage
        self._memoTime = 0
        self._chronoValue = 0

    def setParam(self):
        #configuration du robot et test de communication
        self.setTempsPas(self.tempsPas)
        assert self.waitOK(5), 'Pas de communication avec le robot'
        self.setTempsPause(self.tempsPause)
        assert self.waitOK(5), 'Pas de communication avec le robot'
        self.setLed(self.niveauLed) # 8191
        assert self.waitOK(5), 'Pas de communication avec le robot'        

    def acquitError(self):
        self.error = False

    def _resetTime(self):
        """
        Méthode qui reinitialise l'instant de départ du chronomètre. Privée.
        """
        self._memoTime = time.time()
        
    def getChrono(self):
        """
        Méthode publique qui renvoi la valeur courante du chronomètre.
        """
        if self.busy:
            self._chronoValue = time.time() - self._memoTime
        return self._chronoValue

    def _foundPorts(self):        
        """
        Liste les ports disponibles sur lesquels quelque chose est connecté.
        Version uniquement linux
        Le robot sera le premier de ces ports.
        A améliorer par l'ajout d'un contrôle de la réponse du robot.
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(2, 256)]
            
        elif sys.platform.startswith('linux'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
            
        else:
            raise EnvironmentError('Unsupported platform')
        
        #print(ports)
        result = []
        for port in ports:
            try:
                #s = serial.Serial(port)
                self._serConnect = serial.Serial(port, 115200, timeout = 0.01)
                print(port)
                time.sleep(0.5)
                self._serConnect.write('M$'.encode())
                time.sleep(0.5)
                if self._getOK():
                    return
                self._serConnect.close()
            except (OSError, serial.SerialException):
                pass
            
        raise("Aucun port trouvé !")
   
    
    def setLed(self, value):
        """
        Fixe la consigne éclairage du robot. Value (int) doit être compris entre 0 et 8191, sinon, rien ne se passe.
        """
        self.niveauLed = value
        if self.niveauLed > 8191:
            self.niveauLed = 8191
        if self.niveauLed < 0:
            self.niveauLed = 0
        self.envoi(F"E{value}$")
        
    def envoi(self, txt):
        """
        Envoi le message txt (str) au robot.

        """

        self.busy = True
        self._serConnect.write(txt.encode())
        self._resetTime()
        #self._serConnect.flushInput()
        
    def waitOK(self, timeout):
        """
        Méthode qui attend la validation d'une instruction envoyée au robot. Elle teste busy jusqu'à son retour a False, et renvoi True.
        timeout(en seconde) permet de quitter sans réponse OK du robot en renvoyant False.
        """
        t = 0
        while self.busy:
            time.sleep(0.1)
            t += 0.1
            if t > timeout:
                return False
        return True

    def _watchOK(self):
        """
        Cette méthode privée est exécutée dans un thread séparé dès l'instanciation d'un Robot. Elle maintient la file de réception vide et attend les réponse OK du robot.
        Cette méthode gère la mise a False de l'attribut busy.
        Si le robot ne répond pas dans les 10 secondes, busy passe a False et l'attribut error passe a True. L'utilisateur a la charge de remettre error a False une fois l'erreur acquittée.
        """        
        while True:
            if self.busy and self._getOK() :
                self.busy = False
            elif self.busy and self.getChrono() > 10:
                self.busy = False
                self.error = True
            else:
                self._serConnect.flushInput()
                
    def _getOK(self):
        """
        Test si ok a été reçu sur la liaison série avec le robot. Renvoi un booléen.
        """
        
        rep = self._serConnect.readline().decode('utf8')
        if rep[:2] == "OK":
            return True
        return False
    
        
    def setTempsPas(self, value):
        """
        Fixe la tempo inter pas des MPP du robot. Value est un temps en micorsecondes.
        Après beaucoup d'essai, 650 semble être une bonne valeur.
        
        """
        self.tempsPas = value
        self.envoi(F"T{value}$")
        
        
    def setTempsPause(self, value):
        """
        Fixe la tempo inter mouvements du robot. Value est un temps en micorsecondes.
        Après beaucoup d'essai, 1700 semble être une bonne valeur.
        
        """
        self.tempsPause = value
        self.envoi(F"P{value}$")
        
    
    def move(self, mvtStr):
        """
        Cette méthode reçoit le paramètre mvtStr (str) contenant une suite de mouvements séparé par des espace. ex : 'F B D2'.
        La méthode crée sun nouvelle chaine a destination du robot en séparant les mouvements FRU des mouvements BLD et en optimisant les enchainements. La nouvelle chaine
        est de la forme :
        'M' + mouvements FRU + '#' + mouvements BLD + '$'
        Par exemple :
                        'F' donne 'Ma#x$'
                        'F B D2' donne 'Max#jr$'
                        'U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2' donne 'Mgfadxdixxdhfaexic#xxjxlxxmlxqxxmlxx$'
        
        Les x correspondent a une absence de mouvement (Les mouvements FRU et BLD doivent avoir le même nombre de lettres) et permettent la synchronisation FRU et BLD.
        
        Cette chaine est envoyée au robot, l'attribut busy est donc mis a True.
        
        La méthode estime le temps de fonctionnement du robot en seconde et renvoi cette valeur saous la forme d'un float.
        
        """
        
        if mvtStr == "":
            return -1
        
        # Dictionnaire des mouvements homologues
        mvts = {'F':'B', 'B':'F', 'R':'L', 'L':'R', 'U':'D', 'D':'U'}
        # dictionnaire des codes mouvements du robot : une lettre minuscule = 1 mouvement, il y en a 18 possibles.
        rename = {'F':'a', "F'":'b', 'F2':'c', 'R':'d', "R'":'e', 'R2':'f', 'U':'g', "U'":'h', 'U2':'i', 'B':'j', "B'":'k', 'B2':'l', 'L':'m', "L'":'n', 'L2':'o', 'D':'p', "D'":'q', 'D2':'r'}
        lstFRU = '' # liste des mouvement FRU
        lstBLD = '' # liste des mouvements BLD
        lstMouvements = mvtStr.split(" ")
        
        i = 0
        nMove = len(lstMouvements) # nombre de mouvement
        lstMouvements.append(" ") # rajoute un élément a la liste de mouvement, pour permettre de tester le suivant du dernier.
        while i < nMove :
            
            fi = lstMouvements[i][0]  # mouvement actuel
            fip1 = lstMouvements[i + 1][0] # mouvement suivant
            
            if mvts[fi] == fip1:
                if "2" in lstMouvements[i] :
                    if fi == "F" or fi == "R" or fi == "U" :
                        lstFRU = lstFRU + rename[fi] + rename[fi]
                        if "2" in lstMouvements[i + 1] :
                            lstBLD = lstBLD + rename[fip1] + rename[fip1]
                        else :
                            lstBLD = lstBLD + rename[lstMouvements[i + 1]] + "x"
                    else:
                        lstBLD = lstBLD + rename[fi] + rename[fi]
                        if ("2" in lstMouvements[i + 1]):
                            lstFRU = lstFRU + rename[fip1] + rename[fip1]
                        else :
                            lstFRU = lstFRU + rename[lstMouvements[i + 1]] + "x"                       
                        
                elif ("2" in lstMouvements[i + 1]):
                    if fi == "F" or fi == "R" or fi == "U":
                        lstFRU = lstFRU + rename[lstMouvements[i]] + "x"
                        lstBLD = lstBLD + rename[fip1] + rename[fip1]
                    else :
                        lstBLD = lstBLD + rename[lstMouvements[i]] + "x"
                        lstFRU = lstFRU + rename[fip1] + rename[fip1]                         
                         
                else :
                    if fi == "F" or fi == "R" or fi == "U":
                        lstFRU += rename[lstMouvements[i]]
                        lstBLD += rename[lstMouvements[i + 1]]
                    else : 
                        lstFRU += rename[lstMouvements[i + 1]]
                        lstBLD += rename[lstMouvements[i]]
                i += 1
            else :
                if fi=="F" or fi=="R" or fi=="U":
                    lstFRU+=rename[lstMouvements[i]]
                    lstBLD += "x"
                else : 
                    lstFRU += "x"
                    lstBLD += rename[lstMouvements[i]]
            i+=1
        
        # envoi au robot
        self.envoi('M' + lstFRU + '#' + lstBLD + "$")
        #print('M' + lstFRU + '#' + lstBLD + "$")
        
        # estimation du temps de résolution
        # le nombre de quart de tour
        nbQuart = len(lstFRU) + lstFRU.count('c') + lstFRU.count('f') + lstFRU.count('i')
        #renvoi une estimation du temps de manipulation du robot
        # * 1.1 -> correction empirique pour plus de réalisme
        return (self.tempsPas * 100 * nbQuart + (len(lstFRU) - 1) * self.tempsPause) * 1.13 / 1e6
    

if __name__ == "__main__":
    # test pour vieux robot !!
    r = Robot()
    r.setTempsPas(600) #800
    r.setTempsPause(1700) #2000
    
    while True:
        print(r.move("B2 F L2 U"))
        time.sleep(1)
    
#     m = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
#     print(r.move(m))
#     
#     while r.busy:
#         print (r.getChrono())
#         
#     r.move("F2 R2 U2 B2 L2 D2")


    

    
    