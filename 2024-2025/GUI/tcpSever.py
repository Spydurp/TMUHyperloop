import socket
import threading
import json
import time
import random
import argparse

class HyperloopTCPServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = []
        self.client_lock = threading.Lock()
        
        # Pod state
        self.state = "Safe to Approach"
        self.velocity = 0.0
        self.distance_traveled = 0.0
        self.brake1_deployed = True
        self.brake2_deployed = True
        self.bat_temp_base = [25.0, 26.5, 27.0, 25.5]
        self.bat_volt_base = [48.5, 48.1, 48.7, 48.2]
        self.bat_cur_base = [0.2, 0.0, 0.5, 0.1]
        self.lim_temp = 30.0
        self.lim_volt = 0.0
        self.lim_cur = 0.0
        self.inverter_volt = 0.0
        
        # Simulation parameters
        self.max_velocity = 350.0  # m/s
        self.acceleration = 25.0   # m/s²
        self.deceleration = 15.0   # m/s²
        self.track_length = 1500.0 # m
        
        # Simulation state
        self.is_accelerating = False
        self.is_decelerating = False
        self.last_update_time = time.time()
    
    def start(self):
        """Start the TCP server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")
            
            self.running = True
            
            # Start the simulation in a separate thread
            sim_thread = threading.Thread(target=self.run_simulation)
            sim_thread.daemon = True
            sim_thread.start()
            
            # Start accepting clients
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"New connection from {client_address}")
                    
                    # Start a new thread to handle this client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                    with self.client_lock:
                        self.clients.append((client_socket, client_address))
                        
                except Exception as e:
                    if self.running:
                        print(f"Error accepting client: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
            self.stop()
    
    def stop(self):
        """Stop the TCP server"""
        self.running = False
        
        # Close all client connections
        with self.client_lock:
            for client_socket, _ in self.clients:
                try:
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        # Close the server socket
        if self.server_socket:
            try:
                self.server_socket.close()
                print("Server stopped")
            except:
                pass
    
    def handle_client(self, client_socket, client_address):
        """Handle communication with a client"""
        try:
            # First, send the current state
            self.send_state_to_client(client_socket)
            
            # Then handle incoming commands
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        # Client disconnected
                        break
                    
                    # Parse the command
                    try:
                        command = json.loads(data.decode('utf-8'))
                        print(f"Received command from {client_address}: {command}")
                        
                        if "command" in command:
                            if command["command"] == "launch":
                                self.start_launch_sequence()
                            elif command["command"] == "stop":
                                self.start_stop_sequence()
                    except json.JSONDecodeError:
                        print(f"Invalid command format: {data.decode('utf-8')}")
                    
                except socket.timeout:
                    # This is normal, continue
                    continue
                except Exception as e:
                    print(f"Error receiving data from client: {e}")
                    break
                    
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            try:
                client_socket.close()
                print(f"Connection closed with {client_address}")
                with self.client_lock:
                    self.clients = [(s, a) for s, a in self.clients if s != client_socket]
            except:
                pass
    
    def send_state_to_all_clients(self):
        """Send the current state to all connected clients"""
        sensor_data = self.get_current_sensor_data()
        data_json = json.dumps(sensor_data)
        
        with self.client_lock:
            clients_to_remove = []
            
            for client_socket, client_address in self.clients:
                try:
                    client_socket.send(data_json.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending data to {client_address}: {e}")
                    clients_to_remove.append((client_socket, client_address))
            
            # Remove any clients that had errors
            for client in clients_to_remove:
                self.clients.remove(client)
                try:
                    client[0].close()
                except:
                    pass
    
    def send_state_to_client(self, client_socket):
        """Send the current state to a specific client"""
        try:
            sensor_data = self.get_current_sensor_data()
            data_json = json.dumps(sensor_data)
            client_socket.send(data_json.encode('utf-8'))
        except Exception as e:
            print(f"Error sending state to client: {e}")
    
    def get_current_sensor_data(self):
        """Get the current sensor data as a list"""
        # Add some random noise to make it realistic
        def add_noise(value, scale=0.01):
            return value + random.uniform(-value * scale, value * scale)
        
        # Battery temps, volts, amps for all 4 batteries
        bat_temps = [add_noise(t + (10 * self.velocity / self.max_velocity)) for t in self.bat_temp_base]
        
        # Battery voltage goes down slightly during acceleration
        bat_volts = [add_noise(v - (3 * self.velocity / self.max_velocity)) for v in self.bat_volt_base]
        
        # Battery current increases during acceleration
        current_factor = 0
        if self.is_accelerating:
            current_factor = 100
        elif self.is_decelerating:
            current_factor = 30  # Regenerative braking
        elif self.velocity > 0:
            current_factor = 20  # Maintaining speed
            
        bat_curs = [add_noise(c + current_factor) for c in self.bat_cur_base]
        
        # LIM values
        lim_temp_actual = self.lim_temp + (30 * self.velocity / self.max_velocity)
        lim_volt_actual = self.lim_volt
        lim_cur_actual = self.lim_cur
        
        # Inverter voltage
        inverter_volt_actual = self.inverter_volt
        
        # Compile all the data
        sensor_data = [
            bat_temps[0], bat_volts[0], bat_curs[0],  # Battery 1
            bat_temps[1], bat_volts[1], bat_curs[1],  # Battery 2
            bat_temps[2], bat_volts[2], bat_curs[2],  # Battery 3
            bat_temps[3], bat_volts[3], bat_curs[3],  # Battery 4
            lim_temp_actual, lim_volt_actual, lim_cur_actual,  # LIM
            self.brake1_deployed, self.brake2_deployed,  # Brakes
            round(self.velocity, 1), round(self.distance_traveled, 1),  # Speed and position
            self.state,  # State
            round(inverter_volt_actual, 1)  # Inverter voltage
        ]
        
        return sensor_data
    
    def start_launch_sequence(self):
        """Start the launch sequence"""
        if self.state != "Safe to Approach":
            print("Cannot launch - not in Safe to Approach state")
            return
            
        print("Starting launch sequence")
        self.state = "Launch Sequence Initiated"
        
        # Set parameters for launch
        self.is_accelerating = True
        self.is_decelerating = False
        self.brake1_deployed = False
        self.brake2_deployed = False
        
        # Set the LIM and inverter values
        self.lim_volt = 400.0
        self.lim_cur = 15.0
        self.inverter_volt = 220.0
        
        self.state = "Accelerating"
    
    def start_stop_sequence(self):
        """Start the emergency stop sequence"""
        print("Starting emergency stop sequence")
        self.state = "Emergency Stop Initiated"
        
        # Set parameters for emergency stop
        self.is_accelerating = False
        self.is_decelerating = True
        
        # If we're at speed, deploy brakes
        if self.velocity > 0:
            self.brake1_deployed = True
            self.brake2_deployed = True
            
        # Cut power to LIM
        self.lim_volt = 0.0
        self.lim_cur = 0.
    

    def run_simulation(self):
        """Simulate pod motion and update state periodically."""
        while self.running:
            current_time = time.time()
            elapsed_time = current_time - self.last_update_time
            self.last_update_time = current_time

            if self.is_accelerating:
                self.velocity = min(self.velocity + self.acceleration * elapsed_time, self.max_velocity)
                self.distance_traveled += self.velocity * elapsed_time
                if self.velocity >= self.max_velocity:
                    self.is_accelerating = False
                    self.is_decelerating = True  # Transition to deceleration

            elif self.is_decelerating:
                self.velocity = max(self.velocity - self.deceleration * elapsed_time, 0)
                self.distance_traveled += self.velocity * elapsed_time
                if self.velocity <= 0:
                    self.is_decelerating = False
                    self.state = "Safe to Approach"

            self.send_state_to_all_clients()
            time.sleep(0.5)  # Adjust frequency of updates

server = HyperloopTCPServer()
server.start()