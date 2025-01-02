import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

class HyperloopControlGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pod Control")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.command_window = QTextEdit()

        main_layout = QVBoxLayout()

        # Start and stop buttons side by side
        button_layout = QHBoxLayout()
        title_layout = QHBoxLayout()
        title_layout2 = QHBoxLayout()
        bat1_2_vLayout = QHBoxLayout()
        bat1_2_cLayout = QHBoxLayout()
        bat1_2_tLayout = QHBoxLayout()
        bat3_4_vLayout = QHBoxLayout()
        bat3_4_cLayout = QHBoxLayout()
        bat3_4_tLayout = QHBoxLayout()
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
        
        self.bat1_display = QLabel("Battery 1:")
        self.bat1_volt = QLabel("Voltage: N/A V")
        self.bat1_volt.setStyleSheet(style)
        self.bat1_cur = QLabel("Current: N/A A")
        self.bat1_cur.setStyleSheet(style)
        self.bat1_temp = QLabel("Temperature: N/A °C")
        self.bat1_temp.setStyleSheet(style)

        self.bat2_display = QLabel("Battery 2:")
        self.bat2_volt = QLabel("Voltage: N/A V")
        self.bat2_volt.setStyleSheet(style)
        self.bat2_cur = QLabel("Current: N/A A")
        self.bat2_cur.setStyleSheet(style)
        self.bat2_temp = QLabel("Temperature: N/A °C")
        self.bat2_temp.setStyleSheet(style)

        self.bat3_display = QLabel("Battery 3:")
        self.bat3_volt = QLabel("Voltage: N/A V")
        self.bat3_volt.setStyleSheet(style)
        self.bat3_cur = QLabel("Current: N/A A")
        self.bat3_cur.setStyleSheet(style)
        self.bat3_temp = QLabel("Temperature: N/A °C")
        self.bat3_temp.setStyleSheet(style)

        self.bat4_display = QLabel("Battery 4:")
        self.bat4_volt = QLabel("Voltage: N/A V")
        self.bat4_volt.setStyleSheet(style)
        self.bat4_cur = QLabel("Current: N/A A")
        self.bat4_cur.setStyleSheet(style)
        self.bat4_temp = QLabel("Temperature: N/A °C")
        self.bat4_temp.setStyleSheet(style)

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
        

        # Connect buttons to their respective functions

        # Create a dictionary to use as a local scope for code execution
        self.console_locals = {}

        # Add widgets to the layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(title_layout) 
        main_layout.addLayout(bat1_2_vLayout)
        main_layout.addLayout(bat1_2_cLayout)
        main_layout.addLayout(bat1_2_tLayout)

        main_layout.addLayout(title_layout2)
        main_layout.addLayout(bat3_4_vLayout)
        main_layout.addLayout(bat3_4_cLayout)
        main_layout.addLayout(bat3_4_tLayout)

        main_layout.addLayout(TempDisplay_layout2)
        main_layout.addLayout(speed_layout)
        main_layout.addLayout(speedDisplay_layout)
        main_layout.addLayout(pos_pressure_layout)
        main_layout.addLayout(posPressureDisplay_layout)
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()