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
stepDelay = 1000

s1 = Stepper(stepperPin, directionPin, stepDelay) #create an instance of the stepper class with the above variables

#MQTT Control
from mqttclient import MQTTClient
import network
import sys
import time

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
adafruitAioKey = 'aio_aAiC902MP1gJ5ZN4HhyUHqnTREr5'

# Define callback function - should edit THIS!!!
def sub_cb(topic, msg):
    #if msg.decode() == "hey":
    #    #print(type(msg.decode())) #decode the byte array (converts it to a string)
    #    print(1)
    #else:
    #    print(0)
    #print((topic, msg))

    cmnd = msg.decode() #decode the message into a string
    if cmnd[0:8] == "s1.drive":
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
        s1.step(num, direc)
    else:
        print(0)

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

# Send test message
feedName = "mzdesa/feeds/me100project"
testMessage = "Robot Connected!"
# testMessage = "1"
mqtt.publish(feedName,testMessage)
print("Published {} to {}.".format(testMessage,feedName))

mqtt.subscribe(feedName)

#The following will be the "LOOP" section (analogous to arduino)
for i in range(10): #read messages from Adafruit IO for 10 seconds
    mqtt.check_msg() #uses a callback function to limit the time the program runs (see inf. running commented out above)
    #print(x) - x ISN'T actually storing it!
    time.sleep(1)

