from machine import I2C, Pin
import time

# I2C0: GP0=SDA, GP1=SCL
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)

print("I2C scan:", i2c.scan())  # Verwacht [0x28] of [0x29]

# Test of hij reageert
if 0x28 in i2c.scan():
    print("BNO055 gevonden op adres 0x28")
else:
    print("Geen BNO055 gevonden")
