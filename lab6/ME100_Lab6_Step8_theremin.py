import machine
import time
import math

capsense0 = machine.TouchPad(machine.Pin(12))
capsense1 = machine.TouchPad(machine.Pin(15))
spkr_pin = machine.Pin(26,machine.Pin.OUT)

# Sine wave
buf = bytearray(100)
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

freq_tone = 500
duty_tone = 0.5
L1 = machine.PWM(spkr_pin,freq=freq_tone,duty=duty_tone,timer=0)

while True:
    csval0 = capsense0.read()
    csval1 = capsense1.read()
    f=int(500*1000/csval1)
    print("CapSense0: '{}', CapSense1: '{}', freq: '{}'".format(csval0,csval1,f))
    time.sleep(0.01)
    L1.freq(f)
