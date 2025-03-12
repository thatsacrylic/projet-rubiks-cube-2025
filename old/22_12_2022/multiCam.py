
from picamera2 import Picamera2
from PIL import Image
import RPi.GPIO as gp
import time
import os

WIDTH = 2592
HEIGHT = 1944

WSCREEN = 1600
HSCREEN = 900

Y1CUT = 400
Y2CUT = 1600
WCUT = WSCREEN * (Y2CUT - Y1CUT) / HSCREEN
X1CUT = (WIDTH - WCUT) // 2
X2CUT = (WIDTH + WCUT) // 2

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

    def select_channel(self, index):
        channelInfo = MultiCamera.adapterInfo.get(index)
        gpioSta = channelInfo["gpio_sta"] # gpio write
        gp.output(7, gpioSta[0])
        gp.output(11, gpioSta[1])
        gp.output(12, gpioSta[2])

    def init_i2c(self, index):
        channel_info = MultiCamera.adapterInfo.get(index)
        os.system(channel_info["i2c_cmd"]) # i2c write

    def configure(self):
        for item in ("A","B","C"):
            print(item)
            self.select_channel(item)
            self.init_i2c(item)
            time.sleep(0.5) 
            if self.picam2 is not None:
                self.picam2.close()
            print("init "+ item)
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_still_configuration(main={"size": (WIDTH, HEIGHT),"format": "BGR888"}, buffer_count=2)) 
            self.picam2.start()
            time.sleep(2)
            self.picam2.capture_array(wait = False)
            time.sleep(0.1)
        time.sleep(2)
            
    def givePillImage(self, item):
        
        self.select_channel(item)
        time.sleep(0.3)
        
        im = self.picam2.capture_image()
        imC = im.crop((X1CUT, Y1CUT, X2CUT, Y2CUT))
        print(imC.size)
        return imC
    


if __name__ == "__main__":
    multi = MultiCamera()
    multi.configure()
    
    img = multi.givePillImage('B')
    img.show()
#     for item in ("A","B","C"):
#         img = multi.givePillImage('A')
#         img.show()

