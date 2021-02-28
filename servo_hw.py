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
    minimum_deg = 0
    maximum_deg = 0
    interp_up = False
    interp_down = False
    slope = 0
    axis = 0
    run = False
    free_for_orders = True
        
    # calculate the slope and axis for conversion
    def calcSlope(self):
        if(self.interp_down):
            x1 = 0
        else:
            x1 = self.minimum_deg
        if(self.interp_up):
            x2 = 180
        else:
            x2 = self.maximum_deg
        y1 = self.minimum
        y2 = self.maximum
        self.slope = (y2 -y1) / (x2 - x1)
        self.axis = y1 - (self.slope * x1)
        print("slope = " + str(self.slope) + " axis = " + str(self.axis) + " x1=" + str(x1) + " x2=" + str(x2) + " y1=" + str(y1) + " y2=" + str(y2))

    # create the motor
    def __init__(self, pin, freq, mini, maxi, interpoliere_unten, interpoliere_oben):
        self.pin_out = pin
        self.frequency = freq
        self.maximum = (maxi/18+2)*10000
        self.minimum = (mini/18+2)*10000
        self.maximum_deg = maxi
        self.minimum_deg = mini
        self.interp_down = interpoliere_unten
        self.interp_up = interpoliere_oben

        if self.maximum < self.minimum: #if values are in false order just rearrange them 
            helper = self.maximum
            self.maximum = self.minimum
            self.minimum = helper
            helper = self.maximum_deg
            self.maximum_deg = self.minimum_deg
            self.minimum_deg = helper

        if self.maximum > 120000:
            self.maximum = 120000
            self.maximum_deg = 180

        elif self.maximum < 20000:
            self.maximum = 20000
            self.maximum_deg = 0

        if self.minimum > 120000:
            self.minimum = 120000
            self.minimum_deg = 180

        elif self.minimum < 20000:
            self.minimum = 20000
            self.minimum_deg = 0   
        self.calcSlope()     

    # initialize the PWM Controlling
    def initialize(self):
        #print("initialize" + str(self.pin_out))
        GPIO.set_mode(self.pin_out,pigpio.ALT5)
#        GPIO.hardware_PWM(self.pin_out, self.frequency, self.cycle)
 #       time.sleep(0.2)
        GPIO.hardware_PWM(self.pin_out, self.frequency, 0)

    # set the cycle time to a certain value
    def setCycle(self, value):
        self.cycle = self.slope * value + self.axis

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
        GPIO.hardware_PWM(self.pin_out, self.frequency, 0)

    # go to a certain position
    def gotoPos(self, angle, speed): #gotoPos angle with certain speed (deg/sec)
        self.run = True
        self.free_for_orders = False
        print("motor" + str(self.pin_out) + " gotoPos " + str(angle) + " " + str(speed))
        endpos = self.slope * angle + self.axis
        if endpos > self.maximum:         #if endpos > max
            endpos = self.maximum
        if endpos < self.minimum:          #if endpos < min
            endpos = self.minimum
        increment = (speed/(50*18))*10000 #increment per 1/50 sec
        if self.cycle > endpos:
            increment = -increment
        print('increment='+str(increment))
        while (not((self.cycle+abs(increment)-1 >= endpos) and (self.cycle-abs(increment)+1<=endpos)) and self.run == True):
            #print("work")
            self.cycle += increment
            GPIO.hardware_PWM(self.pin_out, self.frequency, int(self.cycle))
            time.sleep(0.02)
        if(self.run == True):
            self.cycle = endpos
            GPIO.hardware_PWM(self.pin_out, self.frequency, int(self.cycle))
            time.sleep(0.02)
        self.stopMotion()
        self.run = False
        self.free_for_orders = True
        print("motor" + str(self.pin_out) + " got to position" + str(self.cycle))


    # return position in degreees
    def getpos(self):
        return (self.cycle - self.axis) / self.slope

    #clean up at program end
    def clean(self):
        print("clean" + self.pin_out)
        GPIO.write(self.pin_out, 0)
        GPIO.stop()
        print("class cleaned")
