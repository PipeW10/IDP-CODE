from machine import Pin, PWM
from time import sleep

class Servo:
    
    def __init__(self, pin, freq):
        self.pin = Pin(pin)
        self.pwm = PWM(pin)
        
        # Set Duty Cycle for Different Angles
        self.max_duty = 4300
        self.min_duty = 3550
        self.half_duty = 4000
        
        #Set PWM frequency
        self.pwm.freq(freq)
        
        #Make sure servo is dropped
        self.pwm.duty_u16(self.min_duty)
    
    #Servo to lift position
    def lift(self):
        self.pwm.duty_u16(self.max_duty)
    
    #Servo to drop position
    def drop (self):
        self.pwm.duty_u16(self.min_duty)
    
    #Servo to middle position
    def mid (self):
        self.pwm.duty_u16(self.half_duty)


