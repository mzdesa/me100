from mqttclient import MQTTClient
from math import sin
import network
import sys

from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import time

"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_host.py
session = 'madesa/ESP32/helloworld'
BROKER = 'mqtt.thingspeak.com'

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port=1883)
print("Connected!")

# send data
# In this sample, we send "fake" data. Replace this code to send useful data,
# e.g. measurement results.

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

r=0 #initialize r at 1000 so you can enter the loop
while r<800: #when load resistance exceeds 800 ohms, plot the data
    time.sleep(15) #code to print to the terminal every 0.3 seconds 
    i = ina.current()
    v = ina.voltage()
    p = ina.power()
    try:
        r = ina.voltage()/ina.current()*1000
    except ZeroDivisionError:
        r = 0 #use zero to avoid an error with the while loop condition

    topic = "channels/1328293/publish/BPTY5PBP9TJGQ5L5".format(session)
    data = "field1={}&field2={}".format(v, i)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()