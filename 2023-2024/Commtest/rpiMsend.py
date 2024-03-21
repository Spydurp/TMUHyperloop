import socket
import time
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    
HOST = "172.20.10.3"  # The server's hostname or IP address
PORT = 65431  # The port used by the server

message = b"Hello, world"

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server")
            while True:
                if ser.in_waiting > 0:
                    message = ser.readline()
                s.sendall(message)
                data = s.recv(1024)
                print(f"Received {data!r}")
                time.sleep(1)  # Adjust the delay between messages if needed
        except ConnectionRefusedError:
            print("Connection refused. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            time.sleep(1)  # Wait before reconnecting