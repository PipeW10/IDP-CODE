from machine import Pin, I2C, PWM 
from tcs34725 import TCS34725
#from vl53l0x import VL53L0X
from SERVO import Servo
from NAVIGATOR import Navigator
from LINES import LineFollower
from time import sleep, sleep_ms


#Class to control all operations the bot does 
#Includes movement, picking up and dropping boxes and selection of future route decisions
class Controller:
    
    def __init__ (self):
        #Initiate navigator and LineFollower classes
        self.nav = Navigator()
        self.linef = LineFollower()
        
        #Set all needed variables to their start values
        self.current_dirc = 1
        self.current_node  = "start"
        self.visit_order = ["locA", "locB", "locC", "locD", "start"]
        self.visit_no = 0
        self.boxes_picked = 0
        #Operation "Lift" or "Drop" or "End"
        self.operation = "Lift"
        
        #Set up forklift Servo
        self.servo = Servo(pin = 15, freq = 50)
        
        #Set up LED
        self.led = Pin(14, Pin.OUT)
        
        #Set up colour sensor
        self.tcs = TCS34725(I2C(id = 0, sda = Pin(8), scl = Pin(9), freq = 50000))
            
    #Called at the start of the run
    def undertake_task(self):
        #Calls get the get out of start function 
        #Drives forward until the first junction is found
        self.linef.out_of_start()
        self.led.value(1)
        #Iterates and calls travel until all of the needed locations have been visited
        while self.visit_no < len(self.visit_order):
            self.travel()
    
    #Function to find the path and directions needed for the next journey
    def start_new_path(self):
        #Depending on what operation is to be done 
        #If the bot has to pick up a box at the end of the journey
        if self.operation == "Lift":
            #End node is the next in the predermined order
            end = self.visit_order[self.visit_no]
            #Keep track of which is the next node to visit
            self.visit_no += 1
        #If the bot is to drop off a box
        elif self.operation == "Drop":
            #Detect the colour of the box picked up to choose a depot as the end point
            #USE COLOUR DETECTION HERE
            end = self.detect_colour_depot()
        #If the operation is to end the run
        elif self.operation == "End":
            #Make the bot return to the start point
            self.visit_no += 1
            end = "start"
        print(end)        
        #Find in the dirc_paths and paths dictionaries the paths needed
        dircs = self.nav.return_dircs(self.current_node, end)
        path = self.nav.return_nodes(self.current_node, end)
        #Return the directions and paths
        return path, dircs
        
    #Travel will control the robots movements for the length of a journey
    def travel(self):
                
        #Number of nodes passed by
        #Used to keep track of where in the journey the bot is
        step = 0
                
        #Get the path to be traversed and the correseponding array of cardinal directions
        path, dircs = self.start_new_path()
        print(self.current_node)
        #Travel through the whole path until the end point is reached
        for step in range(len(path) - 1):
            #calculate how much to turn
            turn_dirc = self.current_dirc - dircs[step]
            #turn corresponding to the turning degrees needed
            if turn_dirc == 0:             
                self.linef.pass_intersection()
            elif turn_dirc ==  -1 or turn_dirc == 3:
                if path[step + 1][:3] == "loc":
                    self.linef.loc_turn(90)
                else:
                    self.linef.turn(90)
            elif turn_dirc == 1 or turn_dirc == -3:
                if path[step + 1][:3] == "loc":
                    self.linef.loc_turn(-90)
                else:
                    self.linef.turn(-90)
                
            #DONT NEED 180 HERE
            #elif turn_dirc == 2 or turn_dirc == -2:
                #self.linef.turn(180)
            #Set what the new current direction is and what the node will be after travelling forward          
            self.current_dirc = dircs[step]
            #Increase step by 1 to keep track of next node to go to
            step += 1
            #Set what the new current direction is and what the node will be after travelling forward 
            self.current_node = path[step]
            #If the end of the path has not been reached
            if step != len(path):
                self.linef.head_straight()
            #If the end of the path has been reached
            else:
                #Exit loop
                continue
        #If the task is to end
        if self.operation == "End":
            #Call finish to enter the start box and turn off light and motors
            self.finish()
        #If the operation is either lift or drop
        else:
            #Call perform operation to either drop or lift the box
            self.perform_op()
        #return current_dirc, current_node

    def perform_op (self):
        if self.operation == "Lift":
            #move forward until box detected
            #while (self.tof.ping()-50 > 10):
                #self.linef.follow_line()
            self.linef.head_straight()
            #lift forklift
            #Servo at 90 degrees
            self.servo.lift()
            
            #Change operation to drop
            self.operation = "Drop"
            #Add 1 to number of boxes picked
            self.boxes_picked += 1
            
            self.linef.exit_loc()
          
        else:
            self.linef.head_straight()
            #lower forklift
            self.servo.drop()
            #BACK UP
            #while (self.tof.ping()-50 < 50):
            self.linef.exit_depot(self.current_node)
            #SHOULD TURN AROUND WHEN NAVIGATING TO NEXT BOX
            if self.boxes_picked == 4:
                self.operation = "End"
            else:
                self.operation = "Lift"
            if self.current_dirc == 1 or self.current_dirc == 2:
                self.current_dirc += 2
            else:
                self.current_dirc -= 2
    #Function to detect the colour of the box 
    def detect_colour_depot(self):
        #Only need to be able to detect one set of colours (ie. red and yellow)
        #read the colour of the box
        colour = self.tcs.read('rgb')
        #will do a range
        if colour[0] == 1:
            end = "dep1"
        else:
            end = "dep2"  
        return end
        

    def finish(self):
        #get into finsh box
        #self.linef.head_straight()
        self.linef.set_speeds(100,100)
        sleep(2)
        #turn motors off
        self.linef.off()
        self.led.value(0)

            
        
