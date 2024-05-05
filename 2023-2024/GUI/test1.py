import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import threading
from threading import Thread
import datetime
import socket

class HyperloopControlGUI(QMainWindow):
    def __init__(self, event):
        super().__init__()

        self.setWindowTitle("Joever")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.command_window = QTextEdit()

        main_layout = QVBoxLayout()

        # Start and stop buttons side by side
        button_layout = QHBoxLayout()
        title_layout = QHBoxLayout()
        title_layout2 = QHBoxLayout()
        voltage_layout = QHBoxLayout()
        current_layout = QHBoxLayout()
        TempDisplay_layout = QHBoxLayout()
        TempDisplay_layout2 = QHBoxLayout() 
        speed_layout = QHBoxLayout()
        speedDisplay_layout = QHBoxLayout()
        pos_pressure_layout = QHBoxLayout()
        posPressureDisplay_layout = QHBoxLayout()
        commandwindow_layout = QVBoxLayout()

        style = "QPushButton { background-color: #1E8939; color: white; }"
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(style)
        style = "QPushButton { background-color: #E11313; color: white; }"
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style)

        self.image_label = QLabel()
        image_path = "Hyperloop_logo_W.png"
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


        button_layout.addWidget(self.start_button)

        button_layout.addWidget(self.stop_button)

        # Displays for voltage and current
        style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        self.battery_display = QLabel("Battery Display:")
        self.voltage_display = QLabel("Voltage: N/A V")
        self.voltage_display.setStyleSheet(style)
        self.current_display = QLabel("Current: N/A A")
        self.current_display.setStyleSheet(style)
        self.temp_display = QLabel("Temperature: N/A °C")
        self.temp_display.setStyleSheet(style)
        self.linear = QLabel("Linear Induction Motor:")
        self.voltage_display2 = QLabel("Voltage: N/A V")
        self.voltage_display2.setStyleSheet(style)
        self.current_display2 = QLabel("Current: N/A A")
        self.current_display2.setStyleSheet(style)
        self.temp_display2 = QLabel("Temperature: N/A °C")
        self.temp_display2.setStyleSheet(style)
        self.pod = QLabel("Pod:")
        self.voltage_display3 = QLabel("Voltage: N/A V")
        self.voltage_display3.setStyleSheet(style)
        self.current_display3 = QLabel("Current: N/A A")
        self.current_display3.setStyleSheet(style)
        self.SBL_display = QLabel("SBL")
        self.temp_display3 = QLabel("Temperature: N/A °C")
        self.temp_display3.setStyleSheet(style)
        self.ambiant = QLabel("Ambiant")
        self.temp_display4 = QLabel("Temperature: N/A °C")
        self.temp_display4.setStyleSheet(style)

        title_layout.addWidget(self.battery_display)
        title_layout.addWidget(self.linear)
        voltage_layout.addWidget(self.voltage_display)
        voltage_layout.addWidget(self.voltage_display2)
        current_layout.addWidget(self.current_display)
        current_layout.addWidget(self.current_display2)
        TempDisplay_layout.addWidget(self.temp_display)
        TempDisplay_layout.addWidget(self.temp_display2)
        title_layout2.addWidget(self.SBL_display)
        title_layout2.addWidget(self.ambiant)
        TempDisplay_layout2.addWidget(self.temp_display3)
        TempDisplay_layout2.addWidget(self.temp_display4)

        #Other Stuff
        self.target_speed = QLabel("Target Speed")
        self.TS_display = QLabel("N/A m/s")
        self.TS_display.setStyleSheet(style)
        self.current_speed = QLabel("Current Speed")
        self.CS_display = QLabel("N/A m/s")
        self.CS_display.setStyleSheet(style)
        self.acceleration = QLabel("Acceleration")
        self.A_display = QLabel("N/A m/s^2")
        self.A_display.setStyleSheet(style)
        self.position = QLabel("Position")
        self.Pos_display = QLabel ("North/East/South/West")
        self.Pos_display.setStyleSheet(style)
        self.pressure = QLabel ("Pressure")
        self.P_display = QLabel("N/A N/M^2")
        self.P_display.setStyleSheet(style)

        speed_layout.addWidget(self.target_speed)
        speed_layout.addWidget(self.current_speed)
        speed_layout.addWidget(self.acceleration)
        speedDisplay_layout.addWidget(self.TS_display)
        speedDisplay_layout.addWidget(self.CS_display)
        speedDisplay_layout.addWidget(self.A_display)
        pos_pressure_layout.addWidget(self.position)
        pos_pressure_layout.addWidget(self.pressure)
        posPressureDisplay_layout.addWidget(self.Pos_display)
        posPressureDisplay_layout.addWidget(self.P_display)


        # Slider for voltage control
        self.voltage_slider = QSlider(Qt.Horizontal)
        self.voltage_slider.setRange(0, 5000)
        self.voltage_slider.setValue(0)
        self.voltage_slider.setTickPosition(QSlider.TicksBelow)
        self.voltage_slider.setTickInterval(10)
        self.voltage_slider.valueChanged.connect(self.update_voltage_display)


        # Console Command Button and Window
        self.command = QLabel("Command Block:")
        style = "QPushButton { background-color: #004c9b; color: yellow; }"
        self.command_button = QPushButton("Enter")
        self.command_button.setStyleSheet(style)
        commandwindow_layout.addWidget(self.command)
        commandwindow_layout.addWidget(self.command_window)
        commandwindow_layout.addWidget(self.command_button)
        

        # Connect buttons to their respective functions
        self.start_button.clicked.connect(self.start_train)
        self.stop_button.clicked.connect(self.stop_train)
        self.command_button.clicked.connect(self.user_input)

        # Define dataRead event
        self.dataWasReadEvent = event
        self.checkThreadTimer = QTimer()
        # Check every .5 seconds
        self.checkThreadTimer.start(500)
        self.checkThreadTimer.timeout.connect(self.update_values)

        # Create a dictionary to use as a local scope for code execution
        self.console_locals = {}

        # Add widgets to the layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(title_layout) 
        main_layout.addLayout(voltage_layout)
        main_layout.addLayout(current_layout)
        main_layout.addLayout(TempDisplay_layout)
        main_layout.addLayout(title_layout2) 
        main_layout.addLayout(TempDisplay_layout2)
        main_layout.addWidget(self.pod)
        main_layout.addWidget(self.voltage_display3)
        main_layout.addWidget(self.current_display3)
        main_layout.addLayout(speed_layout)
        main_layout.addLayout(speedDisplay_layout)
        main_layout.addLayout(pos_pressure_layout)
        main_layout.addLayout(posPressureDisplay_layout)
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

        

    def update_voltage_display(self):
        voltage = self.voltage_slider.value()

    def start_train(self):
        # Implement code to start the train or perform relevant actions
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: JOEVER V")
        self.current_display.setText("Current: JOEVER A")
        self.temp_display.setText("Temperature: JOEVER °C")
        self.voltage_display2.setText(f"Voltage: JOEVER V")
        self.current_display2.setText("Current: JOEVER A")
        self.temp_display2.setText("Temperature: JOEVER °C")
        self.temp_display3.setText("Temperature: JOEVER °C")
        self.temp_display4.setText("Temperature: JOEVER °C")
        self.voltage_display3.setText(f"Voltage: JOEVER V")
        self.current_display3.setText("Current: JOEVER A")
        self.TS_display.setText("North")


    def stop_train(self):
        # Implement code to stop the train or perform relevant actions
        # Send E-Stop signal to pod
        # Kill power to lim
        # Apply Brakes

        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: 0 A")
        self.temp_display.setText("Temperature: 0 °C")
        self.voltage_display2.setText(f"Voltage: {voltage} V")
        self.current_display2.setText("Current: 0 A")
        self.temp_display2.setText("Temperature: 0 °C")
        self.temp_display3.setText("Temperature: 0 °C")
        self.temp_display4.setText("Temperature: 0 °C")
        self.voltage_display3.setText(f"Voltage: {voltage} V")
        self.current_display3.setText("Current: 0 A")

    def user_input(self):
        # Implement code to print user input in command block
        print(self.command_window.toPlainText())
        # Send command to pod
        try:
            self.s.sendall(bytes(self.command_window.toPlainText(), 'utf-8'))
            print("Sent")
        except:
            print("Error")
        
        

    def update_values(self):
        # Check if data was read
        if self.dataWasReadEvent:
            file = open('2023-2024\GUI\data.txt', 'r')
            line = file.readline()
            data = line.split(',')
            file.close()
            # take values and update them
            self.voltage_display.setText(f"Voltage: {data[0]} V")
            self.voltage_display2.setText(f"Voltage: {data[1]} V")
            self.voltage_display3.setText(f"Voltage: {data[2]} V")
            self.current_display.setText(f"Current: {data[3]} A")
            self.current_display2.setText(f"Current: {data[4]} A")
            self.current_display3.setText(f"Current: {data[5]} A")
            self.temp_display.setText(f"Temperature: {data[6]} °C")
            self.temp_display2.setText(f"Temperature: {data[7]} °C")
            self.temp_display3.setText(f"Temperature: {data[8]} °C")
            self.temp_display4.setText(f"Temperature: {data[9]} °C")
            self.dataWasReadEvent.clear()
        
        

def main(dataReadEvent, appCloseEvent):
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI(dataReadEvent)
    window.show()
    if(app.exec()):
        appCloseEvent.set()
    sys.exit()

def readData(dataReadEvent, appCloseEvent, conn: socket):
    delay1 = datetime.datetime.now()
    # Write data to data.txt
    try:
        data = conn.recv(1024)
    except:
        print("An Exception Occured: {e}")

    dtxt = open("data.txt", 'wb')
    dtxt.write(data)
    dtxt.close()
    delay2 = datetime.datetime.now()
    differencetime = (delay2 - delay1).total_seconds()
    writedelay = int(5)
    restart = (writedelay - differencetime)
    dataReadEvent.set()
    if appCloseEvent:
        sys.exit()
    threading.Timer(restart, readData, args=(dataReadEvent, conn)).start()    

if __name__ == "__main__":
    dataReadEvent = threading.Event()
    appCloseEvent = threading.Event()
    dataReadEvent.clear()
    appCloseEvent.clear()
    
    HOST = "172.20.10.10"  # Standard loopback interface address (localhost)
    PORT = 65431  # Port to listen on (non-privileged ports are > 1023)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {conn}")
            
            data = conn.recv(1024)
            print(data)
            #Thread(target = main, args=(dataReadEvent, appCloseEvent) ).start()
        
        """while True:
            delay1 = datetime.datetime.now()
            # Write data to data.txt
            with conn:
                try:
                    data = conn.recv(1024)
                    print(data)
                except Exception as e:
                    print("An Exception Occured: {e}")
            
            dtxt = open("data.txt", 'wb')
            dtxt.write(data)
            dtxt.close()
            delay2 = datetime.datetime.now()
            differencetime = (delay2 - delay1).total_seconds()
            writedelay = int(5)
            restart = (writedelay - differencetime)
            dataReadEvent.set()
            if appCloseEvent:
                sys.exit()
                """