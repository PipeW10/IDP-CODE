from NAVIGATOR import Navigator
from MOTORCONTROLLER import MControl

nav = Navigator()
mcont = MControl()

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
            mcont.turn(90)
    elif turn_dirc == 1 or turn_dirc == -3:
            mcont.turn(-90)
    elif turn_dirc == 2 or turn_dirc == -2:
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
        


#LINE FOLLOW TEST
from LINES import LineFollower
linef = LineFollower()

while True:
    linef.follow_line()
    