import serial

def limGo():
    ser = serial.Serial('/dev/tty/ACM0', 115200, bytesize=8, timeout=None, stopbits=1)
    ser.write(b'!r 2_')
    ser.close()

def limStop():
    ser = serial.Serial('/dev/tty/ACM0', 115200, bytesize=8, timeout=None, stopbits=1)
    ser.write(b'!r 0_')
    ser.close()
