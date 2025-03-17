from machine import Pin, PWM
from time import sleep

class Servo:
    
    def __init__(self, pin, freq):
        self.pin = Pin(pin)
        self.pwm = PWM(pin)
        
        # Set Duty Cycle for Different Angles
        self.max_duty = 3650
        self.min_duty = 3250
        self.half_duty = int(self.max_duty/2)
        
        #Set PWM frequency
        self.pwm.freq(freq)
        
        #Make sure servo is dropped
        self.pwm.duty_u16(self.min_duty)
    
    def lift(self):
        self.pwm.duty_u16(self.max_duty)
    
    def drop (self):
        self.pwm.duty_u16(self.min_duty)


