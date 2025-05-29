import socket
import time
import serial
import pinouts
import podStates

# Data Array Definitions
BATVOLT = 0
BATCUR = 1
BATTEMP = 2
LIMVOLT = 3
LIMCUR = 4
LIMTEMP = 5
VEL = 6
LBRAKEON = 7
LBRAKEOFF = 8
RBRAKEON = 9
RBRAKEOFF = 10

# State Definitions
SAFE = 0
LAUNCH_READY = 1
RUNNING = 2
BRAKING = 3
CRAWLING = 4
FAULT = 5
CURSTATE = 0

start = time.time()

ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1) #ACM2 does not exist atm
ser3 = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
ser1.reset_input_buffer()
ser2.reset_input_buffer()
ser3.reset_input_buffer()

# Brake Check
podStates.brakeCheck()
    
HOST = "172.20.10.3"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server")
            while True:
                data = ""
                if ser1.in_waiting > 0: # Use CSV format
                    line1 = ser1.readline()
                    data = data + line1.decode('utf-8').rstrip() + ","
                else: 
                     # fill with space character and a comma for next value
                    data = data + " ,"
                if ser2.in_waiting > 0: # Use CSV format
                    line2 = ser2.readline()
                    data = data + line1.decode('utf-8').rstrip() + ","
                else:# fill with space character and a comma for next value
                    data = data + " ,"
                if ser3.in_waiting > 0: # Use CSV format
                    line3 = ser3.readline()
                    data = data + line1.decode('utf-8').rstrip() + ","
                else: # fill with space character and a comma for next value
                    data = data + " ,"

                # Save data
                file = open("sensordata.txt", "a")
                file.write(data + " time: " + str(time.time() - start) + "\n")
                file.close()

                s.sendall(bytes(data, 'utf-8'))
                com_in = s.recv(1024).decode('utf-8')
                print(f"Received {data!r}")
                # Parse command inputs
                commands = com_in.split(" ")
                commandSize = len(commands)
                if "X" in commands or "!" not in commands:
                    # E-Stop
                    pinouts.apply_brakes()
                    pinouts.lim_power_off()
                    s.sendall(bytes("E-Stop Recieved: Power Cut", 'utf-8'))
                
                    
                # Put state code and behavior here
                
        except ConnectionRefusedError:
            print("Connection refused. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            time.sleep(1)  # Wait before reconnecting


# Error, program closed
# Shut down all power, deploy brakes