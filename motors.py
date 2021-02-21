from servo_hw import servomotor
import threading
import time

class motor_xy:
    remaining_time = 0
    speed_x = 0
    speed_y = 0

    # initialize the needed motors
    def __init__ (self, pinx, piny, freq):
        self.x_motor = servomotor(pinx, freq, 180)
        self.y_motor = servomotor(piny, freq, 60)
        self.x_motor.initialize()
        self.x_motor.initialize()
    
    # send both motors to a certain position with fixed speed
    def gotoposition(self, x, y):
        x_thread = threading.Thread(target=self.x_motor.gotoPos, args=(x, 45))
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
            print("timer = " + str(self.remaining_time))
            x_step_thread = threading.Thread(target=self.x_motor.goOneStep, args=[self.speed_x*5.55])
            y_step_thread = threading.Thread(target=self.y_motor.goOneStep, args=[self.speed_y*5.55])
            x_step_thread.start()
            y_step_thread.start()
            x_step_thread.join()
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
        print("speeds set")
        if self.remaining_time == 0:    #if no thread lives right now
            print("trying to start the walkinthread")
            walkinthread = threading.Thread(target=self.walk_til_dead, args=())
            walkinthread.start()
        elif self.remaining_time >0:
            self.reset_timer()
    
    # return motorpositions in degree
    def get_positions(self):
        return self.x_motor.getpos(), self.y_motor.getpos()