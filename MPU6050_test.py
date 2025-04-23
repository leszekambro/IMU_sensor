import smbus
import time

bus = smbus.SMBus(3)  # <- I2C-3
address = 0x68        # <- Adres MPU6050

try:
    bus.write_byte_data(address, 0x6B, 0)  # Wake up MPU6050
    print("MPU6050 initialized successfully!")
except IOError as e:
    print("I/O Error:", e)

