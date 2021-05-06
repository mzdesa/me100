from mqttclient import MQTTClient
from math import sin
import network
import sys

"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_host.py
session = 'madesa/ESP32/helloworld'
BROKER = 'broker.mqttdashboard.com'

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
for t in range(100):
    s = sin(t/10)
    # add additional values as required by application
    topic = "{}/data".format(session)
    data = "{},{}".format(t, s)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()