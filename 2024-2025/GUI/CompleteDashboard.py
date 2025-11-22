import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from datetime import datetime

SENSOR_FILE = "sensorvals.txt"
COMMAND_FILE = "commands.txt"

class CompleteDashboard:
    def __init__(self, root, data_lock, command_lock):
        self.root = root
        self.data_lock = data_lock
        self.command_lock = command_lock
        
        # Configure root window
        self.root.title("Hyperloop Mission Control")
        self.root.geometry("1600x900")
        self.root.configure(bg="#0f172a")
        
        # Sensor data
        self.sensor_data = {
            'state': 'Safe to Approach',
            'lim_temp': 0.0,
            'lim_volt': 0.0,
            'lim_cur': 0.0,
            'inverter_volt': 0.0,
            'brake1': False,
            'brake2': False,
            'distance': 0.0,
            'velocity': 0.0
        }
        
        self.setup_ui()
        self.update_data()
        
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg="#0f172a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # STATE HEADER
        self.create_state_header(main_container)
        
        # MIDDLE SECTION: LIM, BRAKE, MISSION CONTROL
        middle_frame = tk.Frame(main_container, bg="#0f172a")
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create three columns
        lim_column = tk.Frame(middle_frame, bg="#0f172a")
        lim_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        brake_column = tk.Frame(middle_frame, bg="#0f172a")
        brake_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        mission_column = tk.Frame(middle_frame, bg="#0f172a")
        mission_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Create panels
        self.create_lim_panel(lim_column)
        self.create_brake_panel(brake_column)
        self.create_mission_control(mission_column)
        
        # BOTTOM SECTION: LOGS
        logs_frame = tk.Frame(main_container, bg="#0f172a")
        logs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create two log panels
        system_log_frame = tk.Frame(logs_frame, bg="#0f172a")
        system_log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        rover_log_frame = tk.Frame(logs_frame, bg="#0f172a")
        rover_log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.create_system_logs(system_log_frame)
        self.create_rover_logs(rover_log_frame)
        
    def create_state_header(self, parent):
        """Create the state display header"""
        header_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#06b6d4",
                               highlightthickness=2)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title = tk.Label(header_frame, text="CURRENT STATE", 
                        font=("Consolas", 14, "bold"),
                        bg="#1e293b", fg="#06b6d4")
        title.pack(pady=(10, 5))
        
        # State display
        state_bg = tk.Frame(header_frame, bg="#334155", 
                           highlightbackground="#06b6d4", highlightthickness=1)
        state_bg.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.state_label = tk.Label(state_bg, text="SAFE", 
                                    font=("Consolas", 36, "bold"),
                                    bg="#334155", fg="#22c55e")
        self.state_label.pack(pady=15)
        
        # System status
        self.status_label = tk.Label(header_frame, text="System Status: Operational",
                                    font=("Consolas", 10),
                                    bg="#1e293b", fg="#06b6d4")
        self.status_label.pack(pady=(0, 10))
        
    def create_lim_panel(self, parent):
        """Create LIM System panel"""
        lim_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#3b82f6",
                            highlightthickness=2)
        lim_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(lim_frame, text="⚡ LIM SYSTEM",
                         font=("Consolas", 16, "bold"),
                         bg="#1e293b", fg="#60a5fa")
        header.pack(pady=(15, 10), padx=15, anchor=tk.W)
        
        # Metrics
        self.lim_metrics = {}
        self.create_metric(lim_frame, "Voltage", "lim_volt", "V", "#60a5fa", "#3b82f6", 600)
        self.create_metric(lim_frame, "Current", "lim_cur", "A", "#fbbf24", "#f59e0b", 200)
        self.create_metric(lim_frame, "Temperature", "lim_temp", "°C", "#fb923c", "#f97316", 100)
        self.create_metric(lim_frame, "Inverter Voltage", "inverter_volt", "V", "#c084fc", "#a855f7", 750)
        
    def create_brake_panel(self, parent):
        """Create Brake System panel"""
        brake_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#ef4444",
                              highlightthickness=2)
        brake_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(brake_frame, text="⚠ BRAKE SYSTEM",
                         font=("Consolas", 16, "bold"),
                         bg="#1e293b", fg="#f87171")
        header.pack(pady=(15, 10), padx=15, anchor=tk.W)
        
        # Brake statuses
        for i in [1, 2]:
            brake_container = tk.Frame(brake_frame, bg="#334155",
                                      highlightbackground="#ef4444", highlightthickness=1)
            brake_container.pack(fill=tk.X, padx=15, pady=8)
            
            label = tk.Label(brake_container, text=f"Brake Position {i}",
                           font=("Consolas", 11), bg="#334155", fg="#fca5a5")
            label.pack(side=tk.LEFT, padx=12, pady=12)
            
            indicator = tk.Canvas(brake_container, width=12, height=12,
                                bg="#334155", highlightthickness=0)
            indicator.pack(side=tk.RIGHT, padx=5, pady=12)
            circle = indicator.create_oval(1, 1, 11, 11, fill="#22c55e")
            
            status = tk.Label(brake_container, text="UNDEPLOYED",
                            font=("Consolas", 11, "bold"),
                            bg="#334155", fg="#22c55e")
            status.pack(side=tk.RIGHT, padx=10, pady=12)
            
            if i == 1:
                self.brake1_indicator = indicator
                self.brake1_circle = circle
                self.brake1_status = status
            else:
                self.brake2_indicator = indicator
                self.brake2_circle = circle
                self.brake2_status = status
        
        # Distance
        distance_container = tk.Frame(brake_frame, bg="#334155",
                                     highlightbackground="#06b6d4", highlightthickness=1)
        distance_container.pack(fill=tk.X, padx=15, pady=(20, 15))
        
        distance_label = tk.Label(distance_container, text="Distance Traveled",
                                 font=("Consolas", 9), bg="#334155", fg="#67e8f9")
        distance_label.pack(pady=(12, 3))
        
        self.distance_value = tk.Label(distance_container, text="0 m",
                                      font=("Consolas", 28, "bold"),
                                      bg="#334155", fg="#22d3ee")
        self.distance_value.pack(pady=(0, 12))
        
    def create_mission_control(self, parent):
        """Create Mission Control panel"""
        mission_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#a855f7",
                                highlightthickness=2)
        mission_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(mission_frame, text="MISSION CONTROL",
                         font=("Consolas", 16, "bold"),
                         bg="#1e293b", fg="#c084fc")
        header.pack(pady=(15, 10), padx=15, anchor=tk.W)
        
        # Buttons
        buttons = [
            ("PREP FOR LAUNCH", "#3b82f6", "READY"),
            ("ABORT LAUNCH", "#eab308", "ABORT"),
            ("LAUNCH", "#22c55e", "GO"),
            ("STOP", "#f97316", "STOP"),
            ("STOP NOW", "#ef4444", "STOP_NOW"),
            ("RESET FAULT", "#64748b", "RESET_FAULT")
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(mission_frame, text=text,
                          font=("Consolas", 11, "bold"),
                          bg=color, fg="white",
                          activebackground=color, activeforeground="white",
                          relief=tk.FLAT, cursor="hand2",
                          command=lambda cmd=command: self.send_command(cmd))
            btn.pack(fill=tk.X, padx=15, pady=5)
            
    def create_system_logs(self, parent):
        """Create System Logs panel"""
        log_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#22c55e",
                            highlightthickness=2)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(log_frame, text="SYSTEM LOGS",
                         font=("Consolas", 14, "bold"),
                         bg="#1e293b", fg="#22c55e")
        header.pack(pady=(10, 5), padx=15, anchor=tk.W)
        
        # Log text area
        self.system_log = scrolledtext.ScrolledText(log_frame,
                                                    font=("Consolas", 9),
                                                    bg="#000000", fg="#22c55e",
                                                    height=10, wrap=tk.WORD,
                                                    relief=tk.FLAT)
        self.system_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Add initial log
        self.add_system_log("System initialized successfully")
        
    def create_rover_logs(self, parent):
        """Create Rover Logs panel"""
        log_frame = tk.Frame(parent, bg="#1e293b", highlightbackground="#f97316",
                            highlightthickness=2)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(log_frame, text="ROVER LOGS",
                         font=("Consolas", 14, "bold"),
                         bg="#1e293b", fg="#fb923c")
        header.pack(pady=(10, 5), padx=15, anchor=tk.W)
        
        # Log text area
        self.rover_log = scrolledtext.ScrolledText(log_frame,
                                                   font=("Consolas", 9),
                                                   bg="#000000", fg="#fb923c",
                                                   height=10, wrap=tk.WORD,
                                                   relief=tk.FLAT)
        self.rover_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Add initial log
        self.add_rover_log("Rover communication established")
        
    def create_metric(self, parent, label, data_key, unit, color, bar_color, max_val):
        """Create a metric display"""
        container = tk.Frame(parent, bg="#1e293b")
        container.pack(fill=tk.X, padx=15, pady=8)
        
        # Label and value
        top_frame = tk.Frame(container, bg="#1e293b")
        top_frame.pack(fill=tk.X, pady=(0, 3))
        
        name_label = tk.Label(top_frame, text=label, font=("Consolas", 9),
                             bg="#1e293b", fg=color)
        name_label.pack(side=tk.LEFT)
        
        value_label = tk.Label(top_frame, text=f"0 {unit}",
                              font=("Consolas", 9, "bold"),
                              bg="#1e293b", fg=color)
        value_label.pack(side=tk.RIGHT)
        
        # Progress bar
        bar_bg = tk.Canvas(container, height=10, bg="#334155",
                          highlightthickness=1, highlightbackground=bar_color)
        bar_bg.pack(fill=tk.X)
        
        bar_fill = bar_bg.create_rectangle(0, 0, 0, 10, fill=bar_color, outline="")
        
        self.lim_metrics[data_key] = {
            'value_label': value_label,
            'bar_canvas': bar_bg,
            'bar_fill': bar_fill,
            'unit': unit,
            'max_val': max_val
        }
        
    def update_data(self):
        """Update all displays"""
        try:
            if self.data_lock.acquire(blocking=False):
                try:
                    with open(SENSOR_FILE, "r") as f:
                        data = f.read().split(',')
                        if len(data) >= 21:
                            self.sensor_data['lim_temp'] = float(data[12])
                            self.sensor_data['lim_volt'] = float(data[13])
                            self.sensor_data['lim_cur'] = float(data[14])
                            self.sensor_data['brake1'] = data[15].strip().lower() == 'true'
                            self.sensor_data['brake2'] = data[16].strip().lower() == 'true'
                            self.sensor_data['velocity'] = float(data[17])
                            self.sensor_data['distance'] = float(data[18])
                            self.sensor_data['state'] = data[19].strip()
                            self.sensor_data['inverter_volt'] = float(data[20])
                            
                            self.update_displays()
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    self.data_lock.release()
        except Exception as e:
            print(f"Error: {e}")
        
        self.root.after(500, self.update_data)
        
    def update_displays(self):
        """Update all UI elements"""
        # Update state
        state = self.sensor_data['state'].upper()
        self.state_label.config(text=state)
        
        # Color code state
        state_colors = {
            'SAFE TO APPROACH': '#22c55e',
            'READY TO LAUNCH': '#eab308',
            'RUNNING': '#3b82f6',
            'BRAKING': '#f97316',
            'FAULT': '#ef4444'
        }
        color = state_colors.get(state, '#22c55e')
        self.state_label.config(fg=color)
        
        # Update LIM metrics
        for key, metric in self.lim_metrics.items():
            value = self.sensor_data.get(key, 0)
            metric['value_label'].config(text=f"{int(value)} {metric['unit']}")
            
            width = metric['bar_canvas'].winfo_width()
            if width > 1:
                fill_width = (value / metric['max_val']) * width
                metric['bar_canvas'].coords(metric['bar_fill'], 0, 0, fill_width, 10)
        
        # Update brakes
        self.update_brake(1, self.sensor_data['brake1'])
        self.update_brake(2, self.sensor_data['brake2'])
        
        # Update distance
        self.distance_value.config(text=f"{int(self.sensor_data['distance'])} m")
        
    def update_brake(self, brake_num, deployed):
        """Update brake status"""
        if brake_num == 1:
            indicator = self.brake1_indicator
            circle = self.brake1_circle
            status = self.brake1_status
        else:
            indicator = self.brake2_indicator
            circle = self.brake2_circle
            status = self.brake2_status
        
        if deployed:
            indicator.itemconfig(circle, fill="#ef4444")
            status.config(text="DEPLOYED", fg="#ef4444")
        else:
            indicator.itemconfig(circle, fill="#22c55e")
            status.config(text="UNDEPLOYED", fg="#22c55e")
            
    def send_command(self, command):
        """Send command to the pod"""
        try:
            if self.command_lock.acquire(blocking=False):
                try:
                    with open(COMMAND_FILE, "w") as f:
                        f.write(command)
                    self.add_system_log(f"Command sent: {command}")
                except Exception as e:
                    self.add_system_log(f"Error sending command: {e}")
                finally:
                    self.command_lock.release()
        except Exception as e:
            print(f"Error: {e}")
            
    def add_system_log(self, message):
        """Add message to system log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        self.system_log.insert(tk.END, log_msg)
        self.system_log.see(tk.END)
        
    def add_rover_log(self, message):
        """Add message to rover log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        self.rover_log.insert(tk.END, log_msg)
        self.rover_log.see(tk.END)

def main(data_lock, command_lock):
    """Main entry point"""
    root = tk.Tk()
    app = CompleteDashboard(root, data_lock, command_lock)
    root.mainloop()

if __name__ == "__main__":
    print("Running Complete Dashboard...")
    data_lock = threading.Lock()
    command_lock = threading.Lock()
    main(data_lock, command_lock)