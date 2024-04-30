import socket
import time
import serial

# Data Array Definitions
BATVOLT = 0
LIMVOLT = 1
BATCUR = 2
LIMCUR = 3
VEL = 4
LBRAKEON = 5
LBRAKEOFF = 6
RBRAKEON = 7
RBRAKEOFF = 8

start = time.time()

if __name__ == '__main__':
    ser1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1) #ACM2 does not exist atm
    ser3 = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
    ser1.reset_input_buffer()
    ser2.reset_input_buffer()
    ser3.reset_input_buffer()
    
HOST = "172.20.10.3"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

message = b"Hello, world"

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

                s.sendall(data)
                conn, addr = s.accept()
                data = conn.recv(1024)
                print(f"Received {data!r}")
                time.sleep(1)  # Adjust/remove the delay between messages if needed

                # Put state code and behavior here
                
        except ConnectionRefusedError:
            print("Connection refused. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            time.sleep(1)  # Wait before reconnecting


# Error, program closed
# Shut down all power, deploy brakes