from board import LED
from machine import Pin
import time

#initialize the GPIO pin number 14, store it in the variable pin_14
pin_14 = Pin(14, mode = Pin.OUT)
#cycle the square wave 300 times
i = 0 #counter variable
t = 0.002 #time to hold an output for
while i<3000:
    pin_14(1) #hold at a high value for t seconds
    time.sleep(t)
    pin_14(0)
    time.sleep(t) #hold at a low value for t seconds
    i+=1
