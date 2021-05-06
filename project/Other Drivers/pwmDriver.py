from machine import Pin, PWM, Timer
import time

dirPin = Pin(27, Pin.OUT)
dirPin.value(1)
stepPin = Pin(15, Pin.OUT)
s1 = PWM(stepPin, freq = 1000, duty = 50) #write high for half, write low for the other half
