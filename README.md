# Raspberry Pi Pico with BNO055 in Python

This project logs **IMU** data from a **BNO055** on a **Rpi Pico**.

Except for the **BNO055**, also a **pushbutton** and **neopixel** RGB-led is connected to the pico. The RGB led is used to visualize the calibration state and the pushbutton to make the logger **record** data (write to a csv file) or stop it.

## Additional files

You will need some additional files:

- bno055.py
- bno055_base.py
- scheduler.py

The **bno055** files are from this repository:
[micropython-bno055](https://github.com/micropython-IMU/micropython-bno055)

The **scheduler** file is shared on the **Software Engineering Wiki** repository:

[scheduler](https://github.com/guybuys/SoftwareEngineeringWiki/blob/main/scheduler.py)

If you want the code to run on your **pico** when powered on, rename the file ```tsm_bno055_example.py``` to ```main.py``` when saving it to the **pico**.
The file ```bno_i2c_scanner.py``` is only intended to find the address on the i2c but the ```tsm_bno055_example.py``` program also checks the available addresses on the i2c bus. 

## Inertial Measurement Units

Using Inertial Measurement Units is a bit challenging. There are a bunch of very useful videos of *Paul McWhorter* that are interesting to watch in order to understand it. You should at least watch the video below to see how you should calibrate the accelerometer:
[9-Axis IMU LESSON 5: Calibrating the BNO055 9-axis Inertial Measurement Sensor](https://www.youtube.com/watch?v=yPfQK75dZbU)

The complete tutorial consists of a list of interesting videos. You can skip the parts about **Arduino** code and iced coffee without sugar. Just focus on the understanding of the IMU.

[9 Axis Inertial Measurement Units With Arduino Tutorial](https://www.youtube.com/watch?v=2AO\_Gmh5K3Q\&list=PLGs0VKk2DiYwEo-k0mjIkWXlkrJWAU4L9)
