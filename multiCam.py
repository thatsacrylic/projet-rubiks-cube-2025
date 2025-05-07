"""
Projet Robot resolveur de Rubik's Cube 2022

Classe permettant l'interface avec la carte physique multicam de la société arducam.
Installation en suivant les explications :

https://www.arducam.com/product/multi-camera-v2-1-adapter-raspberry-pi/
https://github.com/ArduCAM/RaspberryPi/tree/master/Multi_Camera_Adapter/Multi_Adapter_Board_4Channel

bugs report :
- utiliser la commande sudo apt --fix-broken install (avant d'installer wiringpi pour résoudre le problème de dépendances avec libc6:armhf
- penser a activer le bus I2C

version:
V1.1 : opérationnelle, pour 4 caméras

"""

autor = 'Grégory COUTABLE'
version = '1.1'
date = '22/12/2022'

from picamera2 import Picamera2
import RPi.GPIO as gp
import time
import os
from threading import Thread, Lock
from PIL import Image

WIDTH = 2592
HEIGHT = 1944

class MultiCamera(object):
    
    adapterInfo = {  
        "A" : {   
            "i2c_cmd":"i2cset -y 10 0x70 0x00 0x04",
            "gpio_sta":[0, 0, 1],
        }, "B" : {
            "i2c_cmd":"i2cset -y 10 0x70 0x00 0x05",
            "gpio_sta":[1, 0, 1],
        }, "C" : {
            "i2c_cmd":"i2cset -y 10 0x70 0x00 0x06",
            "gpio_sta":[0, 1, 0],
        },"D" : {
            "i2c_cmd":"i2cset -y 10 0x70 0x00 0x07",
            "gpio_sta":[1, 1, 0],
        }
    }

    def __init__(self):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)
        self.picam2 = None
        
        self.imgPILL = {k: Image.new('RGB', (1600, 900)) for k in 'ABCD'}
        
        self._configure()
        
        self.verrou = Lock()
        
        self.proc = Thread(target = self._refreshImg)
        self.proc.start()
        
    def _refreshImg(self):
        while True:
            for item in 'ABCD':
                self._selectChannel(item)
                time.sleep(0.5)
                img = self.picam2.capture_image()
                self.verrou.acquire()
                self.imgPILL[item] = img
                self.verrou.release()
#                 print(item)

    def _selectChannel(self, index):
        channelInfo = MultiCamera.adapterInfo.get(index)
        gpioSta = channelInfo["gpio_sta"] # gpio write
        gp.output(7, gpioSta[0])
        gp.output(11, gpioSta[1])
        gp.output(12, gpioSta[2])

    def _initI2C(self, index):
        channel_info = MultiCamera.adapterInfo.get(index)
        os.system(channel_info["i2c_cmd"]) # i2c write

    def _configure(self):
        for item in 'ABCD':
            print(item)
            self._selectChannel(item)
            self._initI2C(item)
            time.sleep(0.5) 
            if self.picam2 is not None:
                self.picam2.close()
            print("init "+ item)
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_still_configuration(main={"size": (WIDTH, HEIGHT),"format": "BGR888"}, buffer_count=2)) 
            self.picam2.start()
            time.sleep(0.5)
            self.picam2.capture_array(wait = False)
            time.sleep(0.1)
    
    def getPillImage(self, item):
        """
        Renvoi une image PILLOW de la taille maxi pour la caméra utilisée.
        """
        self.verrou.acquire()
        img = self.imgPILL[item]
        self.verrou.release()        
        return img


if __name__ == "__main__":
    multi = MultiCamera()
    
    time.sleep(5)
    
    for item in 'ABCD':
        img = multi.getPillImage(item)
        img.show()