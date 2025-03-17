# Black land with white lines
# 4 sensors front-aligned horizontally
# Also assuming the robot can rotate about its COM (this can be adjusted for a smooth turn )
# Assumes Pin=1 --> white/line, and Pin=0 black/non-line
from machine import Pin, PWM
from MOTOR import Motor
from time import sleep, sleep_ms

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
        self.COR_SPEED = 80# Correction speed of slower motor
               
        self.last_valid_state = "F" # Start with Forward state

    def read_sensors(self): # current sensor states
        return [self.S1.value(), self.S2.value(), self.S3.value(), self.S4.value()]

    #Heads straight following the line until an intersection is found
    def head_straight(self):
        while self.intersection() == False:
            self.follow_line()
        #Turn motors off for more consistent turning
        self.off()

    def follow_line(self): # FOLLOWING A LINE
        sensors = self.read_sensors()

        #Reads values of two middle sensors and decides based on their values
        if sensors[1] == 1 and sensors[2] == 1: # Centered on the line
            #Set both motors to nominal speed
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "F" #Forward

        elif sensors[1] == 1 and sensors[2] == 0: # Drifting right
            #Slow down left motor to correct 
            self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "L"

        elif sensors[2] == 1 and sensors[1] == 0: # Drifting left
            #Slow down right motor to correct
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            self.last_valid_state = "R"
                
        else: # continue last valid action for unexpected states
            if self.last_valid_state == "F":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "L":
                self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "R":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            #COUDL GET RID OF
            elif self.last_valid_state == "stop":
                self.off()
            
    def pass_intersection(self):
        while self.intersection() == True:
            self.follow_line()

    def intersection(self):
        sensors = self.read_sensors()
        #If an intersection is detected
        if sensors[0] == 1 or sensors[3] == 1:
            intersection = True
        #If no interection is detected
        else:
            intersection = False
        return intersection
    
    #CHECK THIS WORKS PROPERLY
    #Function to get bot out of the start box and following the first line
    #Check it works with FIRST WHITE LINE
    def out_of_start(self):
        while self.read_sensors()[3] != 1:
            self.set_speeds(75,75)
        self.off()
            
    def loc_turn(self,deg):
        
        f_fast_speed = 75
        r_slow_speed = 40
        keep_driving = 500
        turn_time = 500
        if deg == 90: #Right turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorL.Forward(f_fast_speed)
            self.motorR.Reverse(r_slow_speed)
            #self.set_speeds(f_fast_speed, -r_slow_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[1] == 0):
                continue
        elif deg == -90: #Left turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorR.Forward(f_fast_speed)
            self.motorL.Reverse(r_slow_speed)
            #self.set_speeds(-r_slow_speed, f_fast_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[2] == 0):
                continue
    
    def turn(self,deg):
        #pay attention to line tracking
        #Fast and slow speeds to set the motors to depending on the turn 
        fast_speed = 80
        slow_speed = 30
        
        #Amount of time before the sensors start trying to detect if teh robot has turned
        #Used to avoid stopping the turn too early
        turn_time = 500
        f_turn_time = 3000

        if deg == 90: #Right turn
            #Set left motor to turn quick and right to turn slow
            self.motorL.Forward(fast_speed)
            self.motorR.Forward(slow_speed)
            #self.set_speeds(fast_speed, slow_speed)
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[1] == 0):
                continue
        elif deg == -90: #Left turn
            #Set left motor to turn quick and right to turn slow
            self.motorR.Forward(fast_speed)
            self.motorL.Forward(slow_speed)
            #self.set_speeds(slow_speed, fast_speed)
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[2] == 0):
                continue
        elif deg == 180: #180 degree turn clockwise
            #Set both motors to turn in opposite directions 
            self.motorL.Forward(75)
            self.motorR.Reverse(75)
            #Wait for the given time
            sleep_ms(f_turn_time)
        elif deg == -180:
            self.motorR.Forward(75)
            self.motorL.Reverse(75)
            #Wait for the given time
            sleep_ms(f_turn_time)
            #Try to detect the line. Exits loop when line is detcted
        #Turn motors off to make line tracking more consistent
        self.off()
            
    #Set the motor speeds
    def set_speeds(self, left_speed, right_speed):
        self.motorL.Forward(left_speed) #Left motor
        self.motorR.Forward(right_speed) #Right motor
        
    def exit_loc(self):          
        self.motorL.Reverse(75)
        self.motorR.Reverse(75)
        sleep_ms(1000)
        
        self.turn(180)
        #sleep_ms(500)
        self.motorL.Reverse(75)# Black land with white lines
# 4 sensors front-aligned horizontally
# Also assuming the robot can rotate about its COM (this can be adjusted for a smooth turn )
# Assumes Pin=1 --> white/line, and Pin=0 black/non-line
from machine import Pin, PWM
from MOTOR import Motor
from time import sleep, sleep_ms

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
        self.COR_SPEED = 65# Correction speed of slower motor
               
        self.last_valid_state = "F" # Start with Forward state

    def read_sensors(self): # current sensor states
        return [self.S1.value(), self.S2.value(), self.S3.value(), self.S4.value()]

    #Heads straight following the line until an intersection is found
    def head_straight(self):
        while self.intersection() == False:
            self.follow_line()
        #Turn motors off for more consistent turning
        self.off()

    def follow_line(self): # FOLLOWING A LINE
        sensors = self.read_sensors()

        #Reads values of two middle sensors and decides based on their values
        if sensors[1] == 1 and sensors[2] == 1: # Centered on the line
            #Set both motors to nominal speed
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "F" #Forward

        elif sensors[1] == 1 and sensors[2] == 0: # Drifting right
            #Slow down left motor to correct 
            self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            self.last_valid_state = "L"

        elif sensors[2] == 1 and sensors[1] == 0: # Drifting left
            #Slow down right motor to correct
            self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            self.last_valid_state = "R"
                
        else: # continue last valid action for unexpected states
            if self.last_valid_state == "F":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "L":
                self.set_speeds(left_speed = self.COR_SPEED, right_speed = self.NOM_SPEED)
            elif self.last_valid_state == "R":
                self.set_speeds(left_speed = self.NOM_SPEED, right_speed = self.COR_SPEED)
            #COUDL GET RID OF
            elif self.last_valid_state == "stop":
                self.off()
            
    def pass_intersection(self):
        while self.intersection() == True:
            self.follow_line()

    def intersection(self):
        sensors = self.read_sensors()
        #If an intersection is detected
        if sensors[0] == 1 or sensors[3] == 1:
            intersection = True
        #If no interection is detected
        else:
            intersection = False
        return intersection
    
    #CHECK THIS WORKS PROPERLY
    #Function to get bot out of the start box and following the first line
    #Check it works with FIRST WHITE LINE
    def out_of_start(self):
        while self.read_sensors()[3] != 1:
            self.set_speeds(75,75)
        self.off()
            
    def loc_turn(self,deg):
        
        f_fast_speed = 75
        r_slow_speed = 40
        keep_driving = 500
        turn_time = 500
        if deg == 90: #Right turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorL.Forward(f_fast_speed)
            self.motorR.Reverse(r_slow_speed)
            #self.set_speeds(f_fast_speed, -r_slow_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[1] == 0):
                continue
        elif deg == -90: #Left turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorR.Forward(f_fast_speed)
            self.motorL.Reverse(r_slow_speed)
            #self.set_speeds(-r_slow_speed, f_fast_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[2] == 0):
                continue
    
    def turn(self,deg):
        #pay attention to line tracking
        #Fast and slow speeds to set the motors to depending on the turn 
        f_fast_speed = 85
        r_slow_speed = 40
        
        #Amount of time before the sensors start trying to detect if teh robot has turned
        #Used to avoid stopping the turn too early
        turn_time = 500
        keep_driving = 250
        f_turn_time = 2250

        if deg == 90: #Right turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorL.Forward(f_fast_speed)
            self.motorR.Reverse(r_slow_speed)
            #self.set_speeds(f_fast_speed, -r_slow_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[1] == 0):
                continue
        elif deg == -90: #Left turn
            self.set_speeds(f_fast_speed, f_fast_speed)
            sleep_ms(keep_driving)
            #Set left motor to turn quick and right to turn slow
            self.motorR.Forward(f_fast_speed)
            self.motorL.Reverse(r_slow_speed)
            #self.set_speeds(-r_slow_speed, f_fast_speed)
            #Wait for the given time
            sleep_ms(turn_time)
            #Try to detect the line. Exits loop when line is detcted
            while (self.read_sensors()[2] == 0):
                continue
        elif deg == 180: #180 degree turn clockwise
            #Set both motors to turn in opposite directions 
            self.motorL.Forward(75)
            self.motorR.Reverse(75)
            #Wait for the given time
            sleep_ms(f_turn_time)
        elif deg == -180:
            self.motorR.Forward(75)
            self.motorL.Reverse(75)
            #Wait for the given time
            sleep_ms(f_turn_time)
            #Try to detect the line. Exits loop when line is detcted
        #Turn motors off to make line tracking more consistent
        self.off()
            
    #Set the motor speeds
    def set_speeds(self, left_speed, right_speed):
        self.motorL.Forward(left_speed) #Left motor
        self.motorR.Forward(right_speed) #Right motor
        
    def exit_loc(self):
        
        self.motorL.Reverse(85)
        self.motorR.Reverse(85)
        sleep_ms(500)
        while self.read_sensors()[0] == 0:
            continue
        #self.turn(180)
        #=#sleep_ms(500)
        #self.motorL.Reverse(75)
        #self.motorR.Reverse(75)
        #sleep_ms(1000)
        
        self.off()
    
    def exit_depot(self, dep):
        self.motorL.Reverse(75)
        self.motorR.Reverse(75)
        sleep_ms(1500)
        
        if dep == "dep1":
            self.turn(180)
        else:
            self.turn(-180)
        self.off()
        
        self.motorL.Reverse(75)
        self.motorR.Reverse(75)
        sleep_ms(1500)
    #Turn both motors off
    def off(self):
        self.motorL.off()
        self.motorR.off()

        self.motorR.Reverse(75)
        sleep_ms(1000)
        
        self.off()
    
    def exit_depot(self, dep):
        self.motorL.Reverse(75)
        self.motorR.Reverse(75)
        sleep_ms(1500)
        
        if dep == "dep1":
            self.turn(180)
        else:
            self.turn(-180)
        self.off()
        
        self.motorL.Reverse(75)
        self.motorR.Reverse(75)
        sleep_ms(1500)
    #Turn both motors off
    def off(self):
        self.motorL.off()
        self.motorR.off()
