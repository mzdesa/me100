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

# Define callback function - should edit THIS!!! See: https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_sub_led.py
def sub_cb(topic, msg):
    #if msg.decode() == "hey":
    #    #print(type(msg.decode())) #decode the byte array (converts it to a string)
    #    print(1)
    #else:
    #    print(0)
    #print((topic, msg))

    cmnd = msg.decode() #decode the message into a string
    if cmnd[0:8] == "a1.drive":
        #find the number of steps
        num = ''
        for c in cmnd[2:]:
            if c.isdigit():
                num = num+c
        direc = num[-1]#the last number will be the direction
        num = num[0:-1] #the rest of the number will be the number of steps
        print("direction" + direc)
        print("number of steps" + num)
        #drive the motor
        #a1.drive(num, dir)
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