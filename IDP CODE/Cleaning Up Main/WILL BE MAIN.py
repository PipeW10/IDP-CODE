#WILL BE MAIN 
from machine import Pin
from CONTROLLER import Controller


#VARIABLES NEEDED THROUGHOUT CODE
#Set the button which will be used to start the run
button = Pin(26, Pin.IN, Pin.PULL_UP)
#Turn blinking LED on
led = Pin(16, Pin.OUT)

controller = Controller()

def start(pin):
    

    led.value(1)
    
    controller.undertake_task()
    
    led.value(0)
        
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=start)   


