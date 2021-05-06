import machine
import time
from mpu9250_new import MPU9250
from machine import I2C, Pin
from board import SDA, SCL

MPU9250._chip_id = 113 # new mpu9250
# Likely to be one of these: 115, 113, 104
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
imu = MPU9250(i2c)

def pvalues(Timer):

    print(imu.accel.xyz)
    print(imu.gyro.xyz)
    print(imu.mag.xyz)
    print(imu.temperature)
    print(imu.accel.z)
    print('')

tm = machine.Timer(1)
tm.init(period=2000, mode=tm.PERIODIC, callback=pvalues)
