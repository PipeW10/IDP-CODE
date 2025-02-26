from machine import Pin, PWM
from utime import sleep

class Motor:
 def __init__(self, dir, pwm):
     self.Dir = Pin(dir)
     self.pwm = PWM(Pin(pwm)) # set speed
     self.pwm.freq(1000) # set max frequency
     self.pwm.duty_u16(0) # set duty cycle
 
 def off(self):
     self.pwm.duty_u16(0)
 
 def Forward(self, speed):
     self.Dir.value(0) # forward = 0 reverse = 1 motor 1
     self.pwm.duty_u16(int(65535*speed/100)) # speed range 0-100 motor 1
     
 def Reverse(self, speed):
     self.Dir.value(1)
     self.pwm.duty_u16(int(65535*speed/100))