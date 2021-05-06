import machine
import math

# Set up the two DAC pins
d = machine.DAC(machine.Pin(25,machine.Pin.OUT),bits=12)
d1 = machine.DAC(machine.Pin(26,machine.Pin.OUT),bits=12)

# To write a constant value, use, e.g.:
# d.write(200)

# Create buffers for the two modulated sine-waves
buf = bytearray(5000)
buf1 = bytearray(5000)

# Assign modulated sine wave, with modulating signal 50x slower than carrier frequency
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * 50 * i / len(buf)) * (0.5 + 0.5 * math.sin(2 * math.pi * i / len(buf))))
    buf1[i] = 128 + int(127 * math.cos(2 * math.pi * 50 * i / len(buf)) * (0.5 + 0.5 * math.sin(2 * math.pi * i / len(buf))))

# Sequentially output the values in the two buffers. Results in a carrier frequency of about
# 100 Hz.
for k in range(10000):
    for i in range(len(buf)):
        d.write(buf[i])
        d1.write(buf1[i])

# The below syntax will alternatively write the byte array to the DAC pin much more quickly (up to a rate of 500 kHz) but
# seems unable to output on both pins simultaneously at higher frequencies and unable to find a way
# to sync the two outputs in order to be able to use the difference between them.
# Second argument is the rate (Hz) of writing bytes to the DAC pin.
# d.write_timed(buf, 5000, mode=machine.DAC.CIRCULAR)
