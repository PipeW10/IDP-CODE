from machine import Pin, I2C, PWM 
from tcs34725 import TCS34725
from SERVO import Servo
from NAVIGATOR import Navigator
from MOTORCONTROLLER import MControl


#Class to control all operations the bot does 
#Includes movement, picking up and dropping boxes and selection of future route decisions
class Controller:
    
    def __innit__ (self):
        self.current_dirc = 1
        self.current_node  = "start"
        self.visit_order = ["locA", "locB", "locC", "locD", "start"]
        self.visit_no = 0
        #Operation "Lift" or "Drop" or "End"
        self.operation = "lift"
        self.nav = Navigator()
        self.mcont = MControl()
        self.servo = Servo(pin = 15, freq = 50)
    
    
    def undertake_task(self):
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
            end = "start"
                
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
        
        #Travel through the whole path until the end point is reached
        for step in range(len(path)):
            #calculate how much to turn
            turn_dirc = self.current_dirc - dircs[step]
            #turn corresponding to the turning degrees needed
            match turn_dirc:
                case 0:
                    pass
                case -1 | 3:
                    self.mcont.turn(90)
                case 1 | -3:
                    self.mcont.turn(-90)
                case 2 | -2:
                    self.mcont.turn(180)
            #Set what the new current direction is and what the node will be after travelling forward 
            self.current_dirc = dircs[step]
            self.current_node = path[step]
            #Increase step by 1 to keep track of next node to go to
            step += 1
            #If the end of the path has not been reached
            if step != len(path):
                self.mcont.head_straight()
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
            #lift forklift
            #Servo at 90 degrees
            self.servo.lift()
            
            self.operation = "Drop"
            pass
        else:
            
            #move forward until in box
            #lower forklift
            #servo down
            self.servo.drop()
            #BACK UP
            if self.boxes_picked == 4:
                self.operation = "End"
            else:
                self.operation = "Lift"


    def detect_colour_depot(self):
        raw_yellow  = None
        raw_red = None
        #raw_blue = None
        #raw_green = None
        raw_colour = self.tcs.read(raw = False)
        #will do a range
        if raw_colour == raw_yellow or raw_colour == raw_red:
            end = "dep2"
        else:
            end = "dep1"
            
        return end


    def finsh(self):
        #get into finsh box
        #turn motors off
        pass

            
        