import sys
import socket
import threading
import json
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit, QMessageBox
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtGui import QPixmap

# Custom signal class for thread-safe communication
class TCPSignals(QObject):
    data_received = Signal(list)
    connection_status = Signal(bool, str)

class HyperloopControlGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # TCP Client Configuration
        self.tcp_client = None
        self.tcp_thread = None
        self.tcp_connected = False
        self.tcp_signals = TCPSignals()
        self.tcp_signals.data_received.connect(self.improveGUI)
        self.tcp_signals.connection_status.connect(self.update_connection_status)
        
        # Server details
        self.tcp_host = "127.0.0.1"  # Default to localhost
        self.tcp_port = 5000         # Default port
        
        self.setWindowTitle("Pod Control")
        self.setGeometry(100, 100, 500, 600)  # Increased size for connection status

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.command_window = QTextEdit()

        main_layout = QVBoxLayout()

        # Start and stop buttons side by side
        button_layout = QHBoxLayout()
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
        inverter_layout = QHBoxLayout()
        connection_layout = QHBoxLayout()
        commandwindow_layout = QVBoxLayout()

        # Style definitions
        button_style = "QPushButton { padding: 8px; font-weight: bold; }"
        green_button_style = button_style + " QPushButton { background-color: #1E8939; color: white; }"
        red_button_style = button_style + " QPushButton { background-color: #E11313; color: white; }"
        blue_button_style = button_style + " QPushButton { background-color: #2196F3; color: white; }"
        display_style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        
        # Control buttons
        self.launch_button = QPushButton("Launch")
        self.launch_button.setStyleSheet(green_button_style)
        self.launch_button.clicked.connect(self.on_launch)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(red_button_style)
        self.stop_button.clicked.connect(self.on_stop)
        
        # TCP Connection button
        self.connect_button = QPushButton("Connect TCP")
        self.connect_button.setStyleSheet(blue_button_style)
        self.connect_button.clicked.connect(self.toggle_tcp_connection)
        
        # Connection status
        self.connection_status = QLabel("Not Connected")
        self.connection_status.setStyleSheet("QLabel { color: red; font-weight: bold; }")

        # Hyperloop logo
        self.image_label = QLabel()
        try:
            image_path = "Hyperloop_logo_W.png"
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        except:
            self.image_label.setText("Logo not found")
            self.image_label.setAlignment(Qt.AlignCenter)

        # Add buttons to layout
        button_layout.addWidget(self.launch_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.connect_button)
        
        # Connection status layout
        connection_layout.addWidget(QLabel("Connection Status:"))
        connection_layout.addWidget(self.connection_status)

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
        main_layout.addLayout(button_layout)
        main_layout.addLayout(connection_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(title_layout) 
        main_layout.addLayout(bat1_2_vLayout)
        main_layout.addLayout(bat1_2_cLayout)
        main_layout.addLayout(bat1_2_tLayout)

        main_layout.addLayout(title_layout2)
        main_layout.addLayout(bat3_4_vLayout)
        main_layout.addLayout(bat3_4_cLayout)
        main_layout.addLayout(bat3_4_tLayout)

        main_layout.addLayout(LIM_title_layout)
        main_layout.addLayout(LIM_Layout)

        main_layout.addLayout(brake_title_layout)
        main_layout.addLayout(brake_layout)

        main_layout.addLayout(state_title_layout)
        main_layout.addLayout(state_layout)

        main_layout.addLayout(speed_layout)
        main_layout.addLayout(speedDisplay_layout)
        main_layout.addLayout(pos_pressure_layout)
        main_layout.addLayout(posPressureDisplay_layout)
        main_layout.addLayout(inverter_layout)
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

    def toggle_tcp_connection(self):
        if not self.tcp_connected:
            self.start_tcp_client()
        else:
            self.stop_tcp_client()

    def start_tcp_client(self):
        if self.tcp_connected:
            return
        
        self.tcp_thread = threading.Thread(target=self.tcp_client_thread)
        self.tcp_thread.daemon = True
        self.tcp_thread.start()
        self.log_command("Starting TCP client connection...")

    def stop_tcp_client(self):
        if self.tcp_connected and self.tcp_client:
            self.tcp_connected = False
            try:
                self.tcp_client.close()
            except:
                pass
            self.log_command("TCP connection closed")
            self.update_connection_status(False, "Connection closed")

    def tcp_client_thread(self):
        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.settimeout(5)  # 5 second timeout for connection attempts
            self.tcp_client.connect((self.tcp_host, self.tcp_port))
            
            self.tcp_connected = True
            self.tcp_signals.connection_status.emit(True, "Connected to server")
            self.log_command(f"Connected to server at {self.tcp_host}:{self.tcp_port}")
            
            # Main receive loop
            self.tcp_client.settimeout(1)  # 1-second timeout for receiving data
            while self.tcp_connected:
                try:
                    data = self.tcp_client.recv(4096)
                    if not data:
                        # Connection closed by server
                        break
                    
                    # Try to parse JSON data
                    try:
                        sensor_data = json.loads(data.decode('utf-8'))
                        self.tcp_signals.data_received.emit(sensor_data)
                        self.log_command("Received data update")
                    except json.JSONDecodeError:
                        self.log_command(f"Error decoding JSON data: {data.decode('utf-8')}")
                        
                except socket.timeout:
                    # This is normal, just continue the loop
                    continue
                except Exception as e:
                    if self.tcp_connected:  # Only log if we're still supposed to be connected
                        self.log_command(f"Error receiving data: {str(e)}")
                    break
                    
            # If we exit the loop, make sure we're properly disconnected
            self.tcp_connected = False
            self.tcp_signals.connection_status.emit(False, "Disconnected")
            
        except Exception as e:
            self.tcp_signals.connection_status.emit(False, f"Connection error: {str(e)}")
            self.log_command(f"TCP connection error: {str(e)}")
    
    def update_connection_status(self, is_connected, message):
        if is_connected:
            self.connection_status.setText("Connected")
            self.connection_status.setStyleSheet("QLabel { color: green; font-weight: bold; }")
            self.connect_button.setText("Disconnect")
        else:
            self.connection_status.setText(message)
            self.connection_status.setStyleSheet("QLabel { color: red; font-weight: bold; }")
            self.connect_button.setText("Connect TCP")
            self.tcp_connected = False

    def log_command(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.command_window.append(f"[{timestamp}] {message}")

    def improveGUI(self, sensor_data):
        # input list
        try:
            (bat1_temp, bat1_volt, bat1_cur,
             bat2_temp, bat2_volt, bat2_cur,
             bat3_temp, bat3_volt, bat3_cur,
             bat4_temp, bat4_volt, bat4_cur,
             lim_temp, lim_volt, lim_cur,
             brake1_deployed, brake2_deployed,
             velocity, distance_traveled, state,
             inverter_volt) = sensor_data  # New inverter voltage added

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
        self.log_command("Launch command sent")
        if self.tcp_connected and self.tcp_client:
            try:
                self.tcp_client.send(json.dumps({"command": "launch"}).encode('utf-8'))
            except Exception as e:
                self.log_command(f"Error sending launch command: {str(e)}")
        else:
            self.log_command("Not connected to server - launch command not sent")

    def on_stop(self):
        self.log_command("Stop command sent")
        if self.tcp_connected and self.tcp_client:
            try:
                self.tcp_client.send(json.dumps({"command": "stop"}).encode('utf-8'))
            except Exception as e:
                self.log_command(f"Error sending stop command: {str(e)}")
        else:
            self.log_command("Not connected to server - stop command not sent")

    def closeEvent(self, event):
        self.stop_tcp_client()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI()
    window.show()

    # Example data to update the GUI, including inverter voltage
    example_data = [
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
    window.improveGUI(example_data)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()