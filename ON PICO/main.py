from machine import Pin, PWM
from utime import sleep
from MOTOR import Motor


motorL = Motor(4,5)
motorR = Motor(6,7)

while True:
 motor.Forward()
 sleep(1)
 motor.Reverse()
 sleep(1)