import socketserver
import threading

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
        self.command_lock.acquire()
        with open(COMMANDS_FILE, "w") as c:
            c.write(self.data.decode("utf-8"))
        # release commands lock, aquire sensor lock, write to self.wfile to send data to gui
        self.command_lock.release()
        self.sensor_lock.acquire()
        with open(SENSOR_FILE, "r") as s:
            values = s.read()
            self.wfile.write(values)

class RpiServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate, command_lock: threading.Lock, sensor_lock: threading.Lock):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.command_lock = command_lock
        self.sensor_lock = sensor_lock

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.command_lock, self.sensor_lock)
    

def connection(command_lock, sensor_lock, Host, Port):
    with RpiServer((Host, Port), TCPHandler, True, command_lock, sensor_lock) as server:
        server.serve_forever()