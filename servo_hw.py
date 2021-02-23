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
    minimum = 0
    maximum = 0
    
    # create the motor
    def __init__(self, pin, freq, mini, maxi):
        self.pin_out = pin
        self.frequency = freq
        self.maximum = (maxi/18+2)*10000
        self.minimum = (mini/18+2)*10000

        if self.maximum < self.minimum: #if values are in false order just rearrange them 
            helper = self.maximum
            self.maximum = self.minimum
            self.minimum = helper

        if self.maximum > 120000:
            self.maximum = 120000

        elif self.maximum < 20000:
            self.maximum = 20000

        if self.minimum > 120000:
            self.minimum = 120000

        elif self.minimum < 20000:
            self.minimum = 20000        

    # initialize the PWM Controlling
    def initialize(self):
        #print("initialize" + str(self.pin_out))
        GPIO.set_mode(self.pin_out,pigpio.ALT5)
#        GPIO.hardware_PWM(self.pin_out, self.frequency, self.cycle)
 #       time.sleep(0.2)
        GPIO.hardware_PWM(self.pin_out, self.frequency, 0)

    # set the cycle time to a certain value
    def setCycle(self, value):
        self.cycle = (value / 18 + 2)* 10000

    # go exactly one step with a certain angle
    def goOneStep(self, angle):
        endpos = self.cycle + angle
        if (endpos > self.minimum) and (endpos < self.maximum):
            self.cycle += angle
        elif endpos < self.minimum:
            self.cycle = self.minimum
        elif endpos > self.maximum:
            self.cycle =self.maximum
 #       print("cycletime = " + str(self.cycle))
        GPIO.hardware_PWM(self.pin_out, self.frequency, int(self.cycle))

    # stop the current motion
    def stopMotion(self):
        GPIO.hardware_PWM(self.pin_out, self. frequency, 0)

    # go to a certain position
    def gotoPos(self, angle, speed): #gotoPos angle with certain speed (deg/sec)
        print("gotoPos " + str(angle) + " " + str(speed))
        endpos = (2 + angle/18)*10000
        if endpos > self.maximum:         #if endpos > max
            endpos = self.maximum
        if endpos < self.minimum:          #if endpos < min
            endpos = self.minimum
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
