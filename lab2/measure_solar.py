from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import time

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

while True:
    ''' Insert your code here to read and print voltage, current, and power from ina219. '''
    time.sleep(0.5) #code to print to the terminal every 0.5 seconds 
    #note: the end argument in the print function prints all the lines on the same line - separate print statements are used for easier organization
    print("Current:", ina.current(), "mA", end = ' | ')
    print("Voltage:", ina.voltage(), "V", end = ' | ')
    #code to avoid a divide by zero error in the calculation of resistance
    try:
        print("Resistance:", (ina.voltage()/ina.current())*1000, "Ohms", end = ' | ')#note the conversion factor to give units of ohms
    except ZeroDivisionError:
        print("Resistance: ", 'NaN', "Ohms", end = ' | ')
        
    print("Power:", ina.voltage()*ina.current(), "mW") #don't use optional argument end such that the next set is printed on a new line