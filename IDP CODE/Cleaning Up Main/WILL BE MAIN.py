#WILL BE MAIN 
from machine import Pin
from CONTROLLER import Controller


#VARIABLES NEEDED THROUGHOUT CODE
#Set the button which will be used to start the run
button = Pin(26, Pin.IN, Pin.PULL_UP)
#Turn blinking LED on


controller = Controller()

def start(pin):
    
    controller.undertake_task()

        
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=start)   


