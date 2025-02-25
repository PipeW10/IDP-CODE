from machine import ADC, Pin, PWM
from machine import I2C
from tcs34725 import TCS34725
from time import sleep_ms

# Pin 0  PWM Motor 1               Ground---[]              []-------------------------------
# Pin 1  DIR Motor 1               Ground---[]              []------                     ----3V3
#                                  Ground---[]              []------                     ----Ground
# Pin 2  PWM Motor 2               Ground---[]              []-------------------------------
# Pin 3  DIR Motor 2               Ground---[]              []-------------------------------
# Pin 4  PWM Motor 3 or Servo 1    Ground---[]              []-------------------------------
# Pin 5  DIR Motor 3               Ground---[]              []-------------------------------
#                                  Ground...[]              []-------------------------------
# Pin 6  PWM Motor 4 or Servo 2    Ground---[]              []-------------------------------
# Pin 7  DIR Motor 4               Ground---[]              []-------------------------------
# Pin 8  GPIO...............................[]              []-------------------------------
# Pin 9  GPIO...............................[]              []-------------------------------
#                                  Ground                   []-------------------------------Ground
# Pin 10 GPIO...............................[]              []-------------------------------
# Pin 11 GPIO...............................[]              []-------------------------------Pin 20 GPIO
# Pin 12 GPIO...............................[]              []-------------------------------Pin 19 GPIO
# Pin 13 GPIO............... ..       ......[]              []-------------------------------Pin 18 GPIO
# Ground....................................[]              []-------------------------------Ground
# Pin 14 GPIO...............................[]              []-------------------------------Pin 17 GPIO
# Pin 15 GPIO...............................[]              []-------------------------------Pin 16 GPIO

#Led pin
led = Pin(14, Pin.OUT)

#Colour Sensor
i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)

print('raw: {}'.format(tcs.read('raw')))

print('rgb: {}'.format(tcs.read('rgb')))

#Motor 
motorL = PWM(Pin(0), freq = 0, duty_u16=32768)
motorL.freq(100)
