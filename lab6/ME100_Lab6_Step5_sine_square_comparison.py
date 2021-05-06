from board import LED
from machine import Pin, PWM, Timer, DAC
from time import sleep
import math

spkr_pin = Pin(26,Pin.OUT)
buf = bytearray(100)
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

spkr = DAC(spkr_pin,bits=12)
spkr.write_timed(buf, 5000, mode=DAC.CIRCULAR)

sleep(5)

#spkr.write_timed(buf, 5000, mode=DAC.NORMAL)
spkr_pin = Pin(26,Pin.OUT)

L1 = PWM(spkr_pin,freq=2500,duty=10,timer=0)
sleep(1)

for k in range(2,9):
    L1.duty(k*10)
    sleep(1)
