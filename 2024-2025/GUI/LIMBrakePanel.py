import tkinter as tk

class LIMBrakePanel:
    """LIM System and Brake System Display Panels for Hyperloop Dashboard"""
    
    def __init__(self, parent):
        """
        Initialize LIM and Brake Panels
        
        Args:
            parent: Parent tkinter widget (Frame or window)
        """
        self.parent = parent
        self.metrics = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Create the LIM and Brake System panels"""
        # Main container with two columns
        main_frame = tk.Frame(self.parent, bg="#0f172a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column for LIM
        left_frame = tk.Frame(main_frame, bg="#0f172a")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Right column for Brake
        right_frame = tk.Frame(main_frame, bg="#0f172a")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Create panels
        self.create_lim_panel(left_frame)
        self.create_brake_panel(right_frame)
        
    def create_lim_panel(self, parent):
        """Create the LIM System panel"""
        # LIM System Frame
        lim_frame = tk.Frame(parent, bg="#1e293b", 
                            highlightbackground="#3b82f6", 
                            highlightthickness=2, relief=tk.FLAT)
        lim_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Header
        header = tk.Label(lim_frame, text="⚡ LIM SYSTEM", 
                         font=("Consolas", 18, "bold"),
                         bg="#1e293b", fg="#60a5fa", anchor=tk.W)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Create metrics
        self.create_metric(lim_frame, "Voltage", "lim_volt", "V", "#60a5fa", "#3b82f6", 600)
        self.create_metric(lim_frame, "Current", "lim_cur", "A", "#fbbf24", "#f59e0b", 200)
        self.create_metric(lim_frame, "Temperature", "lim_temp", "°C", "#fb923c", "#f97316", 100)
        self.create_metric(lim_frame, "Inverter Voltage", "inverter_volt", "V", "#c084fc", "#a855f7", 750)
        
    def create_brake_panel(self, parent):
        """Create the Brake System panel"""
        # Brake System Frame
        brake_frame = tk.Frame(parent, bg="#1e293b", 
                              highlightbackground="#ef4444", 
                              highlightthickness=2, relief=tk.FLAT)
        brake_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Header
        header = tk.Label(brake_frame, text="⚠ BRAKE SYSTEM", 
                         font=("Consolas", 18, "bold"),
                         bg="#1e293b", fg="#f87171", anchor=tk.W)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Brake 1 Status
        brake1_container = tk.Frame(brake_frame, bg="#334155", 
                                   highlightbackground="#ef4444",
                                   highlightthickness=1)
        brake1_container.pack(fill=tk.X, padx=20, pady=10)
        
        brake1_label = tk.Label(brake1_container, text="Brake Position 1", 
                               font=("Consolas", 12), bg="#334155", fg="#fca5a5")
        brake1_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.brake1_indicator = tk.Canvas(brake1_container, width=15, height=15, 
                                         bg="#334155", highlightthickness=0)
        self.brake1_indicator.pack(side=tk.RIGHT, padx=5, pady=15)
        self.brake1_circle = self.brake1_indicator.create_oval(2, 2, 13, 13, fill="#22c55e")
        
        self.brake1_status = tk.Label(brake1_container, text="UNDEPLOYED", 
                                     font=("Consolas", 12, "bold"), 
                                     bg="#334155", fg="#22c55e")
        self.brake1_status.pack(side=tk.RIGHT, padx=10, pady=15)
        
        # Brake 2 Status
        brake2_container = tk.Frame(brake_frame, bg="#334155", 
                                   highlightbackground="#ef4444",
                                   highlightthickness=1)
        brake2_container.pack(fill=tk.X, padx=20, pady=10)
        
        brake2_label = tk.Label(brake2_container, text="Brake Position 2", 
                               font=("Consolas", 12), bg="#334155", fg="#fca5a5")
        brake2_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.brake2_indicator = tk.Canvas(brake2_container, width=15, height=15, 
                                         bg="#334155", highlightthickness=0)
        self.brake2_indicator.pack(side=tk.RIGHT, padx=5, pady=15)
        self.brake2_circle = self.brake2_indicator.create_oval(2, 2, 13, 13, fill="#22c55e")
        
        self.brake2_status = tk.Label(brake2_container, text="UNDEPLOYED", 
                                     font=("Consolas", 12, "bold"), 
                                     bg="#334155", fg="#22c55e")
        self.brake2_status.pack(side=tk.RIGHT, padx=10, pady=15)
        
        # Distance Display
        distance_container = tk.Frame(brake_frame, bg="#334155", 
                                     highlightbackground="#06b6d4",
                                     highlightthickness=1)
        distance_container.pack(fill=tk.X, padx=20, pady=(30, 20))
        
        distance_label = tk.Label(distance_container, text="Distance Traveled", 
                                 font=("Consolas", 10), bg="#334155", fg="#67e8f9")
        distance_label.pack(pady=(15, 5))
        
        self.distance_value = tk.Label(distance_container, text="0 m", 
                                      font=("Consolas", 32, "bold"), 
                                      bg="#334155", fg="#22d3ee")
        self.distance_value.pack(pady=(0, 15))
        
    def create_metric(self, parent, label, data_key, unit, color, bar_color, max_val):
        """
        Create a metric display with progress bar
        
        Args:
            parent: Parent frame
            label: Display name of the metric
            data_key: Key to store metric data
            unit: Unit of measurement (V, A, °C, etc.)
            color: Text color in hex
            bar_color: Progress bar color in hex
            max_val: Maximum value for progress bar scale
        """
        # Container
        container = tk.Frame(parent, bg="#1e293b")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        # Label and value
        top_frame = tk.Frame(container, bg="#1e293b")
        top_frame.pack(fill=tk.X, pady=(0, 5))
        
        name_label = tk.Label(top_frame, text=label, font=("Consolas", 10),
                             bg="#1e293b", fg=color)
        name_label.pack(side=tk.LEFT)
        
        value_label = tk.Label(top_frame, text=f"0 {unit}", 
                              font=("Consolas", 10, "bold"),
                              bg="#1e293b", fg=color)
        value_label.pack(side=tk.RIGHT)
        
        # Progress bar background
        bar_bg = tk.Canvas(container, height=12, bg="#334155", 
                          highlightthickness=1,
                          highlightbackground=bar_color)
        bar_bg.pack(fill=tk.X)
        
        # Progress bar fill
        bar_fill = bar_bg.create_rectangle(0, 0, 0, 12, fill=bar_color, outline="")
        
        # Store references
        self.metrics[data_key] = {
            'value_label': value_label,
            'bar_canvas': bar_bg,
            'bar_fill': bar_fill,
            'unit': unit,
            'max_val': max_val,
            'color': color
        }
        
    def update(self, lim_temp, lim_volt, lim_cur, inverter_volt, brake1, brake2, distance):
        """
        Update all metrics and brake status
        
        Args:
            lim_temp: LIM temperature in Celsius
            lim_volt: LIM voltage in Volts
            lim_cur: LIM current in Amperes
            inverter_volt: Inverter voltage in Volts
            brake1: Brake 1 status (True=deployed, False=undeployed)
            brake2: Brake 2 status (True=deployed, False=undeployed)
            distance: Distance traveled in meters
        """
        data = {
            'lim_temp': lim_temp,
            'lim_volt': lim_volt,
            'lim_cur': lim_cur,
            'inverter_volt': inverter_volt
        }
        
        # Update LIM metrics
        for key, value in data.items():
            if key in self.metrics:
                metric = self.metrics[key]
                metric['value_label'].config(text=f"{int(value)} {metric['unit']}")
                
                # Update progress bar
                width = metric['bar_canvas'].winfo_width()
                if width > 1:  # Make sure canvas is rendered
                    fill_width = (value / metric['max_val']) * width
                    metric['bar_canvas'].coords(metric['bar_fill'], 0, 0, fill_width, 12)
        
        # Update brake statuses
        self.update_brake_status(1, brake1)
        self.update_brake_status(2, brake2)
        
        # Update distance
        self.distance_value.config(text=f"{int(distance)} m")
        
    def update_brake_status(self, brake_num, deployed):
        """
        Update brake status indicator
        
        Args:
            brake_num: Brake number (1 or 2)
            deployed: Boolean indicating if brake is deployed
        """
        if brake_num == 1:
            indicator = self.brake1_indicator
            circle = self.brake1_circle
            status_label = self.brake1_status
        else:
            indicator = self.brake2_indicator
            circle = self.brake2_circle
            status_label = self.brake2_status
        
        if deployed:
            indicator.itemconfig(circle, fill="#ef4444")
            status_label.config(text="DEPLOYED", fg="#ef4444")
        else:
            indicator.itemconfig(circle, fill="#22c55e")
            status_label.config(text="UNDEPLOYED", fg="#22c55e")


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("LIM & Brake System Test")
    root.geometry("1200x700")
    root.configure(bg="#0f172a")
    
    panel = LIMBrakePanel(root)
    
    # Test update
    def test_update():
        import random
        panel.update(
            lim_temp=67 + random.randint(-5, 5),
            lim_volt=475 + random.randint(-10, 10),
            lim_cur=128 + random.randint(-10, 10),
            inverter_volt=631 + random.randint(-5, 5),
            brake1=random.choice([True, False]),
            brake2=random.choice([True, False]),
            distance=2841 + random.randint(0, 100)
        )
        root.after(1000, test_update)
    
    test_update()
    root.mainloop()