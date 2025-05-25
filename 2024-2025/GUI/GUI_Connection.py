import threading
import socket
import sys

# Control Station GUI Backend code (running on laptop)

def connect(HOST, PORT, command_lock: threading.Lock, data_lock: threading.Lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        # send commands from commands file, acquire lock first
        command_lock.acquire()
        with open("GUI/commands.txt", "r") as c:
            data = c.read()
        command_lock.release()
        sock.sendall(bytes(data, "utf-8"))
        sock.sendall(b"\n")

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        #acquire datalock and write to datafile
        data_lock.acquire()
        with open("GUI/data.txt", "w") as d:
            d.write(received)