import smbus2
import math
import time
import serial

# MPU6050 Registers and Addresses
DEVICE_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change port name to whatever
time.sleep(2)  # Allow time for Arduino to initialize

# MPU6050 initialization
bus = smbus2.SMBus(1)
bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)

def read_acceleration_data():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, ACCEL_XOUT, 6)
    x = (data[0] << 8) | data[1]
    y = (data[2] << 8) | data[3]
    z = (data[4] << 8) | data[5]

    # Convert raw values to acceleration in m/s^2
    accel_x = x / 16384.0
    accel_y = y / 16384.0
    accel_z = z / 16384.0

    return accel_x, accel_y, accel_z

def calculate_speed(accel_x, accel_y, accel_z, time_interval):
    # Calculate resultant acceleration (excluding gravity) GENIUS 
    accel_resultant = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    
    # Calculate change in velocity (speed) using the equation: v = u + at
    # Assuming initial velocity u = 0, and a is the resultant acceleration I LOVE PHYSICKs
    speed = accel_resultant * time_interval

    return speed

try:
    while True:
        start_time = time.time()  # Record start time for interval

        # Read acceleration data
        accel_data = read_acceleration_data()

        # Calculate time interval since the last reading
        current_time = time.time()
        time_interval = current_time - start_time

        # Calculate speed using acceleration data and time interval
        current_speed = calculate_speed(*accel_data, time_interval)

        # Send speed data back to Arduino
        speed_str = "{:.2f}".format(current_speed)
        ser.write(speed_str.encode())

        # Print speed to console
        print("Current Speed: {} m/s".format(speed_str))

        # Wait until half a second elapses before the next reading
        time.sleep(0.5 - time_interval)  # Adjust for elapsed time

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
