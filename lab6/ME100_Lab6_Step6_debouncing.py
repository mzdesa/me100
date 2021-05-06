from board import A9, LED
from machine import Pin
import time

# Set up the pin in pull-up mode, so that a simple pushbutton can be used.
# when pressed, the pin is shorted to ground. When released, the internal
# pull-up resistor makes the input effectively high.
p = Pin(A9, mode=Pin.IN, pull=Pin.PULL_UP)

# Use the board LED for output
led = Pin(LED,mode=Pin.OUT)

counter = 0
last_state = 0
last_time = time.ticks_ms()

while True:
    # Read value on input pin
    state = p()

    # Compute time delta_t since last time the output changed
    t = time.ticks_ms()
    delta_t = t - last_time

    # Execute if more than 20 ms have elapsed since last output change and the current
    # input differs from the current output (XOR, ^, function is used)
    if delta_t > 20 and state^last_state:
        last_time = t
        counter += 1
        last_state = state

    # Update output to LED
    if last_state:
        led(1)
    else:
        led(0)
