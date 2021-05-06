import paho.mqtt.client as paho
import matplotlib.pyplot as plt

"""
Get measurement results from microphyton board and plot on host computer.
Use in combination with mqtt_plot_mpy.py.

Install paho MQTT client and matplotlib on host, e.g.
    $ pip install paho-mqtt
    $ pip install matplotlib

Start this program first on the host from a terminal prompt, e.g.
    $ python mqtt_plot_host.py
then run mqtt_plot_mpy.py on the ESP32.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_mpy.py
session = 'madesa/ESP32/helloworld'
BROKER = 'broker.mqttdashboard.com'
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# initialize data vectors
# in this example we plot only 1 value, add more as needed
i = []
v = []
p = []
r = []

# mqtt callbacks
def data(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    v.append(f[0])
    i.append(f[1])
    p.append(f[2])
    r.append(f[3])

def plot(client, userdata, message):
    # customize this to match your data
    print("plotting ...")
    plt.plot(r, p, 'rs')
    plt.xlabel('Resistance')
    plt.ylabel('Power')
    print("show plot ...")
    # show plot on screen
    plt.show()

# subscribe to topics
data_topic = "{}/data".format(session, qos)
plot_topic = "{}/plot".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.subscribe(plot_topic)
mqtt.message_callback_add(data_topic, data)
mqtt.message_callback_add(plot_topic, plot)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()
