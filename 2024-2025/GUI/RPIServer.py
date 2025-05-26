import socketserver
import threading

# Raspberry pi connection code
# TCP connection, server side

class TCPHandler(socketserver.StreamRequestHandler):
    # Request handler for the server. instantiated once per connection to server, must override the handle() method
    def __init__(self, request, client_address, server, command_lock: threading.Lock, sensor_lock: threading.Lock):
        super().__init__(request, client_address, server)
        self.command_lock = command_lock
        self.sensor_lock = sensor_lock

    def handle(self):
        # self.rfile: a file object containing the request from the client.
        self.data = self.rfile.readline(100).rstrip() # read 100 bytes of data from the client (control station)
        # aquire commands lock and write to commands file
        self.command_lock.acquire()
        with open("Pod Control/commands.txt", "w") as c:
            c.write(self.data.decode("utf-8"))
        # release commands lock, aquire sensor lock, write to self.wfile to send data to gui
        self.command_lock.release()
        self.sensor_lock.acquire()
        with open("Pod Control/sensorvals.txt", "r") as s:
            values = s.readline()
            self.wfile.write(values)


def connection(command_lock, sensor_lock, Host, Port):
    with socketserver.TCPServer((Host, Port), TCPHandler) as server:
        server.serve_forever()