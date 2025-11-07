import threading
import socket
import time
CMD_FILE = "C:/Users/ankar/OneDrive/Desktop/GNC/Hyperloop/TMUHyperloop/2024-2025/GUI/commands.txt"
DATA_FILE = "C:/Users/ankar/OneDrive/Desktop/GNC/Hyperloop/TMUHyperloop/2024-2025/GUI/data.txt"
# Control Station GUI Backend code (running on laptop)

def connect(HOST, PORT, command_lock: threading.Lock, data_lock: threading.Lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        # send commands from commands file, acquire lock first
        command_lock.acquire()
        print("cmd lock acq")
        with open(CMD_FILE, "r") as c:
            data = c.read()
        command_lock.release()
        sock.send(bytes(data, "utf-8"))
        print("sent commands")

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        #acquire datalock and write to datafile
        print(received)
        data_lock.acquire()
        print("data lock acq")
        with open(DATA_FILE, "w") as d:
            d.write(received)
        data_lock.release()
        print("received data")
        time.sleep(0.5)