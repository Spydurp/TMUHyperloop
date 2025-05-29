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

        self.limDisplay = QLabel("LIM:")
        self.limVolt = QLabel("Voltage: N/A V")
        self.limVolt.setStyleSheet(style)
        self.limCur = QLabel("Current: N/A A")
        self.limCur.setStyleSheet(style)
        self.limTemp = QLabel("Temperature: N/A °C")
        self.limTemp.setStyleSheet(style)

        LIM_title_layout.addWidget(self.limDisplay)
        LIM_Layout.addWidget(self.limVolt)
        LIM_Layout.addWidget(self.limCur)
        LIM_Layout.addWidget(self.limTemp)

        self.brakeDisplay = QLabel("Brake Position:")
        self.brake_1_pos = QLabel("Deployed")
        self.brake_1_pos.setStyleSheet(style)
        self.brake_2_pos = QLabel("Deployed")
        self.brake_2_pos.setStyleSheet(style)

        brake_title_layout.addWidget(self.brakeDisplay)
        brake_layout.addWidget(self.brake_1_pos)
        brake_layout.addWidget(self.brake_2_pos)

        self.stateDisplay = QLabel("Current State:")
        self.state = QLabel("Safe to Approach")
        self.state.setStyleSheet(style)

        state_title_layout.addWidget(self.stateDisplay)
        state_layout.addWidget(self.state)

        #Other Stuff
        self.current_speed = QLabel("Current Speed")
        self.CS_display = QLabel("N/A m/s")
        self.CS_display.setStyleSheet(style)
        self.position = QLabel("Position")
        self.Pos_display = QLabel ("0 m")
        self.Pos_display.setStyleSheet(style)

        speed_layout.addWidget(self.current_speed)
        speedDisplay_layout.addWidget(self.CS_display)
        pos_pressure_layout.addWidget(self.position)
        posPressureDisplay_layout.addWidget(self.Pos_display)
        

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
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()