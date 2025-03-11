from machine import Pin, PWM
from utime import sleep
from MOTOR import Motor
from SERVO import Servo


motorL = Motor(4,5)
motorR = Motor(6,7)
fork = Servo(pin = 15, freq = 50)


