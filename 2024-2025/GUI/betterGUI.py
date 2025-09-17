import sys
import socket
import threading
import json
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtGui import QPixmap, QImage, QFont

HOST_IP = "192.168.x.x"
TCP_PORT = 5000
CMD_FILE = "C:/Users/user/Documents/Coding Projects/GUI/TMUHyperloop/2024-2025/GUI/commands.txt"
DATA_FILE = "C:/Users/user/Documents/Coding Projects/GUI/TMUHyperloop/2024-2025/GUI/data.txt"
# Control Station GUI Backend code (running on laptop)

class HyperloopControlGUI(QMainWindow):

    def __init__(self, d_lock: threading.Lock, c_lock: threading.Lock):
        super().__init__()
        self.D_LOCK = d_lock
        self.C_LOCK = c_lock
        
        self.setWindowTitle("Pod Control")
        self.setGeometry(100, 100, 500, 600)  # Increased size for connection status

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.command_window = QTextEdit()

        main_layout = QVBoxLayout()

        # Start and stop buttons side by side
        button_layout = QHBoxLayout()
        button_layout2 = QHBoxLayout()
        image_layout = QHBoxLayout()
        title_layout = QHBoxLayout()
        title_layout2 = QHBoxLayout()
        LIM_title_layout = QHBoxLayout()
        bat1_2_vLayout = QHBoxLayout()
        bat1_2_cLayout = QHBoxLayout()
        bat1_2_tLayout = QHBoxLayout()
        bat3_4_vLayout = QHBoxLayout()
        bat3_4_cLayout = QHBoxLayout()
        bat3_4_tLayout = QHBoxLayout()
        LIM_Layout = QHBoxLayout()
        brake_title_layout = QHBoxLayout()
        brake_layout = QHBoxLayout()
        state_title_layout = QHBoxLayout()
        state_layout = QHBoxLayout()
        speed_layout = QHBoxLayout()
        speedDisplay_layout = QHBoxLayout()
        pos_pressure_layout = QHBoxLayout()
        posPressureDisplay_layout = QHBoxLayout()
        inverter_layout = QVBoxLayout()
        commandwindow_layout = QVBoxLayout()

        # Style definitions
        button_style = "QPushButton { padding: 8px; font-weight: bold; }"
        green_button_style = button_style + " QPushButton { background-color: #1E8939; color: white; }"
        red_button_style = button_style + " QPushButton { background-color: #E11313; color: white; }"
        blue_button_style = button_style + " QPushButton { background-color: #2196F3; color: white; }"
        display_style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        state_style = "QLabel { border: 1px solit gray; background-color: #1E1E1E; color: white: padding: 5px; font: 18pt; }"
        
        # Control buttons
        self.launch_button = QPushButton("Launch")
        self.launch_button.setStyleSheet(green_button_style)
        self.launch_button.clicked.connect(self.on_launch)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(red_button_style)
        self.stop_button.clicked.connect(self.on_stop)

        self.e_stop_button = QPushButton("STOP NOW")
        self.e_stop_button.setStyleSheet(red_button_style)
        self.e_stop_button.clicked.connect(self.on_e_stop)

        self.ready_button = QPushButton("Prep for Launch")
        self.ready_button.setStyleSheet(blue_button_style)
        self.ready_button.clicked.connect(self.on_ready)

        self.cancel_button = QPushButton("Abort Launch")
        self.cancel_button.setStyleSheet(red_button_style)
        self.cancel_button.clicked.connect(self.on_Cancel)

        self.reset_fault_button = QPushButton("Reset Fault")
        self.reset_fault_button.setStyleSheet(blue_button_style)
        self.reset_fault_button.clicked.connect(self.on_fault_reset)

        # Hyperloop logo
        self.image_label = QLabel()
        image_path = "miku.jpg"
        pixmap = QPixmap()
        pixmap.load(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignHCenter)
    
        image_layout.addWidget(self.image_label)

        # Add buttons to layout
        button_layout.addWidget(self.ready_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.launch_button)
        
        button_layout2.addWidget(self.stop_button)
        button_layout2.addWidget(self.e_stop_button)
        button_layout2.addWidget(self.reset_fault_button)
        
        # Connection status layout

        # Displays for voltage and current
        self.bat1_display = QLabel("Battery 1:")
        self.bat1_volt = QLabel("Voltage: N/A V")
        self.bat1_volt.setStyleSheet(display_style)
        self.bat1_cur = QLabel("Current: N/A A")
        self.bat1_cur.setStyleSheet(display_style)
        self.bat1_temp = QLabel("Temperature: N/A °C")
        self.bat1_temp.setStyleSheet(display_style)

        self.bat2_display = QLabel("Battery 2:")
        self.bat2_volt = QLabel("Voltage: N/A V")
        self.bat2_volt.setStyleSheet(display_style)
        self.bat2_cur = QLabel("Current: N/A A")
        self.bat2_cur.setStyleSheet(display_style)
        self.bat2_temp = QLabel("Temperature: N/A °C")
        self.bat2_temp.setStyleSheet(display_style)

        self.bat3_display = QLabel("Battery 3:")
        self.bat3_volt = QLabel("Voltage: N/A V")
        self.bat3_volt.setStyleSheet(display_style)
        self.bat3_cur = QLabel("Current: N/A A")
        self.bat3_cur.setStyleSheet(display_style)
        self.bat3_temp = QLabel("Temperature: N/A °C")
        self.bat3_temp.setStyleSheet(display_style)

        self.bat4_display = QLabel("Battery 4:")
        self.bat4_volt = QLabel("Voltage: N/A V")
        self.bat4_volt.setStyleSheet(display_style)
        self.bat4_cur = QLabel("Current: N/A A")
        self.bat4_cur.setStyleSheet(display_style)
        self.bat4_temp = QLabel("Temperature: N/A °C")
        self.bat4_temp.setStyleSheet(display_style)

        title_layout.addWidget(self.bat1_display)
        title_layout.addWidget(self.bat2_display)

        bat1_2_vLayout.addWidget(self.bat1_volt)
        bat1_2_vLayout.addWidget(self.bat2_volt)
        bat1_2_cLayout.addWidget(self.bat1_cur)
        bat1_2_cLayout.addWidget(self.bat2_cur)
        bat1_2_tLayout.addWidget(self.bat1_temp)
        bat1_2_tLayout.addWidget(self.bat2_temp)

        bat3_4_vLayout.addWidget(self.bat3_volt)
        bat3_4_vLayout.addWidget(self.bat4_volt)
        bat3_4_cLayout.addWidget(self.bat3_cur)
        bat3_4_cLayout.addWidget(self.bat4_cur)
        bat3_4_tLayout.addWidget(self.bat3_temp)
        bat3_4_tLayout.addWidget(self.bat4_temp)

        title_layout2.addWidget(self.bat3_display)
        title_layout2.addWidget(self.bat4_display)

        self.limDisplay = QLabel("LIM:")
        self.limVolt = QLabel("Voltage: N/A V")
        self.limVolt.setStyleSheet(display_style)
        self.limCur = QLabel("Current: N/A A")
        self.limCur.setStyleSheet(display_style)
        self.limTemp = QLabel("Temperature: N/A °C")
        self.limTemp.setStyleSheet(display_style)

        LIM_title_layout.addWidget(self.limDisplay)
        LIM_Layout.addWidget(self.limVolt)
        LIM_Layout.addWidget(self.limCur)
        LIM_Layout.addWidget(self.limTemp)

        self.brakeDisplay = QLabel("Brake Position:")
        self.brake_1_pos = QLabel("Deployed")
        self.brake_1_pos.setStyleSheet(display_style)
        self.brake_2_pos = QLabel("Deployed")
        self.brake_2_pos.setStyleSheet(display_style)

        brake_title_layout.addWidget(self.brakeDisplay)
        brake_layout.addWidget(self.brake_1_pos)
        brake_layout.addWidget(self.brake_2_pos)

        self.stateDisplay = QLabel("Current State:")
        self.state = QLabel("Safe to Approach")
        self.state.setStyleSheet(display_style)
        self.state.setFont(QFont("Arial", 18))

        state_title_layout.addWidget(self.stateDisplay)
        state_layout.addWidget(self.state)

        # Other Stuff
        self.velocity = QLabel("Velocity")
        self.CS_display = QLabel("N/A m/s")
        self.CS_display.setStyleSheet(display_style)
        self.distance_traveled = QLabel("Distance Traveled")
        self.Pos_display = QLabel ("0 m")
        self.Pos_display.setStyleSheet(display_style)

        # New display for inverter voltage
        self.inverter_display = QLabel("Inverter Voltage:")
        self.inverter_voltage = QLabel("Voltage: N/A V")
        self.inverter_voltage.setStyleSheet(display_style)

        inverter_layout.addWidget(self.inverter_display)
        inverter_layout.addWidget(self.inverter_voltage)

        speed_layout.addWidget(self.velocity)
        speedDisplay_layout.addWidget(self.CS_display)
        pos_pressure_layout.addWidget(self.distance_traveled)
        posPressureDisplay_layout.addWidget(self.Pos_display)

        # Add command window
        self.commands_label = QLabel("Command Log:")
        self.command_window = QTextEdit()
        self.command_window.setReadOnly(True)
        commandwindow_layout.addWidget(self.commands_label)
        commandwindow_layout.addWidget(self.command_window)

        # Create a dictionary to use as a local scope for code execution
        self.console_locals = {}

        # Add widgets to the layout
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)
        main_layout.addLayout(state_title_layout)
        main_layout.addLayout(state_layout)
        
        #main_layout.addLayout(title_layout)
        #main_layout.addLayout(bat1_2_vLayout)
        #main_layout.addLayout(bat1_2_cLayout)
        #main_layout.addLayout(bat1_2_tLayout)

        #main_layout.addLayout(title_layout2)
        #main_layout.addLayout(bat3_4_vLayout)
        #main_layout.addLayout(bat3_4_cLayout)
        #main_layout.addLayout(bat3_4_tLayout)

        main_layout.addLayout(LIM_title_layout)
        main_layout.addLayout(LIM_Layout)

        main_layout.addLayout(brake_title_layout)
        main_layout.addLayout(brake_layout)

        main_layout.addLayout(speed_layout)
        main_layout.addLayout(speedDisplay_layout)
        main_layout.addLayout(pos_pressure_layout)
        main_layout.addLayout(posPressureDisplay_layout)
        main_layout.addLayout(inverter_layout)
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

    def log_command(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.command_window.append(f"[{timestamp}] {message}")

    def improveGUI(self):
        # input list
        self.D_LOCK.acquire()
        with open(DATA_FILE, "r") as d:
            data = d.read().split(',')
        self.D_LOCK.release()
        try:
            (bat1_temp, bat1_volt, bat1_cur,
             bat2_temp, bat2_volt, bat2_cur,
             bat3_temp, bat3_volt, bat3_cur,
             bat4_temp, bat4_volt, bat4_cur,
             lim_temp, lim_volt, lim_cur,
             brake1_deployed, brake2_deployed,
             velocity, distance_traveled, state,
             inverter_volt) = data  # New inverter voltage added

            # Update inverter voltage display
            self.inverter_voltage.setText(f"Voltage: {inverter_volt} V")

            # battery 1 values (temp, voltage, current)
            self.bat1_temp.setText(f"Temperature: {bat1_temp} °C")
            self.bat1_volt.setText(f"Voltage: {bat1_volt} V")
            self.bat1_cur.setText(f"Current: {bat1_cur} A")
            # battery 2 values
            self.bat2_temp.setText(f"Temperature: {bat2_temp} °C")
            self.bat2_volt.setText(f"Voltage: {bat2_volt} V")
            self.bat2_cur.setText(f"Current: {bat2_cur} A")

            # battery 3 values
            self.bat3_temp.setText(f"Temperature: {bat3_temp} °C")
            self.bat3_volt.setText(f"Voltage: {bat3_volt} V")
            self.bat3_cur.setText(f"Current: {bat3_cur} A")

            # battery 4 values
            self.bat4_temp.setText(f"Temperature: {bat4_temp} °C")
            self.bat4_volt.setText(f"Voltage: {bat4_volt} V")
            self.bat4_cur.setText(f"Current: {bat4_cur} A")

            # updated LIM values
            self.limTemp.setText(f"Temperature: {lim_temp} °C")
            self.limVolt.setText(f"Voltage: {lim_volt} V")
            self.limCur.setText(f"Current: {lim_cur} A")

            # updated break positions
            self.brake_1_pos.setText("Deployed" if brake1_deployed else "Retracted")
            self.brake_2_pos.setText("Deployed" if brake2_deployed else "Retracted")

            # updated velocity/position
            self.CS_display.setText(f"{velocity} m/s")
            self.Pos_display.setText(f"{distance_traveled} m")

            # updated pod state
            self.state.setText(state)
        except Exception as e:
            self.log_command(f"Error updating GUI with received data: {str(e)}")

    def on_launch(self):
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("GO")
        self.C_LOCK.release()
        self.log_command("Launch command sent")
        
    def on_stop(self):
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("STOP")
        self.C_LOCK.release()
        self.log_command("Stop command sent")
    
    def on_e_stop(self): # link to STOP NOW button
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("STOP_NOW")
        self.C_LOCK.release()
        self.log_command("E-STOP")
    
    def on_ready(self): # Link to ready button
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("READY")
        self.C_LOCK.release()
        self.log_command("Prep launch command sent")
    
    def on_Cancel(self): # link to abort launch button
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("ABORT")
        self.C_LOCK.release()
        self.log_command("Cancel launch command sent")
    
    def on_fault_reset(self): # link to reset fault button
        self.C_LOCK.acquire()
        with open(CMD_FILE, "w") as c:
            c.write("RESET_FAULT")
        self.C_LOCK.release()
        self.log_command("Fault reset command sent")

    def closeEvent(self, event):
        super().closeEvent(event)


def main(data_lock: threading.Lock, commands_lock: threading.Lock):
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI(data_lock, commands_lock)
    window.show()
    # Example data to update the GUI, including inverter voltage
    '''    example_data = [
        25.0, 48.5, 10.2,  # Battery 1
        26.5, 48.1, 10.0,  # Battery 2
        27.0, 48.7, 10.5,  # Battery 3
        25.5, 48.2, 10.1,  # Battery 4
        60.0, 400.0, 15.0,  # LIM
        True, False,         # Brakes
        300.5, 1200.0,       # Speed and position
        "Safe to Approach",  # State
        220.0                # Inverter voltage
    ]
    '''
    def update():
        window.improveGUI()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    sys.exit(app.exec())

if __name__ == "__main__":
    main(threading.Lock(), threading.Lock())