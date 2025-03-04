# Black land with white lines
# 4 sensors front-aligned horizontally
# Also assuming the robot can rotate about its COM (this can be adjusted for a smooth turn )
# Assumes Pin=1 --> white/line, and Pin=0 black/non-line
from machine import Pin, PWM
from MOTOR import Motor
from MOTORCONTROLLER import MControl

class LineFollower():
    
    def __init__ (self):
        self.S1 = Pin(20, Pin.IN) # Leftmost sensor ADJUST FOR CORRECT PINS
        self.S2 = Pin(18, Pin.IN) # Left sensor
        self.S3 = Pin(19, Pin.IN) # Right sensor
        self.S4 = Pin(21, Pin.IN) # Rightmost sensor

        # Define motor control pins GET RID OF MOTORS USE MCONTROL
        self.left_motor = Motor(4,5)
        self.right_motor = Motor(7,6)
        self.mcont = MControl()

        self.NOM_SPEED = 100 # Nominal motor speed # ADJUST FOR TURNING STRENGTH
        self.COR_SPEED = 0 # Correction speed of slower motor
               
        self.last_valid_state = "F" # Start with Forward state

    def read_sensors(self): # current sensor states
        return [0, self.S2.value(), self.S3.value(), 0]

    #WILL GET RID OF THESE TURNS
    def move_forward(self): # forward command
        self.left_motor.Forward(self.NOM_SPEED)
        self.right_motor.Forward(self.NOM_SPEED)

    def sml_turn_left(self): # correct by slightly turning left
        self.left_motor.Forward(self.COR_SPEED)
        self.right_motor.Forward(self.NOM_SPEED)

    def sml_turn_right(self): # correct by slightly turning right
        self.left_motor.Forward(self.NOM_SPEED)
        self.right_motor.Forward(self.COR_SPEED)

    def stop(self):
        self.left_motor.Forward(0)
        self.right_motor.Forward(0)

    def reverse(self):
        self.left_motor.Forward(-self.NOM_SPEED)
        self.right_motor.Forward(-self.NOM_SPEED)



    def follow_line(self): # SIMPLY FOLLOWING A LINE
        sensors = self.read_sensors()

        if sensors == [0, 1, 1, 0]: # Centered on the line
            #self.mcont.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            self.move_forward()
            self.last_valid_state = "F"

        elif sensors == [0, 1, 0, 0] or sensors == [1, 0, 0, 0]: # Drifting right
            #self.mcont.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            self.sml_turn_left()
            self.last_valid_state = "L"

        elif sensors == [0, 0, 1, 0] or sensors == [0, 0, 0, 1]: # Drifting left
            #self.mcont.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            self.sml_turn_right()
            self.last_valid_state = "L"

        elif sensors == [0, 0, 0, 0]: # No line detected
            if self.last_valid_state == "F":
                #self.mcont.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
                self.move_forward()
            elif self.last_valid_state == "L":
                #self.mcont.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
                self.sml_turn_left()
            elif self.last_valid_state == "R":
                #self.mcont.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
                self.sml_turn_right()
            else:
                #self.mcont.off()
                self.stop()
                self.last_valid_state = "stop"
                
        #IS THIS REDUNDANT????
        else: # continue last valid action for unexpected states
            if self.last_valid_state == "F":
                self.move_forward()
            elif self.last_valid_state == "L":
                self.sml_turn_left()
            elif self.last_valid_state == "R":
                self.sml_turn_right()
            elif self.last_valid_state == "stop":
                self.stop()

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
        