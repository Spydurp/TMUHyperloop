import serial
import keyboard


# Configure the serial port


# Open the serial port
ser = serial.Serial('COM3', 115200, bytesize=8, timeout=None, stopbits=1)
#packet = bytearray([0xAA, 0x01, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xDE, 0xAD])

# Send data through the serial port
while(not keyboard.is_pressed("`")):
    if keyboard.is_pressed('w'):
        ser.write(b'!G 1 1000_')
        print(ser.read(12))
    elif(keyboard.is_pressed('s')):
        ser.write(b'!G 1 -1000_')
        print(ser.read(13))
    elif(keyboard.is_pressed('a')):
        ser.write(b'!AC 1 50000_')
        print(ser.read(13))
    elif(keyboard.is_pressed('d')):
        ser.write(b'!DC 1 50000_')
        print(ser.read(13))
    # Send a command to set the motor speed to the maximum value

# Close the serial port
ser.close()
