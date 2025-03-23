from machine import Pin, PWM

class Motor:
    def __init__(self, dirc, pwm):
        self.Dir = Pin(dirc, Pin.OUT)
        self.pwm = PWM(Pin(pwm)) # set speed
        self.pwm.freq(1000) # set max frequency
        self.pwm.duty_u16(0) # set duty cycle

        self.current_speed = 0

    #Turns the motor off
    def off(self):
        self.pwm.duty_u16(0)
        self.current_speed = 0

    def Forward(self, speed):
        if self.current_speed != speed:
            self.Dir.value(0) #Forward = 0
            self.pwm.duty_u16(int(65535*speed/100)) #Speed range 0-100
            #Update current speed
            self.current_speed = speed
     
    def Reverse(self, speed):
        #Negative speed for reverse
        if self.current_speed != -speed: 
            self.Dir.value(1) #Reverse = 1
            self.pwm.duty_u16(int(65535*speed/100)) #Speed range 0-100
            #Update current speed
            self.current_speed = -speed


