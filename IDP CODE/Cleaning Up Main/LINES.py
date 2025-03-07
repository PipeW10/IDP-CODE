# Black land with white lines
# 4 sensors front-aligned horizontally
# Also assuming the robot can rotate about its COM (this can be adjusted for a smooth turn )
# Assumes Pin=1 --> white/line, and Pin=0 black/non-line
from machine import Pin, PWM
from MOTOR import Motor
from time import sleep

class LineFollower():
    
    def __init__ (self):
        self.S1 = Pin(20, Pin.IN) # Leftmost sensor ADJUST FOR CORRECT PINS
        self.S2 = Pin(18, Pin.IN) # Left sensor
        self.S3 = Pin(19, Pin.IN) # Right sensor
        self.S4 = Pin(21, Pin.IN) # Rightmost sensor

        # Define motor control pins GET RID OF MOTORS USE ROL
        self.motorL = Motor(4,5)
        self.motorR = Motor(7,6)

        self.NOM_SPEED = 100 # Nominal motor speed # ADJUST FOR TURNING STRENGTH
        self.COR_SPEED = 60 # Correction speed of slower motor
               
        self.last_valid_state = "F" # Start with Forward state

    def read_sensors(self): # current sensor states
        return [self.S1.value(), self.S2.value(), self.S3.value(), self.S3.value()]

           #Heads straight following the line until an intersection is found
    def head_straight(self):
        while self.linef.intersection_type() == "NO INTERSECTION":
            self.linef.follow_line()

    def follow_line(self): # SIMPLY FOLLOWING A LINE
        sensors = self.read_sensors()

        if sensors[1] == 1 and sensors[2] == 1: # Centered on the line
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "F"

        elif sensors[1] == 1 and sensors[2] == 0: # Drifting right
            self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "L"

        elif sensors[2] == 1 or sensors[1] == 0: # Drifting left
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            self.last_valid_state = "R"

        elif sensors == [0, 0, 0, 0]: # No line detected
            if self.last_valid_state == "F":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "L":
                self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "R":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            else:
                self.off()
                self.last_valid_state = "stop"
                
        #IS THIS REDUNDANT????
        else: # continue last valid action for unexpected states
            if self.last_valid_state == "F":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "L":
                self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "R":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            elif self.last_valid_state == "stop":
                self.off()

    #PROBS GET RID OF
    def intersection_type(self):
        sensors = self.read_sensors()

        if sensors == [1, 1, 1, 1]:
            intersection = "STEM" # approaching from base of T junction
        elif sensors == [1, 1, 0, 0] or sensors == [1, 1, 1, 0]:
            intersection = "RIGHT ARM" # approaching from right arm of T junction
        elif sensors == [0, 0, 1, 1] or sensors == [0, 1, 1, 1]:
            intersection = "LEFT ARM" # approaching from left arm of T junction
        else:
            intersection = "NO INTERSECTION"

        return intersection
    
    #CHECK THIS WORKS PROPERLY
    #Function to get bot out of the start box and following the first line
    #Check it works with FIRST WHITE LINE
    def out_of_start(self):
        sensors = self.read_sensors()
        while sensors != [0,1,1,0]:
            self.follow_line()
    
    def turn(self,deg):
        #pay attention to line tracking
        f_fast_speed = 75
        r_slow_speed = 20
        
        turn_time = 1.0
        f_turn_time = 2.5

        if deg == 90:
            self.motorL.Forward(f_fast_speed)
            self.motorR.Forward(r_slow_speed)
            sleep(turn_time)
            while (self.read_sensors()[1] == 0):
                sleep(0.1)
        elif deg == -90:
            self.motorR.Forward(f_fast_speed)
            self.motorL.Forward(r_slow_speed)
            sleep(turn_time)
            while (self.read_sensors()[2] == 0):
                sleep(0.1)
        else:
            self.motorL.Forward(f_fast_speed)
            self.motorR.Reverse(f_fast_speed)
            sleep(f_turn_time)
            while (self.read_sensors()[1] == 0):
                sleep(0.1)
        self.off()
        
    def set_speeds(self, left_speed, right_speed):
        self.motorL.Forward(left_speed)
        self.motorR.Forward(right_speed)
    
    def off(self):
        self.motorL.off()
        self.motorR.off()


