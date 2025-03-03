from NAVIGATOR import Navigator
from MOTORCONTROLLER import MControl

nav = Navigator()
mcont = MControl()

#Number of nodes passed by
#Used to keep track of where in the journey the bot is
step = 0
        
#Get the path to be traversed and the correseponding array of cardinal directions
path = return_path("start", "depA")
dircs = return_dircs("start", "depA")

#Travel through the whole path until the end point is reached
for step in range(len(path)):
    #calculate how much to turn
    turn_dirc = current_dirc - dircs[step]
    #turn corresponding to the turning degrees needed
    match turn_dirc:
        case 0:
            pass
        case -1 | 3:
            mcont.turn(90)
        case 1 | -3:
            mcont.turn(-90)
        case 2 | -2:
            mcont.turn(180)
    #Set what the new current direction is and what the node will be after travelling forward 
    current_dirc = dircs[step]
    current_node = path[step]
    #Increase step by 1 to keep track of next node to go to
    step += 1
    #If the end of the path has not been reached
    if step != len(path):
        mcont.head_straight()
    #If the end of the path has been reached
    else:
        mcont.off()