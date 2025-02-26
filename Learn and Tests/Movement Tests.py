#Test Writing of Actual Code
#CHECK HOW TO INTEGRATE LINE TRACKING SEAMLESSLY. PROBABLY LET LINETRACKING TAKE CARE OF HEAD STRAIGHT AND FOCUS ON GOOD TURNING
current_dirc = 1
current_node  = "start"
visit_order = ["locA", "locB", "locC", "locD", "start"]
visit_no = 0
operation = "lift"

#current_path = map.shortest_path("start", "locC")
#future_dircs = map.path_direction(path = current_path, dirc_map = direction_map)

#MAKE SEPARATE FILE WITH THESE MAYBE
#Dictionary of all needed paths using nodes
paths = None
#Dictionary of all needed paths in cardinal 
dirc_paths = None


#Operation "Lift" or "Drop" or "End"
def start_new_path(current_node, end, dirc_paths = dirc_paths, paths = paths):
    dircs = dirc_paths[current_node][end]
    path = paths[current_node][end]
    return path, dircs
    

def travel(end, current_dirc, current_node, operation, visit_order, visit_no):
    step = 0
    if operation == "Lift":
        end = visit_order[visit_no]
        visit_no += 1
    elif operation == "Drop":
        #USE COLOUR DETECTION HERE
        end = detect_colour_depot
    elif operation == "End":
        end = "start"
    
    path, dircs = start_new_path(current_node, end)
    
    for step in range(len(path)):
        turn_dirc = current_dirc - dircs[step]
        match turn_dirc:
            case 0:
                pass
            case -1 | 3:
                turn(90)
            case 1 | -3:
                turn(-90)
            case 2 | -2:
                turn (180)
        current_dirc = dircs[step]
        current_node = path[step]
        step += 1
        if step != len(path):
            head_straight()
        else:
            continue
        
    if operation == "End":
        finish()
    else:
        perform_op(operation)
    return current_dirc, current_node

def perform_op (operation):
    if operation == "Lift":
        #move forward until box detected
        #lift forklift
        #Servo at 90 degrees
        servo.duty_u16(half_duty)
        sleep(2)
        pass
    else:
        #servo down
        servo.duty_u16(min_duty)
        sleep(2)
        #move forward until in box
        #lower forklift
        pass

def head_straight():
    motorL.Forward(100)
    motorR.Forward(100)
    #use line tracking to stay on track
    #until node found

def turn(deg):
    #pay attention to line tracking
    fast_speed = 75
    slow_speed = 50
    turn_time = 3
    
    if deg == 90:
        motorL.Forward(fast_speed)
        motorR.Forward(slow_speed)
        sleep(turn_time)
    elif deg == -90:
        motorR.Forward(fast_speed)
        motorL.Forward(slow_speed)
        sleep(turn_time)
    else:
        motorL.Forward(fast_speed)
        motorR.Reverse(fast_speed)
        sleep(turn_time)

def finsh():
    motorL.off()
    motorR.off()
    light.off()
        