#Before Running you have to "sudo pigpiod"
#imports
import pigpio
import time

GPIO = pigpio.pi()
# obsolete GPIO.setmode(GPIO.BOARD)

# class servomotor
# used to control one servomotor
class servomotor:
    pin_out = 0
    frequency = 0
    cycle = 120000
    maximum = 0
    
    # create the motor
    def __init__(self, pin, freq, maxi):
        self.pin_out = pin
        self.frequency = freq
        self.maximum = (maxi/18+2)*10000
        if self.maximum > 120000:
            self.maximum = 120000
        elif self.maximum < 20000:
            self.maximum = 20000

    # initialize the PWM Controlling
    def initialize(self):
        print("initialize" + str(self.pin_out))
        GPIO.set_mode(self.pin_out,pigpio.ALT5)
        GPIO.hardware_PWM(self.pin_out, self.frequency, self.cycle)
        time.sleep(0.2)
        GPIO.hardware_PWM(self.pin_out, self.frequency, 0)

    # go exactly one step with a certain angle
    def goOneStep(self, angle):
        endpos = self.cycle + angle
        if (endpos > 20000) and (endpos < self.maximum):
            self.cycle += angle
        elif endpos < 20000:
            self.cycle = 20000
        elif endpos > self.maximum:
            self.cycle =self.maximum
 #       print("cycletime = " + str(self.cycle))
        GPIO.hardware_PWM(self.pin_out, self.frequency, int(self.cycle))

    # stop the current motion
    def stopMotion(self):
        GPIO.hardware_PWM(self.pin_out, self. frequency, 0)

    # go to a certain position
    def gotoPos(self, angle, speed): #gotoPos angle with certain speed (deg/sec)
        endpos = (2 + angle/18)*10000
        if endpos > self.maximum:         #if endpos > max
            endpos = self.maximum
        if endpos < 20000:          #if endpos < min
            endpos = 20000
        increment = (speed/(50*18))*10000 #increment per 1/50 sec
        if self.cycle > endpos:
            increment = -increment
        print('increment='+str(increment))
        while (not((self.cycle+abs(increment)-1 >= endpos) and (self.cycle-abs(increment)+1<=endpos))):
            #print("work")
            self.cycle += increment
            GPIO.hardware_PWM(self.pin_out, self.frequency, int(self.cycle))
            time.sleep(0.02)
        self.stopMotion()
        print("motor" + str(self.pin_out) + " got to position" + str(self.cycle))
    
    # return position in degreees
    def getpos(self):
        return (self.cycle/10000 - 2) * 18

    #clean up at program end
    def clean(self):
        print("clean" + self.pin_out)
        GPIO.write(self.pin_out, 0)
        GPIO.stop()
        print("class cleaned")
