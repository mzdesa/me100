import umqtt1
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
myMqttClient = "TestClient"
adafruitIoUrl = "io.adafruit.com"
adafruitUsername = "mzdesa"
adafruitAioKey = "aio_GJdP223W6wRRDsxKpaderIj1SLaE"

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = umqtt1.MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
time.sleep(0.5)
mqtt.connect()
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)
mqtt.subscribe(feedName)

# Send test message
feedName = "mzdesa/feeds/myfeed"
testMessage = "Hello Adafruit World"
# testMessage = "1"
mqtt.publish(feedName,testMessage)
print("Published {} to {}.".format(testMessage,feedName))

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
for i in range(0, 60):
    mqtt.check_msg()
    time.sleep(1)

mqtt.disconnect();
