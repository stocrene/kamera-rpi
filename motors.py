from servo_hw import servomotor
import threading
import time
import json

class motor_xy:
    remaining_time = 0
    speed_x = 0
    speed_y = 0

    # initialize the needed motors
    def __init__ (self, pinx, piny, freq):
        self.x_motor = servomotor(pinx, freq, 10, 180, True, True)
        self.y_motor = servomotor(piny, freq, 10, 90, True, False)
        self.x_motor.initialize()
        self.x_motor.initialize()
        fd = open("/home/pi/kamera-rpi/position.txt", "r")
        if fd.mode == 'r':
            content = fd.read()
        fd.close()
        jdata = json.loads(content)
        if (("xpos" not in jdata) or ("ypos" not in jdata)):
            self.gotoposition(0,0)
            print("did not find a loadable positioning file")
        else:
            self.catchOldPosition(jdata["xpos"], jdata["ypos"])
            print("positioning file: "+content+" found")
    
    # recreate the former position by overwriting the cycletime
    def catchOldPosition(self, x, y):
        self.x_motor.setCycle(-x+180)
        self.y_motor.setCycle(y)
        
    # send both motors to a certain position with fixed speed
    def gotoposition(self, x, y):
        print("gotoposition "+ str(-x+180)+" "+str(y))
        # kill every command to drive
        self.cancel_latest()
        self.remaining_time = 0
        while ((self.x_motor.free_for_orders == False) or (self.y_motor.free_for_orders == False)):
            time.sleep(0.0001)
        x_thread = threading.Thread(target=self.x_motor.gotoPos, args=(-x+180, 45))
        y_thread = threading.Thread(target=self.y_motor.gotoPos, args=(y, 45))
        x_thread.start()
        y_thread.start()
        print("threads started")
        x_thread.join()
        y_thread.join()
        print("threads done")

    # walk in a certain direction with a certain speed until a timer runs out
    # gets called by set_speeds() do not call this function in paticular
    def walk_til_dead(self):
        self.remaining_time = 10         #set watchdog
        while self.remaining_time > 0: #while watchdog gets reseted within 0.2sec
    #        print("timer = " + str(self.remaining_time))
            if(abs(self.speed_x)> 15):
                x_step_thread = threading.Thread(target=self.x_motor.goOneStep, args=[-self.speed_x*5.55])
                x_step_thread.start()
                x_step_thread.join()
            
            if(abs(self.speed_y)> 15):
                y_step_thread = threading.Thread(target=self.y_motor.goOneStep, args=[self.speed_y*5.55])
                y_step_thread.start()
                y_step_thread.join()
            time.sleep(0.02)
            self.remaining_time -= 1
        self.x_motor.stopMotion()
        self.y_motor.stopMotion()

    # reset the timer for walk_til_dead()
    def reset_timer(self):
        self.remaining_time = 10    #reset watchdog
    
    # send motor in a certain direction at a certain speed. 
    # must be recalled each 200ms so the timer does not run out
    def set_speeds(self, x, y):     #set variables
        self.speed_x = x   
        self.speed_y = y
        self.cancel_latest()        
        while ((self.x_motor.free_for_orders == False) or (self.y_motor.free_for_orders == False)):
            time.sleep(0.0001)
        if self.remaining_time == 0:    #if no thread lives right now
           # print("trying to start the walkinthread")
            walkinthread = threading.Thread(target=self.walk_til_dead, args=())
            walkinthread.start()
        elif self.remaining_time >0:
            self.reset_timer()
    
    # return motorpositions in degree
    def get_positions(self):
 #       return self.x_motor.getpos(), self.y_motor.getpos()
        xpos = 180 - self.x_motor.getpos()
        ypos = self.y_motor.getpos()
        filecontent = "{\"xpos\":" + str(round(xpos)) + ",\"ypos\":"+str(round(ypos))+"}"
#        print(filecontent)
        fd = open("/home/pi/kamera-rpi/position.txt","w+")
        fd.write(filecontent)
        fd.close()
        return round(xpos), round(ypos)

    # cancel latest movement
    def cancel_latest(self):
        self.x_motor.run = False
        self.y_motor.run = False