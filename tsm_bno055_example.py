# Simple test program for MicroPython bno055 driver

import machine
import time
import neopixel
from bno055 import *
from scheduler import Scheduler, Task

i2c = machine.SoftI2C(scl=machine.Pin(9), sda=machine.Pin(8), freq=100000, timeout=1000000)
onboard_led = machine.Pin(25, machine.Pin.OUT)
rgb_led_pin = machine.Pin(18, machine.Pin.OUT)
virt_gnd = machine.Pin(17, machine.Pin.OUT)
virt_gnd.value(False)
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
rgb_led = neopixel.NeoPixel(machine.Pin(rgb_led_pin), 1)

rgb_led[0] = (0, 0, 0)  
rgb_led.write()
print("TSM test program!")
time.sleep_ms(200)  # wacht extra tijd voor sensorstart
print("I2C scan:", i2c.scan())  # Verwacht [0x28] of [0x29]

imu = BNO055(i2c)
imu.reset()
calibrated = False
recording = False

filename = None  # global, nog niet aangemaakt

def start_record():
    global filename, start
    start = time.ticks_ms()
    filename = "imu_data.csv"
    with open(filename, "w") as f:
        # Kopregel schrijven
        f.write("time,temp,mag_x,mag_y,mag_z,gyro_x,gyro_y,gyro_z,accel_x,accel_y,accel_z,lin_x,lin_y,lin_z,grav_x,grav_y,grav_z,quat_w,quat_x,quat_y,quat_z,heading,roll,pitch\n")

start = time.ticks_ms()

def led_manager(led_counter=[]):
    if len(led_counter) == 0:
        print("Start LED manager task...")
        led_counter.append(0)
    if not calibrated:
        onboard_led.toggle()
    elif led_counter[0] % 4 == 0:
        onboard_led.toggle()
    led_counter[0] += 1

def read_bno055():
    global calibrated
    if not calibrated:
        calibrated = imu.calibrated()
        sys, gyro, accel, mag = imu.cal_status()
        if accel < 3:
            if sys < 3 or gyro < 3 or mag < 3:
                rgb_led[0] = (63, 0, 0)
            else:
                rgb_led[0] = (63, 31, 0)
        else:
            rgb_led[0] = (0, 63, 0)
        rgb_led.write()
                
        print(f'Calibration required: sys {sys} gyro {gyro} accel {accel} mag {mag}')
    if recording:
        # Tijd sinds start (in seconden)
        t = (time.ticks_ms() - start) / 1000

        # Sensor uitlezen
        temp = imu.temperature()
        mag = imu.mag()
        gyro = imu.gyro()
        accel = imu.accel()
        lin = imu.lin_acc()
        grav = imu.gravity()
        quat = imu.quaternion()
        euler = imu.euler()

        # Eén CSV-regel maken  
        line = "{:.2f},{:.1f},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            t, temp, *mag, *gyro, *accel, *lin, *grav, *quat, *euler)

        # Toevoegen aan bestand
        with open(filename, "a") as f:
            f.write(line)
    else:
        print('Temperature {}°C'.format(imu.temperature()))
        print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
        print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
        print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
        print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
        print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
        print('Quatern.  w {:5.3f}    x {:5.3f}     y {:5.3f}     z {:5.3f}'.format(*imu.quaternion()))
        print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))

def read_pressure():
    pass
    # print("Druksensor gelezen (dummy)")

def read_temperature():
    pass
    # print("Temperatuursensor gelezen (dummy)")

def button_read(prev_button = []):
    global recording, start
    if len(prev_button) == 0:
        print("Start button read task...")
        prev_button.append(button.value())
    button_val = button.value()
    if button_val == 0 and prev_button[0] == 1:
        if recording:
            recording =  False
            rgb_led[0] = (0, 63, 0)
        else:
            if calibrated:
                start_record()
                recording =  True
                rgb_led[0] = (0, 0, 63)
                print("Recording ...")
        rgb_led.write()        
              
    prev_button[0] = button_val

scheduler = Scheduler()
scheduler.add_task(Task("LedManager", 250, led_manager))
# scheduler.add_task(Task("Druk", 5, read_pressure))
# scheduler.add_task(Task("Temperatuur", 100, read_temperature))
scheduler.add_task(Task("BNO055", 200, read_bno055))
scheduler.add_task(Task("ButtonRead", 100, button_read))

# Start de scheduler (voor demo: 1 cyclus)
print("Start scheduler...")
while True:
    for task in scheduler.tasks:
        if task.should_run():
            task.run()
    if recording and (time.ticks_ms() - start) / 1000 >= 1800:
        break

print(f"Program ended! Recorded for {(time.ticks_ms() - start) / 1000} seconds.")
rgb_led[0] = (63, 31, 0)  
rgb_led.write()