import serial.tools.list_ports

# Get a list of available serial ports
ports = list(serial.tools.list_ports.comports())

# Print the list of available serial ports
for port in ports:
    print(port)
