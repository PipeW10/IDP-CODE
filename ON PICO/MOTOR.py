from machine import Pin, PWM

class Motor:
    def __init__(self, dirc, pwm):
        self.Dir = Pin(dirc, Pin.OUT)
        self.pwm = PWM(Pin(pwm)) # set speed
        self.pwm.freq(1000) # set max frequency
        self.pwm.duty_u16(0) # set duty cycle

        self.current_speed = 0

    def off(self):
        self.pwm.duty_u16(0)

    def Forward(self, speed):
        if self.current_speed != speed:
            self.Dir.value(0) # forward = 0 reverse = 1 motor 1
            self.pwm.duty_u16(int(65535*speed/100)) # speed range 0-100 motor 1
            self.current_speed = speed
     
    def Reverse(self, speed):
        if self.current_speed != -speed: #negative speed for reverse
            self.Dir.value(1)
            self.pwm.duty_u16(int(65535*speed/100))
            self.current_speed = -speed
