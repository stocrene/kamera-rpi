#Before Running you have to "sudo pigpiod"
#imports
import pigpio
import time

GPIO = pigpio.pi()
# obsolete GPIO.setmode(GPIO.BOARD)

class servomotor:
    pin_out = 0
    frequency = 0
    cycle = 60000
    
    def __init__(self, pin, freq):
        self.pin_out = pin
        self.frequency = freq

    def initialize(self):
        GPIO.set_mode(self.pin_out,pigpio.ALT5)
        GPIO.hardware_PWM(self.pin_out, self.frequency, self.cycle)

        #goto unglücklich gewählt 
    def goto(self, angle, speed): #goto angle with certain speed (deg/sec)
        endpos = (2 + angle/18)*10000
        if endpos > 120000:         #if endpos > max
            endpos = 120000
        if endpos < 20000:          #if endpos < min
            endpos = 20000
        increment = (speed/(50*18))*10000 #increment per 1/50 sec
        if self.cycle > endpos:
            increment = -increment
        print('endpos' + str(endpos) + 'cycle'+str(self.cycle)+'increment'+str(increment))
        while (not((self.cycle+1000 >= endpos) and (self.cycle-1000<=endpos))):
            #print("work")
            self.cycle += increment
            GPIO.hardware_PWM(self.pin_out, self.frequency, self.cycle)
            time.sleep(0.02)
        GPIO.hardware_PWM(self.pin_out, self.frequency, 0)
    
    def getpos(self):
        return (self.cycle/10000 - 2) * 18

    def clean(self):
        GPIO.write(self.pin_out, 0)
        GPIO.stop()
        print("class cleaned")


#initialize a servo class (12 for x-axis; 13 for y-axis)
s1 = servomotor(12, 50)
s1.initialize()

try:
    while True:
        angle = float(input('Enter angle between 0 & 180:'))
        speed = float(input('Enter angular speed in deg/sec:'))
        s1.goto(angle,speed)

finally:
    s1.clean()
    
