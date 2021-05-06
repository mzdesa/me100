from board import LED
import time
from machine import Pin, PWM, Timer
import math

#initialize built in LED pin
led = Pin(27, mode = Pin.OUT)
#i = 0
#while i<20:
#    led(1)
#    time.sleep(1)
#    led(0)
#    time.sleep(1)
#    i+=1

bach = [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247, 262, 277, 294, 311, 330, 349, 370, 370, 392, 415, 440, 466, 494, 523, 554, 587, 622, 659, 698, 740, 784, 831, 880, 932, 988, 1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976, 2093, 2217, 2349, 2489, 2637, 2794, 2960, 3136, 3322, 3520, 3729, 3951, 4186, 4435, 4699, 4978]

L1 = PWM(led, freq = 500, duty = 50, timer = 0)

for i in range(0, len(bach)):
    L1.freq(bach[i])