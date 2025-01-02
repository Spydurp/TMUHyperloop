import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import threading
from threading import Thread
import datetime
import socket
import time

DATAFILE = "C:/Users/alexm/OneDrive/Desktop/Hyperloop/TMUHyperloop/2023-2024/GUI/data.txt"
COMOUT = "!"
appCloseEvent = False
dataReadEvent = False   

class HyperloopControlGUI(QMainWindow):

    def __init__(self):
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
        self.launch_button = QPushButton("Launch")
        self.launch_button.setStyleSheet(style)
        style = "QPushButton { background-color: #E11313; color: white; }"
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style)

        self.image_label = QLabel()
        image_path = "Hyperloop_logo_W.png"
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


        button_layout.addWidget(self.launch_button)

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
        self.launch_button.clicked.connect(self.launch_train)
        self.stop_button.clicked.connect(self.stop_train)
        self.command_button.clicked.connect(self.user_input)

        # Define dataRead event
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

    def launch_train(self):
        # Send Launch Command
        global COMOUT
        COMOUT = COMOUT + " G"
        print("Launch")
        


    def stop_train(self):
        # Send E-STOP Command
        global COMOUT
        COMOUT = COMOUT + " X"
        print("Stop")

    def user_input(self):
        global COMOUT
        # Implement code to print user input in command block
        COMOUT = COMOUT + " " + self.command_window.toPlainText()
        print(self.command_window.toPlainText())
        # Send command to pod
        

    def update_values(self):
        global dataReadEvent
        # Check if data was read
        if dataReadEvent:
            file = open('2023-2024/GUI/testData.txt', 'r')
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
            dataReadEvent = False    

def main():
    global appCloseEvent
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI()
    window.show()
    if not app.exec():
        appCloseEvent = True
        sys.exit()

# Delete later if unneccessary
def readData(conn: socket):
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
    dataReadEvent = True
    if appCloseEvent:
        sys.exit()
    threading.Timer(restart, readData, args=(dataReadEvent, conn)).start()    


if __name__ == '__main__':
    Thread(target = main, args=()).start()
    
    HOST = "172.20.10.3"  # Standard loopback interface address (localhost)
    PORT = 65431  # Port to listen on (non-privileged ports are > 1023)
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {conn}")
                while True:
                    data = conn.recv(1024)
                    print(data)
                    conn.sendall(bytes(COMOUT, 'utf-8'))
                    COMOUT = "!" # After sending command, reset COMOUT to connection confirmation character
                    if data:
                        dtxt = open(DATAFILE, 'w')
                        dtxt.write("Test\n")
                        dtxt.write(data.decode('utf-8'))
                        dtxt.close()
                        dataReadEvent = True
                    # Send commands to RPI
                    if appCloseEvent:
                        sys.exit()
