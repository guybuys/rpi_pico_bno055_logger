# Raspberry Pi Pico with the Adafruit BNO055 module in MicroPython

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

The file ```bno_i2c_scanner.py``` was only intended to find the address on the i2c. I started from the example on the **micropython-bno055** repository but it didn't work. With the scanner file, I could see that the I2C address was found but the communication didn't work, probably due to the I2C clock stretching of the BNO055. When I swiched and used the SoftI2C class instead of the I2C class, it did work. I did not change the pull-up resistors of the **adafruit BNO055** module. The ```tsm_bno055_example.py``` program also checks the available addresses on the i2c bus so the ```bno_i2c_scanner.py``` is not needed. 

## Inertial Measurement Unit

Using an Inertial Measurement Unit is a bit challenging. There are a bunch of very useful videos of *Paul McWhorter* that are interesting to watch in order to understand it. I found the video below very interesting to see how the calibration of the accelerometer is done:
[9-Axis IMU LESSON 5: Calibrating the BNO055 9-axis Inertial Measurement Sensor](https://www.youtube.com/watch?v=yPfQK75dZbU)

The complete tutorial consists of a list of interesting videos. You can skip the parts about **Arduino** code and iced coffee without sugar. Just focus on the understanding of the IMU.

[9 Axis Inertial Measurement Units With Arduino Tutorial](https://www.youtube.com/watch?v=2AO\_Gmh5K3Q\&list=PLGs0VKk2DiYwEo-k0mjIkWXlkrJWAU4L9)

In case you prefer to read, this link is a written introduction with clear drawings and animations:
[Inertial Measurement Unit introduction](https://www.advancednavigation.com/tech-articles/inertial-measurement-unit-imu-an-introduction/)

Still not found what you are looking for? Search for **how does an imu work** in your favorite search engine. Typical, the explanation is a bit basic but you got to start somewhere ...

