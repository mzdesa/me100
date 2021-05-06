import machine
import time

capsense0 = machine.TouchPad(machine.Pin(12))
capsense1 = machine.TouchPad(machine.Pin(15))

while True:
    csval0 = capsense0.read()
    csval1 = capsense1.read()
    print("CapSense0: '{}', CapSense1: '{}'".format(csval0,csval1))
    time.sleep(0.1)

    
