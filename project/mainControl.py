"""
Run the operations of all the different motors
Check if the button has been pressed
Record the position in space in an array
Send the array back to the user
"""
#stepper driver libraries
from machine import Pin, PWM, Timer, I2C
from board import SDA, SCL
from board import LED
from mpu9250_new import MPU9250
import time
import math

#mqtt libraries
from mqttclient import MQTTClient
import network
import sys

#set up MPU to be used at a later point
MPU9250._chip_id = 113
# 115, 113, 104
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
imu = MPU9250(i2c)

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


#Servo Class - Allows for expansion to an additional servo motor if the user wishes
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
#global mode
#mode = "normal" #mode can be either normal or cmm

class Axis:
    """
    class for each axis of the stepper. It takes in an array of the motors that drive that axis.
    """
    def __init__(self, arr_motors, lth, sensor_name, ra, mod):
        self.motors = arr_motors
        self.angle = arr_motors[0].pos #initialize the angle of the arm as zero
        self.length = lth #length of the arm
        self.sensName = sensor_name #name of the sensor object that gives the angle of the arm
        self.ratio = ra #gear ratio from the stepper to the arm
        self.mode = mod #holds the drive mode (cmm, normal) of the arm

    def drive(self, cnt, direc):
        """
        function to drive a single motor arm
        """
        if self.mode == "normal":
            self.motors[0].step(cnt,direc)
            #print("normal")
            #now, update the angle of the arm - each step is 1.8 degrees (NEMA 17 and 11 standard)
            if direc == 1:
                self.angle = self.angle+cnt*1.8*self.ratio
            elif direc == 0:
                self.angle = self.angle-cnt*1.8*self.ratio
            else:
                print('invalid direction - must be 0 or 1')
        else:
            #cmm mode movement - do one step at a time - if the switch is high, stop and publish position data
            sense = Pin(21, Pin.IN)
            for i in range(cnt):
                if sense.value() == 0: #when the pin reads 0, the sensor is depressed!
                    mqtt.publish(feedName, position())
                    self.motors[0].reset() #reset the stepper so it stops driving
                    time.sleep(1) #sleep for 5 seconds after readjusting from point
                    #now step it backwards in the opposite direction to stop it from continually sending the point
                    print(sense.value())
                    if direc == 1:
                        self.motors[0].step(50, 0) #if the stepping directiosn was 1, to move it back, go 50 steps in the zero direction
                        self.angle -= 50*1.8 #readjust the angle
                    else:
                        self.motors[0].step(50,1)
                        self.angle += 50*1.8
                    break #break out of the for loop (stop driving!)
                else:
                    #if switch is at 1, complete one step
                    self.motors[0].step(1, direc)
                    print(sense.value())
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
        
        if self.mode == "normal":
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
                if sense.value() == 0:
                    mqtt.publish(feedName, position())
                    #now, step in the opposite direction
                    if direction == 1:
                        self.motors[0].dirPin.value(0)
                        self.motors[1].dirPin.value(1) #switch the direction
                        for i in range(50): #step backwards 50
                            self.motors[0].stepPin.value(1)
                            self.motors[1].stepPin.value(1)
                            time.sleep_us(self.motors[1].delay)
                        self.motors[0].pos -= 50 #subtract 50 steos
                        self.motors[1].pos += 50
                    else:
                        self.motors[0].dirPin.value(1)
                        self.motors[1].dirPin.value(0) #switch the direction
                        for i in range(50): #step backwards 50
                            self.motors[0].stepPin.value(1)
                            self.motors[1].stepPin.value(1)
                            time.sleep_us(self.motors[1].delay)
                        self.motors[0].pos += 50 #add 50 steps
                        self.motors[1].pos -= 50
                else:
                    #if switch is zero, complete one step
                    self.motors[0].stepPin.value(1)
                    self.motors[1].stepPin.value(1)
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

#note: ratio is the ratio of the input to the output gears
#base (axis 1)
delay = 1000
s1 = Stepper(15, 27, delay) #define base stepper motor
a1 = Axis([s1],0, '', 12.21/120, "normal")
#arm 1 (axis 2)
s2 = Stepper(32, 14, delay) #define arm1 stepper motor1
a2 = Axis([s2], 0.15, '', 12.21/60, "normal")
#arm 2 (axis 3)
s3 = Stepper(17, 16, delay) #define arm1 stepper motor2
a3 = Axis([s3], 0.2, '', 12.21/40, "normal")
#arm 3 (axis 4 - rotational only)
s4 = Stepper(4, 13, 500) #define arm 3 rotation stepper motor
a4 = Axis([s4], 0, '', 1, "normal") #note the 1:1 ratio from the direct coupling

def position():
    """
    function that takes in no arguments and returns the position of the endpoint
    """
    p1 = [a2.length*math.sin(math.radians(a2.angle)), a2.length*math.cos(math.radians(a2.angle))] #calculate the position of the 1st endpoint, unrotated
    r_1 = a2.length*math.sin(math.radians(a2.angle))+a3.length*math.cos(math.radians(a3.angle))*math.sin(math.radians(a2.angle))+a3.length*math.sin(math.radians(a3.angle))*math.cos(math.radians(a2.angle))
    r_2 = a2.length*math.cos(math.radians(a2.angle))+a3.length*math.cos(math.radians(a3.angle))*math.cos(math.radians(a2.angle))-a3.length*math.sin(math.radians(a3.angle))*math.sin(math.radians(a2.angle))
    r = [r_1, r_2, 0] #un-base rotated r vector #note that the j axis is vertical position
    #now, rotate the vector
    r = [r[0]*math.cos(math.radians(a1.angle)), r_2, r[0]*math.sin(math.radians(a1.angle))]
    r = str(r)
    return r #return r as a string!

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
adafruitAioKey = 'KEY'

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

    elif "mode" in cmnd:
        #recognizes commands of the form 'mode(cmm)'
        if "cmm" in cmnd:
            a1.mode = "cmm" #reset the mode variable to cmm
            a2.mode = "cmm"
            a3.mode = "cmm"
            #a4.mode = "cmm"
        else:
            a1.mode = "normal"
            a2.mode = "normal"
            a3.mode = "normal"
            #a1.mode = "normal"
    
    elif "imu" in cmnd: #if the command to read IMU data at a certain point in time is received, then send the IMU data to the user
        x_array_data = [imu.accel.x, imu.accel.y, imu.accel.z, imu.gyro.x, imu.gyr0.y, imu.gyro.z]
        mqtt.publish(feedName, x_array_data)
        print("imu")
    
    elif "Robot" in cmnd:
        print("Welcome") #recognizes the first time connection of the robot and avoids sending error message!

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
for i in range(600): #Runs the robot for a ten minute session
    mqtt.check_msg() #uses a callback function to limit the time the program runs (see inf. running commented out above)
    time.sleep(1)