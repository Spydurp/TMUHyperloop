import socket
import time
import serial
import pinouts
import podStates
from threading import Thread

CURSTATE = 0
SAFE = 0
RUNNING = 1
BRAKING = 2
FAULT = 3

start = time.time()

ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1) #ACM2 does not exist atm
ser3 = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
SBL = serial.Serial('COM3', 115200, bytesize=8, timeout=None, stopbits=1) # Find actual port name in testing
ser1.reset_input_buffer()
ser2.reset_input_buffer()
ser3.reset_input_buffer()

# Brake Check
if not podStates.brakeCheck():
    print("ERROR: Brakes not cycling")
    CURSTATE = FAULT
    
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

                if commands[0] != '!' or commands[1] == 'X':
                    print("connection broken")
                    CURSTATE = FAULT
                    # Test !EX(Emergency Shutdown), !MS(Stop in all modes), !SFT(Safety stop)
                    SBL.write(b'!EX')
                    pinouts.lim_power_off()
                    pinouts.apply_brakes()
                    if pinouts.brake_L_OFF and pinouts.brake_R_OFF and not pinouts.brake_R_ON and not pinouts.brake_L_ON:
                        CURSTATE = SAFE
                
                if commands[1] == 'G' and CURSTATE != FAULT and CURSTATE != RUNNING:
                    # Set up power connections, close switches, release brakes
                    CURSTATE = Thread(target = podStates.launch, args=(SBL)).start()
                
                if CURSTATE == FAULT:
                    SBL.write(b'!EX')
                    pinouts.lim_power_off()
                    pinouts.apply_brakes()
                    if pinouts.brake_L_OFF and pinouts.brake_R_OFF and not pinouts.brake_R_ON and not pinouts.brake_L_ON:
                        CURSTATE = SAFE

                #End of loop, clear commands
                commands = {}
                com_in = ""
                commandSize = 0
        
        except ConnectionRefusedError:
            print("Connection refused. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            time.sleep(1)  # Wait before reconnecting