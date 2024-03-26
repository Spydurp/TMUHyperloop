import serial

def readSerial():
    message = {}
    if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()

    if ser.in_waiting > 0:
        message = message.append(ser.readline())