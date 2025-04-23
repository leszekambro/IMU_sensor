# -*- coding: utf-8 -*-
import smbus
import time

bus = smbus.SMBus(3)  # <-- i2c-3
address = 0x68

# Rejestry MPU6050
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

def read_raw_data(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value

# Inicjalizacja MPU6050
bus.write_byte_data(address, 0x6B, 0)

print "Reading data from MPU6050 and logging to file..."

# Otwórz plik do dopisywania danych
with open("imu_log.txt", "a") as logfile:
    logfile.write("timestamp,Ax,Ay,Az,Gx,Gy,Gz\n")  # nagłówki

    while True:
        timestamp = time.time()  # znacznik czasu UNIX (sekundy)

        # Akcelerometr
        ax = read_raw_data(ACCEL_XOUT_H)
        ay = read_raw_data(ACCEL_XOUT_H + 2)
        az = read_raw_data(ACCEL_XOUT_H + 4)

        # Żyroskop
        gx = read_raw_data(GYRO_XOUT_H)
        gy = read_raw_data(GYRO_XOUT_H + 2)
        gz = read_raw_data(GYRO_XOUT_H + 4)

        # Przelicz na jednostki fizyczne
        Ax = ax / 16384.0
        Ay = ay / 16384.0
        Az = az / 16384.0

        Gx = gx / 131.0
        Gy = gy / 131.0
        Gz = gz / 131.0

        # Wyświetl dane
        print "Accel [g]:  X=%.2f  Y=%.2f  Z=%.2f" % (Ax, Ay, Az)
        print "Gyro  [deg/s]: X=%.2f  Y=%.2f  Z=%.2f" % (Gx, Gy, Gz)
        print "-" * 50

        # Zapisz do pliku
        logfile.write("%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n" % (
            timestamp, Ax, Ay, Az, Gx, Gy, Gz
        ))
        logfile.flush()

        time.sleep(1)
