from board import LED
from machine import Pin
import time

#initialize built in LED pin
led = Pin(LED, mode = Pin.OUT)
i = 0
while i<20:
    led(1)
    time.sleep(1)
    led(0)
    time.sleep(1)
    i+=1
