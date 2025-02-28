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
    
    def lift(self):
        self.duty_u16(self.max_duty)
    
    def drop (self):
        self.duty_u16(self.min_duty)

servo = Servo(pin = 15, freq = 50) 
