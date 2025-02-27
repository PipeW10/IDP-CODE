from machine import Pin
from machine import I2C
from tcs34725 import TCS34725
from time import sleep_ms

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)

#Define colours

def readColour (self):
    red = None
    blue = None
    green = None
    yellow = None
    raw  = tcs.read('raw')
    rgb = tcs.read('rgb')
    
tcs = TCS34725(I2C(0, sda=Pin(16), scl=Pin(17)))


print('raw: {}'.format(tcs.read(raw = false)))

print('rgb: {}'.format(tcs.read('rgb')))
