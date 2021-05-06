from machine import Pin, PWM, Timer
import time
import math

class Servo:
    def __init__(self, spin, frq):
        self.servoPin = Pin(spin, Pin.OUT) #define the servo pin
        self.pwmPin = PWM(self.servoPin, freq = frq) #define the pin as a pwm pin with frequency frq
        self.angle = 0 #starting angle of the servo
    
    def set_angle(self, theta):
        duty_input = math.floor((100/180)*theta) #maps theta to an integer duty

        for i in range(0,duty_input):
            self.pwmPin.duty(i)
            time.sleep_ms(20)

        self.angle = math.floor((180/100)*duty_input) #update the angle of the arm

servoPin = 27
servoFreq = 50

#define servo object
s1 = Servo(servoPin, servoFreq)
s1.set_angle(100)