from machine import Pin
import time

#initialize pins
dirPin = Pin(27,Pin.OUT)
stepPin = Pin(15,Pin.OUT)

period = 0.0005
steps = 200

#loop
#i = 0
#while i<1:
dirPin.value(1)

step_counter = 0
while step_counter<steps:
    stepPin.value(1)
    time.sleep(period)
    stepPin.value(0)
    time.sleep(period)     

    step_counter +=1 
step_counter = 0 #reset step counter

time.sleep(0.5)

dirPin.value(0) #change direction


while step_counter<steps:
    stepPin.value(1)
    time.sleep(period)
    stepPin.value(0)
    time.sleep(period)
    step_counter+=1
step_counter = 0 #reset step counter

time.sleep(0.5)

#i+=1



