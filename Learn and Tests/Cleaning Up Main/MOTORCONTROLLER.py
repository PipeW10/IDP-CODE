from MOTOR import Motor
from time import sleep

class MControl():
    def __init__ (self):
        self.motorL = Motor(4,5)
        self.motorR = Motor(6,7)
       
    def head_straight(self):
        self.motorL.Forward(100)
        self.motorR.Forward(100)
        #use line tracking to stay on track
        #until node found

    def turn(self,deg):
        #pay attention to line tracking
        fast_speed = 75
        slow_speed = 50
        turn_time = 3

        if deg == 90:
            self.motorL.Forward(fast_speed)
            self.motorR.Forward(slow_speed)
            sleep(turn_time)
        elif deg == -90:
            self.motorR.Forward(fast_speed)
            self.motorL.Forward(slow_speed)
            sleep(turn_time)
        else:
            self.motorL.Forward(fast_speed)
            self.motorR.Reverse(fast_speed)
            sleep(turn_time)
        self.motorL.off()
        self.motorR.off()