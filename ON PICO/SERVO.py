from machine import Pin, PWM
from time import sleep

class Servo:
    
    def __init__(self, pin, freq):
        self.pin = Pin(pin)
        self.pwm = PWM(pin)
        
        # Set Duty Cycle for Different Angles
        self.max_duty = 7864
        self.min_duty = 1802
        self.half_duty = int(self.max_duty/2)
        
        #Set PWM frequency
        self.freq = freq
        self.freq (self.freq)

servo = Servo(pin = 15, freq = 50) 


    
try:
    while True:
        #Servo at 0 degrees
        servo.duty_u16(min_duty)
        sleep(2)
        #Servo at 90 degrees
        servo.duty_u16(half_duty)
        sleep(2)
        #Servo at 180 degrees
        servo.duty_u16(max_duty)
        sleep(2)
except KeyboardInterrupt:
    print("Keyboard interrupt")
    # Turn off PWM
    servo.deinit()