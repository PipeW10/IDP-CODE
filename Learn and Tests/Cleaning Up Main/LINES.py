# Black land with white lines
# 4 sensors front-aligned horizontally
# Also assuming the robot can rotate about its COM (this can be adjusted for a smooth turn )
# Assumes Pin=1 --> white/line, and Pin=0 black/non-line
from machine import Pin, PWM
from MOTOR import Motor

class LineFollower():
    
    def __init__ (self):
        self.S1 = Pin(1, Pin.IN) # Leftmost sensor ADJUST FOR CORRECT PINS
        self.S2 = Pin(2, Pin.IN) # Left sensor
        self.S3 = Pin(3, Pin.IN) # Right sensor
        self.S4 = Pin(4, Pin.IN) # Rightmost sensor

        # Define motor control pins
        self.left_motor = Motor(4,5)
        self.right_motor = Motor(7,6)

        self.NOM_SPEED = 100 # Nominal motor speed # ADJUST FOR TURNING STRENGTH
        self.COR_SPEED = 85 # Correction speed of slower motor
               
        self.last_valid_state = None # Start with no state

    def read_sensors(self): # current sensor states
        return [self.S1.value(), self.S2.value(), self.S3.value(), self.S4.value()]

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
            self.move_forward()
            last_valid_state = "following_line"

        elif sensors == [0, 1, 0, 0] or sensors == [1, 0, 0, 0]: # Drifting left
            self.sml_turn_right()
            last_valid_state = "sligthly_turning_right"

        elif sensors == [0, 0, 1, 0] or sensors == [0, 0, 0, 1]: # Drifting right
            self.sml_turn_left()
            last_valid_state = "slightly_turning_left"

        elif sensors == [0, 0, 0, 0]: # No line detected
            if last_valid_state == "following_line":
                self.move_forward()
            elif last_valid_state == "slightly_turning_left":
                self.sml_turn_left()
            elif last_valid_state == "slightly_turning_right":
                self.sml_turn_right()
            else:
                self.stop()
                last_valid_state = "stop"

        else: # continue last valid action for unexpected states
            if last_valid_state == "following_line":
                self.move_forward()
            elif last_valid_state == "turning_left":
                self.sml_turn_left()
            elif last_valid_state == "turning_right":
                self.sml_turn_right()
            elif last_valid_state == "stop":
                self.stop()

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