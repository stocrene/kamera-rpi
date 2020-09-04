# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:01:07 2020

@author: Rem
"""

import time 
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

m1_pin = 4  #gelb
m2_pin = 17 #grün
m3_pin = 23 #blau
m4_pin = 24 #violett

anzahlSchritte = 8
schritte_pro_drehung = 512
grad_pro_schritt = 360.0/schritte_pro_drehung

stufe1 = 0.005
stufe2 = 0.001



schritt = list(range(0, anzahlSchritte))
schritt[0] = [0,0,0,1]
schritt[1] = [0,0,1,1]
schritt[2] = [0,0,1,0]
schritt[3] = [0,1,1,0]
schritt[4] = [0,1,0,0]
schritt[5] = [1,1,0,0]
schritt[6] = [1,0,0,0]
schritt[7] = [1,0,0,1]


GPIO.setup(m1_pin, GPIO.OUT)
GPIO.setup(m2_pin, GPIO.OUT)
GPIO.setup(m3_pin, GPIO.OUT)
GPIO.setup(m4_pin, GPIO.OUT)



def macheSchritt(m1, m2, m3, m4):
    GPIO.output(m1_pin, m1)
    GPIO.output(m2_pin, m2)
    GPIO.output(m3_pin, m3)
    GPIO.output(m4_pin, m4)


def drehungSchritte(schritte, richtung, geschwindigkeit):
    if geschwindigkeit == 1:
        pause = stufe1 
    else:
        pause = stufe2
    if(richtung == 'links'):
        for i in range(schritte):
            for j in range(anzahlSchritte):
                macheSchritt(schritt[j][0], schritt[j][1], schritt[j][2], schritt[j][3])
                time.sleep(pause)
    else:
        for i in range(schritte):
            for j in reversed(range(anzahlSchritte)):
                macheSchritt(schritt[j][0], schritt[j][1], schritt[j][2], schritt[j][3])
                time.sleep(pause)
    macheSchritt(0,0,0,0)
    
    
def drehungGrad(grad, richtung, geschwindigkeit):
    schritte = int(grad/grad_pro_schritt)
    drehungSchritte(schritte, richtung, geschwindigkeit)
 
 
"""
Argument 1: g (Grad)  oder   s (Schritte)
Argument 2: Grad      oder   Anzahl Schritte
Argument 3: links     oder   rechts
Argument 4: 1         oder   2   (Zwei Geschwindigkeitsstufen)
Beispiel Konsolenaufruf: python Schrittmotor.py g 90 links 2
"""

if __name__ == "__main__":  
    if len(sys.argv) != 5:
        print("Es müssen vier Argumente angegeben werden")
    else:
	    richtung = sys.argv[3]
        geschwindigkeit = int(sys.argv[4])
        if sys.argv[1] == 'g':
            grad = int(sys.argv[2])
            drehungGrad(grad, richtung, geschwindigkeit)
        elif sys.argv[1] == 's':
            schritte = int(sys.argv[2])
            drehungSchritte(schritte, richtung, geschwindikeit)
    
    

    # int __Position = 0
    # def __init__(self, schritte, richtung, geschwindigkeit):
        # self.__m1 = m1
        # self.__m2 = m2
        # self.__m3 = m3
        # self.__m4 = m4
        # self.__geschwindigkeit = geschwindigkeit
    
    # def get_Pos(self):
        # return __Position
    
    # def __Schritt1(self):
        # GPIO.output(self.__m4, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m4, False)
        
    # def __Schritt2(self):
        # GPIO.output(self.__m4, True)
        # GPIO.output(self.__m3, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m4, False)
        # GPIO.output(self.__m3, False)
        
    # def __Schritt3(self):
        # GPIO.output(self.__m3, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m3, False)
        
    # def __Schritt4(self):
        # GPIO.output(self.__m2, True)
        # GPIO.output(self.__m3, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m2, False)
        # GPIO.output(self.__m3, False)
         
    # def __Schritt5(self):
        # GPIO.output(self.__m2, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m2, False)
        
    # def __Schritt6(self):
        # GPIO.output(self.__m2, True)
        # GPIO.output(self.__m1, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m2, False)
        # GPIO.output(self.__m1, False)
              
    # def __Schritt7(self):
        # GPIO.output(self.__m1, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m1, False)
        
    # def __Schritt8(self):
        # GPIO.output(self.__m4, True)
        # GPIO.output(self.__m1, True)
        # sleep (self.__geschwindigkeit)
        # GPIO.output(self.__m4, False)
        # GPIO.output(self.__m1, False)
        
        
    # def __Linkslauf(self):
        # __Schritt1();
        # __Schritt2();
        # __Schritt3();
        # __Schritt4();
        # __Schritt5();
        # __Schritt6();
        # __Schritt7();
        # __Schritt8();
        
        # __Position = __Position - 8
        
    # def __Rechtslauf(self):
        # __Schritt8();
        # __Schritt7();
        # __Schritt6();
        # __Schritt5();
        # __Schritt4();
        # __Schritt3();
        # __Schritt2();
        # __Schritt1();
        # __Position = __Position + 8
        
    # def Drehung_Grad(self, int grad):
        # float anzahl;
        # if grad > 0:
            # anzahl = grad/(360.0/512.0)
            # for x in range(anzahl):
            # __Rechtslauf()
        # else:
            # anzahl = grad/(360.0/512.0)*(-1.0)
            # for x in range(anzahl):
            # __Linkslauf()
        
        
        