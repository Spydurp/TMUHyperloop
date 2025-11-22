import tkinter as tk
from LIMBrakePanel import LIMBrakePanel
import threading
import time

SENSOR_FILE = "sensorvals.txt"

class HyperloopGUI:
    def __init__(self, root, data_lock, command_lock):
        self.root = root
        self.data_lock = data_lock
        self.command_lock = command_lock
        
        # Configure root window
        self.root.title("Hyperloop Mission Control")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")
        
        # Create the LIM and Brake panel
        self.panel = LIMBrakePanel(self.root)
        
        # Start update loop
        self.update_data()
        
    def update_data(self):
        """Update all displays with current sensor data"""
        try:
            # Read sensor data from file
            if self.data_lock.acquire(blocking=False):
                try:
                    with open(SENSOR_FILE, "r") as f:
                        data = f.read().split(',')
                        if len(data) >= 21:
                            # Update the panel with sensor data
                            self.panel.update(
                                lim_temp=float(data[12]),      # LIM Temperature
                                lim_volt=float(data[13]),      # LIM Voltage
                                lim_cur=float(data[14]),       # LIM Current
                                inverter_volt=float(data[20]), # Inverter Voltage
                                brake1=(data[15].strip().lower() == 'true'),  # Brake 1
                                brake2=(data[16].strip().lower() == 'true'),  # Brake 2
                                distance=float(data[18])       # Distance traveled
                            )
                except FileNotFoundError:
                    print(f"Error: {SENSOR_FILE} not found")
                except Exception as e:
                    print(f"Error reading sensor data: {e}")
                finally:
                    self.data_lock.release()
            
        except Exception as e:
            print(f"Error updating display: {e}")
        
        # Schedule next update (500ms = 2 Hz)
        self.root.after(500, self.update_data)

def main(data_lock, command_lock):
    """Main entry point for the GUI"""
    root = tk.Tk()
    app = HyperloopGUI(root, data_lock, command_lock)
    root.mainloop()

if __name__ == "__main__":
    # For standalone testing without locks
    print("Running in standalone test mode...")
    print("Make sure sensorvals.txt exists with proper data format")
    
    data_lock = threading.Lock()
    command_lock = threading.Lock()
    main(data_lock, command_lock)