from machine import Pin
import time

sense = Pin(21, Pin.IN) #can be any GPIO pin
#for ten seconds, print out the value read by the pin
#note: circuit uses a pull-up resistor!
for i in range(10):
    print(sense.value())
    #print(type(sense.value())) #sense.value() returns an integer
    time.sleep(1) #the pin is HIGH (1) when the button is not depressed and LOW (0) when the button is depressed