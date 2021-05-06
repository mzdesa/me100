"""
Run the operations of all the different motors
Check if the button has been pressed
Record the position in space in an array
Send the array back to the user
"""
#stepper driver libraries
from machine import Pin, PWM, Timer
import time
import math

#mqtt libraries
from mqttclient import MQTTClient
import network
import sys


#Stepper Class
class Stepper:
    def __init__(self, spin, dpin, dly):
        self.stepPin = Pin(spin,Pin.OUT) #stepper step pin number
        self.dirPin = Pin(dpin,Pin.OUT) #stepper direction pin number
        self.delay = dly
        self.pos = 0 #initialize the position of the stepper as "zero - homing position!"

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

        #update the position of the stepper relative to where it started
        if direction == 0:
            self.pos == self.pos - count
        elif direction == 1:
            self.pos == self.pos + count
        else:
            print("Direction must be either 0 (backwards) or 1 (forwards)")

    def reset(self):
        """
        function to reset stepper pins to zero - note that delay is unchanged
        """
        #pin resets
        self.dirPin.value(0)
        self.stepPin.value(0)


#Servo Class
class Servo:
    def __init__(self, spin, frq):
        self.servoPin = Pin(spin, Pin.OUT) #define the servo pin
        self.pwmPin = machine.PWM(self.servoPin, freq = frq) #define the pin as a pwm pin with frequency frq
        self.angle = 0 #starting angle of the servo
    
    def angle(self, theta):
        duty_input = math.floor((100/180)*theta) #maps theta to an integer duty
        self.pwmPin.duty(duty_input)
        self.angle = math.floor((180/100)*duty_input) #update the angle of the arm

#define functions for the arm 

class Axis:
    """
    class for each axis of the stepper. It takes in an array of the motors that drive that axis.
    """
    def __init__(self, arr_motors, lth, sensor_name, ra):
        self.motors = arr_motors
        self.angle = arr_motors[0].pos #initialize the angle of the arm as zero
        self.length = lth #length of the arm
        self.sensName = sensor_name #name of the sensor object that gives the angle of the arm
        self.ratio = ra #gear ratio from the stepper to the arm

    def drive(self, cnt, direc):
        """
        function to drive a single motor arm
        """
        if mode == "normal":
            self.motors[0].step(cnt,direc)
            #now, update the angle of the arm - each step is 1.8 degrees (NEMA 17 and 11 standard)
            if direc == 1:
                self.angle = self.angle+cnt*1.8*self.ratio
            elif direc == 0:
                self.angle = self.angle-cnt*1.8*self.ratio
            else:
                print('invalid direction - must be 0 or 1')
        else:
            #cmm mode movement - do one step at a time - if the switch is high, stop and publish position data
            for i in range(cnt):
                if switch == 1:
                    mqtt.publish(feedName, position())
                else:
                    #if switch is zero, complete one step
                    self.motors[0].step(1, direc)
                    if direc == 1:
                        self.angle = self.angle+1*1.8*self.ratio
                    elif direc == 0:
                        self.angle = self.angle-1*1.8*self.ratio
                    else:
                        print('invalid direction - must be 0 or 1')

    def dual_drive(self, count, direction):
        """
        function to drive two motors synchronously
        assume that the two motors to drive are the first two in the array!
        """
        #first, synchronize the delay and position values of each (if they haven't already been synced!)
        self.motors[1].delay = self.motors[0].delay
        self.motors[1].pos = self.motors[0].pos

        #set the directions of both stepper motors
        self.motors[0].dirPin.value(direction) #enable the motor to move in a particular direction
        #tell the 2nd motor to move in the opposite direction so rotation is smooth (due to symmetry)
        if direction == 1:
            self.motors[1].dirPin.value(0)
        else:
            self.motors[1].dirPin.value(1)
        
        if mode == "normal":
            for i in range(count): #do a count number of "steps" of the motor
                self.motors[0].stepPin.value(1)
                self.motors[1].stepPin.value(1)

                time.sleep_us(self.motors[1].delay) #continue this command for the delay period

                self.motors[0].stepPin.value(0) #switch the steppers off
                self.motors[1].stepPin.value(0)
                time.sleep_us(self.motors[1].delay)

            #update the position of the stepper relative to where it started
            if direction == 0:
                self.motors[0].pos == self.motors[0].pos - count
                self.motors[1].pos == self.motors[1].pos - count
                self.angle = self.angle-count*1.8*self.ratio
            elif direction == 1:
                self.motors[0].pos == self.motors[0].pos + count
                self.motors[1].pos == self.motors[1].pos + count
                self.angle = self.angle+count*1.8*self.ratio
            else:
                print("Direction must be either 0 (backwards) or 1 (forwards)")
        else:
            #CMM mode operation
            for i in range(count):
                if switch == 1:
                    mqtt.publish(feedName, position())
                else:
                    #if switch is zero, complete one step
                    self.motors[0].step(1, direction)
                    self.motors[1].step(2,direction)
                    if direction == 1:
                        self.angle = self.angle+1*1.8*self.ratio
                        self.motors[0].pos == self.motors[0].pos + 1
                        self.motors[1].pos == self.motors[1].pos + 1
                    elif direction == 0:
                        self.angle = self.angle-1*1.8*self.ratio
                        self.motors[0].pos == self.motors[0].pos - 1
                        self.motors[1].pos == self.motors[1].pos - 1
                    else:
                        print('invalid direction - must be 0 or 1')

    def reset(self):
        #function to reset the arm position
        a1.angle = 0

#PREDEFINE ALL STEPPER NAMES FOR THE USER
global mode
mode = "normal" #mode can be either normal or cmm

global switch
switch = 0 #if switch is off, it's not being depressed, if on, it is

#note: ratio is the ratio of the input to the output
#base (axis 1)
delay = 1000
s1 = Stepper(15, 27, delay) #define base stepper motor
a1 = Axis([s1],0, '', 12.21/120)
#arm 1 (axis 2)
s2 = Stepper(32, 14, delay) #define arm1 stepper motor1
a2 = Axis([s2], 0.15, '', 12.21/60)
#arm 2 (axis 3)
s3 = Stepper(17, 16, delay) #define arm1 stepper motor2
a3 = Axis([s3], 0.2, '', 12.21/40)
#arm 3 (axis 4 - rotational only)
#s4 = Stepper(stepperPin, directionPin, stepDelay) #define arm 3 rotation stepper motor
#a3 = Axis([s4], 0, '', 1) #note the 1:1 ratio from the direct coupling

def position():
    """
    function that takes in no arguments and returns the position of the endpoint
    """
    position = str([0,0,0])
    return position

#Internet Connectivity
# Check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'mzdesa'
adafruitAioKey = 'aio_GJdP223W6wRRDsxKpaderIj1SLaE'

# Define callback function - should edit THIS!!! See: https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_sub_led.py
def sub_cb(topic, msg):
    cmnd = msg.decode() #decode the message into a string
    if cmnd[0:8] == "a1.drive":
        #find the number of steps
        num = ''
        for c in cmnd[2:]:
            if c.isdigit():
                num = num+c
        direc = int(num[-1])#the last number will be the direction
        num = int(num[0:-1]) #the rest of the number will be the number of steps
        print(direc)
        print(num)
        #drive the motor
        a1.drive(num,direc)

    elif cmnd[0:8] == "a2.drive":
        #find the number of steps
        num = ''
        for c in cmnd[2:]:
            if c.isdigit():
                num = num+c
        direc = int(num[-1])#the last number will be the direction
        num = int(num[0:-1]) #the rest of the number will be the number of steps
        #drive the motor
        a2.drive(num,direc)

    elif cmnd[0:8] == "a3.drive":
        #find the number of steps
        num = ''
        for c in cmnd[2:]:
            if c.isdigit():
                num = num+c
        direc = int(num[-1])#the last number will be the direction
        num = int(num[0:-1]) #the rest of the number will be the number of steps
        #drive the motor
        a3.drive(num,direc)

    elif cmnd[0:8] == "a4.drive":
        #find the number of steps
        num = ''
        for c in cmnd[2:]:
            if c.isdigit():
                num = num+c
        direc = int(num[-1])#the last number will be the direction
        num = int(num[0:-1]) #the rest of the number will be the number of steps
        #drive the motor
        a4.drive(num,direc)

    elif cmnd[2:] == "reset":
        #reset motor
        if cmnd[0:2]=="a1":
            a1.reset()
        if cmnd[0:2]=="a2":
            a2.reset()
        if cmnd[0:2]=="a3":
            a3.reset()
        if cmnd[0:2]=="a4":
            a4.reset()
    
    elif cmnd == "position":
        #publish the position of the endpoint
        pos = position()
        mqtt.publish(feedName, pos)

    elif cmnd[0:4] == "mode":
        #recognizes commands of the form 'mode(cmm)'
        if "cmm" in cmnd:
            mode = "cmm"
        else:
            mode = "normal"
    #add a command for "robot connected" being the message
    else:
        print("Error, Command Not Recognized")
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

# Send test message
global feedName
feedName = "mzdesa/feeds/me100project"
testMessage = "Robot Connected!"
# testMessage = "1"
mqtt.publish(feedName,testMessage)
print("Published {} to {}.".format(testMessage,feedName))

mqtt.subscribe(feedName)

#The following will be the "LOOP" section (analogous to arduino)
for i in range(60): #read messages from Adafruit IO for 10 seconds
    mqtt.check_msg() #uses a callback function to limit the time the program runs (see inf. running commented out above)
    #print(x) - x ISN'T actually storing it!
    time.sleep(1)