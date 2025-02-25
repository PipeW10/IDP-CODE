from machine import Pin, PWM
from utime import sleep
from MOTOR import Motor


motor=Motor()

while True:
 motor.Forward()
 sleep(1)
 motor.Reverse()
 sleep(1)