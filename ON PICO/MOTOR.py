from machine import Pin, PWM
from utime import sleep

class Motor:
 def __init__(self, dir, pwm):
     self.m1Dir = Pin(dir)
     self.pwm1 = PWM(Pin(pwm)) # set speed
     self.pwm1.freq(1000) # set max frequency
     self.pwm1.duty_u16(0) # set duty cycle
 
 def off(self):
     self.pwm1.duty_u16(0)
 
 def Forward(self, speed):
     self.m1Dir.value(0) # forward = 0 reverse = 1 motor 1
     self.pwm1.duty_u16(int(65535*speed/100)) # speed range 0-100 motor 1
     
 def Reverse(self, speed):
     self.m1Dir.value(1)
     self.pwm1.duty_u16(int(65535*speed/100))