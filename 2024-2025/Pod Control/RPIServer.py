import socketserver
import threading
import socket

# Raspberry pi connection code
# TCP connection, server side
COMMANDS_FILE = "/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/commands.txt"
SENSOR_FILE = "/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/sensorvals.txt"

class TCPHandler(socketserver.StreamRequestHandler):
    # Request handler for the server. instantiated once per connection to server, must override the handle() method
    def __init__(self, request, client_address, server, command_lock: threading.Lock, sensor_lock: threading.Lock):
        super().__init__(request, client_address, server)
        self.command_lock = command_lock
        self.sensor_lock = sensor_lock

    def handle(self):
        # self.rfile: a file object containing the request from the client.
        self.data = self.rfile.read().rstrip() # read 100 bytes of data from the client (control station)
        # aquire commands lock and write to commands file
        print(self.data.decode("utf-8"))
        self.command_lock.acquire()
        print("cmd lock acq")
        with open(COMMANDS_FILE, "w") as c:
            c.write(self.data.decode("utf-8"))
        # release commands lock, aquire sensor lock, write to self.wfile to send data to gui
        self.command_lock.release()
        self.sensor_lock.acquire()
        print("sens lock acq")
        with open(SENSOR_FILE, "r") as s:
            values = s.read()
            self.wfile.write(values)
            print("sent")
        self.sensor_lock.release()

class RpiServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate, command_lock: threading.Lock, sensor_lock: threading.Lock):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.command_lock = command_lock
        self.sensor_lock = sensor_lock

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.command_lock, self.sensor_lock)
    

def connection(command_lock: threading.Lock, sensor_lock: threading.Lock, Host, Port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((Host, Port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode().strip()
        if data:
            #print(data + " cmd") 
            command_lock.acquire()
            with open(COMMANDS_FILE, "w") as c:
                c.write(data)
            # release commands lock, aquire sensor lock, write to self.wfile to send data to gui
            command_lock.release()
        sensor_lock.acquire()
        with open(SENSOR_FILE, "r") as s:
            values = s.read()
            conn.send(values.encode("utf-8")) # send to gui
        sensor_lock.release()
        

if __name__ == "__main__":
    c = threading.Lock()
    s = threading.Lock()
    RPI_IP = "192.168.0.120" # On Hyperloop wifi
    RPI_PORT = 15000
    connection(c, s, RPI_IP, RPI_PORT)