from machine import Pin
import time

#define the drive and step pin numbers
#stepPin = 19
#dirPin = 20

#stepPin = Pin(19,Pin.OUT)
#dirPin = Pin(20,Pin.OUT)
class Stepper:
    def __init__(self, spin, dpin, dly):
        self.stepPin = Pin(spin,Pin.OUT) #stepper step pin number
        self.dirPin = Pin(dpin,Pin.OUT) #stepper direction pin number
        self.delay = dly
    def step(self, count, direction):
        """
        self passes in the instance of the stepper motor
        count is the number of steps
        direction is either a 1 (forward) or a 0 (backward)
        """
        self.dirPin.value(direction) #enable the motor to move in a particular direction
        
        for i in range(count): #do 200 "steps" of the motor
            self.stepPin.value(1)
            time.sleep_us(self.delay) #continue this command for the delay period

            self.stepPin.value(0) #switch the stepper off
            time.sleep_us(self.delay) 

#create an instance of the stepper class
stepperPin = 15
directionPin = 27
stepDelay = 500

s1 = Stepper(stepperPin, directionPin, stepDelay) #create an instance of the stepper class with the above variables

stepperPin2 = 32
directionPin2 = 14
stepDelay2 = 1000
s2 = Stepper(stepperPin2, directionPin2, stepDelay2)

s3 = Stepper(17, 16, stepDelay)

#s1.step(200,1) #move 200 steps forward
#s2.step(50,1)

