#WILL BE MAIN 
from machine import Pin
from CONTROLLER import Controller


#VARIABLES NEEDED THROUGHOUT CODE
#Set the button which will be used to start the run
button = Pin(12, Pin.IN, Pin.PULL_DOWN)

controller = Controller()

def start():
    
    #Turn blinking LED on
    led = Pin(14, Pin.OUT)
    led.value(1)
    
    controller.undertake_task
    
    led.value(0)
        
#First function to be called
#probably use an interrupt
while (button.value() == 0):
    continue

start()
    

