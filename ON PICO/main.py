#MAIN
from machine import Pin
from CONTROLLER import Controller
import utime


#VARIABLES NEEDED THROUGHOUT CODE
#Set the button which will be used to start the run
button = Pin(26, Pin.IN, Pin.PULL_UP)
led = Pin(14, Pin.OUT)
led.value(0)


controller = Controller()
last_time = 0
def start(pin):
    global last_time
    current_time = utime.ticks_ms()

    #led.value(1)
    if utime.ticks_diff(current_time, last_time) > 1000:
        last_time = current_time
        controller.undertake_task()
    
    #led.value(0)
        
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=start)   




