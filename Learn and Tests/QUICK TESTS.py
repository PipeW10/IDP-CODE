from NAVIGATOR import Navigator
from LINES import LineFollower

nav = Navigator()
linef = LineFollower()

#TEST FROM A TO B
#Number of nodes passed by
#Used to keep track of where in the journey the bot is
step = 0
current_dirc = 1
        
#Get the path to be traversed and the correseponding array of cardinal directions
path = nav.return_nodes("start", "locA")
dircs = nav.return_dircs("start", "locA")

#Travel through the whole path until the end point is reached
for step in range(len(path)):
    #calculate how much to turn
    turn_dirc = current_dirc - dircs[step]
    #turn corresponding to the turning degrees needed
    if turn_dirc == 0:
            pass
    elif turn_dirc ==  -1 or turn_dirc == 3:
            linef.turn(90)
    elif turn_dirc == 1 or turn_dirc == -3:
            linef.turn(-90)
    elif turn_dirc == 2 or turn_dirc == -2:
            linef.turn(180)
    #Set what the new current direction is and what the node will be after travelling forward 
    current_dirc = dircs[step]
    current_node = path[step]
    #Increase step by 1 to keep track of next node to go to
    step += 1
    #If the end of the path has not been reached
    if step != len(path):
        linef.head_straight()
    #If the end of the path has been reached
    else:
        linef.off()
        


#LINE FOLLOW TEST
from LINES import LineFollower
linef = LineFollower()

while True:
    linef.follow_line()
    
    
from machine import Pin
#for testting purposes
interrupt = 0
button = Pin(26, Pin.IN, Pin.PULL_UP)

def start(pin):
    if interrupt == 0:
        interrupt = 1
        #enter code to run here
    else:
        interrupt = 0
        #enter stop code here
        
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=start)   

from NAVIGATOR import Navigator
from time import sleep
from LINES import LineFollower
from machine import Pin


linef = LineFollower()
nav = Navigator()
#LED 
led = Pin(16, Pin.OUT)
led.value(0)



#TEST FROM A TO B
#Number of nodes passed by




    
button = Pin(26, Pin.IN, Pin.PULL_UP)
interrupt = 0

#for testting purposes
def start(pin, interrupt = interrupt):
     #Get the path to be traversed and the correseponding array of cardinal directions
    path = nav.return_nodes("start", "locA")
    dircs = nav.return_dircs("start", "locA")
    step = 0
    current_dirc = 1
    for step in range(len(path)):
        #calculate how much to turn
        turn_dirc = current_dirc - dircs[step]
        #turn corresponding to the  turning degrees needed
        if turn_dirc == 0:
                pass
        elif turn_dirc ==  -1 or turn_dirc == 3:
                linef.turn(90)
        elif turn_dirc == 1 or turn_dirc == -3:
                linef.turn(-90)
        elif turn_dirc == 2 or turn_dirc == -2:
                linef.turn(180)
        #Set what the new current direction is and what the node will be after travelling forward 
        current_dirc = dircs[step]
        current_node = path[step]
        #Increase step by 1 to keep track of next node to go to
        step += 1
        #If the end of the path has not been reached
        if step != len(path):
            linef.head_straight()
        #If the end of the path has been reached
        else:
            linef.off()

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=start)

