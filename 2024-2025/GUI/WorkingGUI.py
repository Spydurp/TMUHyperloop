import sys
import os
import socket
import threading
import json
import time
from PySide6.QtWidgets import QApplication, QGroupBox, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit, QMessageBox, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtGui import QPixmap, QImage, QFont, QFontDatabase, QColor, QTextCursor






HOST_IP = "192.168.x.x"
TCP_PORT = 5000
CMD_FILE = "2024-2025\GUI\commands.txt"
DATA_FILE = "2024-2025\GUI\data.txt"
LOGO_PATH = "2024-2025\GUI\Hyperloop_full_logo_B.png"
#d_LOCK = threading.Lock()
#c_LOCK = threading.Lock()


class HyperloopControlGUI(QMainWindow):
    def __init__(self, d_lock: threading.Lock, c_lock: threading.Lock):
        super().__init__()
        self.D_LOCK = d_lock
        self.C_LOCK = c_lock


        self.setWindowTitle("Pod Control GUI")
        self.setGeometry(100, 100, 900, 600)    #size of display


        central_widget = QWidget()              #display screen
        self.setCentralWidget(central_widget)   #display widgets


        # Window Style:
        self.setStyleSheet("""
            QMainWindow { background-color: #474649; }
            QWidget { background-color: #242533; color: white; }
            QLabel { color: white; }
        """)


       #---------------------------- Creating widgets/layouts --------------------------------
       
       #Button_style:
        button_style = """
            QPushButton {
                padding: 8px;
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 12pt;
                background-color: #2E2E2E;   /* color of button */
                color: white;                /* color of writing */
                border: 1px solid gray;      /* border */
                border-radius: 10px;         /* rounder edges */
            }
            QPushButton:hover {
                background-color: #3A3A3A;  
            }
            QPushButton:pressed {
                background-color: #1E1E1E;  
            }
        """
        green_button_style = button_style + " QPushButton {background-color: #206a2a; color: white;}"
        red_button_style = button_style + " QPushButton { background-color: #d80505; color: white; }"
        blue_button_style = button_style + " QPushButton { background-color: #090daa; color: white; }"
        orange_button_style = button_style + " QPushButton { background-color: #f56612; color: white; }"
        purple_button_style = button_style + " QPushButton { background-color: #7702cf; color: white; }"
        yellow_button_style = button_style + " QPushButton { background-color: #f9ba1d; color: white; }"
       


        #display_style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        #state_style = "QLabel { border: 1px solit gray; background-color: #1E1E1E; color: white: padding: 5px; font: 18pt; }"


        #Right-side vertical buttons:
        # Control buttons:
        self.launch_button = QPushButton("LAUNCH")
        self.launch_button.setStyleSheet(green_button_style)
        self.launch_button.clicked.connect(self.on_launch)
       
        self.stop_button = QPushButton("STOP")
        self.stop_button.setStyleSheet(red_button_style)
        self.stop_button.clicked.connect(self.on_stop)


        self.e_stop_button = QPushButton("STOP NOW")
        self.e_stop_button.setStyleSheet(orange_button_style)
        self.e_stop_button.clicked.connect(self.on_e_stop)


        self.ready_button = QPushButton("PREP FOR LAUNCH")
        self.ready_button.setStyleSheet(yellow_button_style)
        self.ready_button.clicked.connect(self.on_ready)


        self.cancel_button = QPushButton("ABORT LAUNCH")
        self.cancel_button.setStyleSheet(purple_button_style)
        self.cancel_button.clicked.connect(self.on_Cancel)


        self.reset_fault_button = QPushButton("RESET FAULT")
        self.reset_fault_button.setStyleSheet(blue_button_style)
        self.reset_fault_button.clicked.connect(self.on_fault_reset)




        # # Image label:
        # self.image_label = QLabel()
        # image_path = os.path.join("2024-2025", "GUI", "miku.jpg")
        # if os.path.exists(image_path):
        #     pixmap = QPixmap(image_path)
        #     self.image_label.setPixmap(pixmap)
        # else:
        #     self.image_label.setText("(image not found)")
        # self.image_label.setAlignment(Qt.AlignCenter)


        # Telemetry labels:
        display_style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
       
        self.bat1_volt = QLabel("Voltage: N/A V")
        self.bat1_volt.setStyleSheet(display_style)
        self.bat1_cur = QLabel("Current: N/A A")
        self.bat1_cur.setStyleSheet(display_style)
        self.bat1_temp = QLabel("Temperature: N/A °C")
        self.bat1_temp.setStyleSheet(display_style)


        self.limVolt = QLabel("Voltage: N/A V")
        self.limVolt.setStyleSheet(display_style)
        self.inverter_voltage = QLabel("Voltage: N/A V")
        self.inverter_voltage.setStyleSheet(display_style)


        self.state = QLabel("Safe to Approach")
        self.state.setStyleSheet(display_style)
        self.state.setFont(QFont("Arial", 18))


        # # Command log:
        # self.command_window = QTextEdit()
        # self.command_window.setReadOnly(True)


        #----------------------------------------------------------------------------------------------
        # ---------- Title Frame @ Top ----------
        title_frame = QGroupBox("Metropolitan Hyperloop")
        title_frame.setObjectName("titleframe")
        title_frame.setFixedHeight(150)


        title_frame.setStyleSheet("""
            QGroupBox#stateframe {
                background: rgba(255,255,255,0.04);
                border-radius: 14px;
                border: 2px solid rgba(96,165,250,0.22);  
                padding: 10 px;
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 15pt;
                color: white;
                left: 375px;      /* title how much to the right */
                top: 30px;        /* title how much to the bottom */
                margin-top: 10px;
            }
            QGroupBox::title {
                left: 375px;      /* title how much to the right */
                top: 30px;        /* title how much to the bottom */
                padding: 0 4px;   /* top/bottom, left/right */
                color: rgb(180,200,255);    
                font-size: 15pt;
            }
        """)


        # Add glow effect:
        glow_top = QGraphicsDropShadowEffect()
        glow_top.setBlurRadius(40)
        glow_top.setColor(QColor(96,165,250))
        glow_top.setOffset(0, 0)
        title_frame.setGraphicsEffect(glow_top)


        # inner layout for content
        title_layout = QHBoxLayout(title_frame)

        # Logo Display:
        self.logo_display = QLabel(self)
        self.logo_display.setAlignment(Qt.AlignCenter)
        logo = QPixmap(LOGO_PATH).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_display.setPixmap(logo)
        self.logo_display.setScaledContents(True)
        title_layout.addWidget(self.logo_display)
       
        # ------------ left and right layout arrangement -------------
        main_layout = QHBoxLayout()   # split screen: left = telemetry, right = controls
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()


        # ---------- Left  ----------
        #left_layout.addWidget(self.image_label)
        left_layout.addWidget(QLabel("Battery 1"))
        left_layout.addWidget(self.bat1_volt)
        left_layout.addWidget(self.bat1_cur)
        left_layout.addWidget(self.bat1_temp)
       
        left_layout.addSpacing(10)


        left_layout.addWidget(QLabel("LIM"))
        left_layout.addWidget(self.limVolt)
        left_layout.addWidget(QLabel("Inverter"))
        left_layout.addWidget(self.inverter_voltage)


        left_layout.addSpacing(10)


        left_layout.addWidget(QLabel("State"))
        left_layout.addWidget(self.state)


        left_layout.addStretch(2)


        # left_layout.addWidget(QLabel("Command Log:"))
        # left_layout.addWidget(self.command_window, stretch=2)
        #---------------------------------------------------------------------------------


        # ---------- Right  ----------
        control_frame = QGroupBox("MISSION CONTROL")     # frame
        control_frame.setObjectName("glowframe")
        control_frame.setFixedWidth(280)


        # Frame Style:
        control_frame.setStyleSheet("""
            QGroupBox#glowframe {
                background: rgba(255,255,255,0.03);
                border-radius: 14px;
                border: 2px solid rgba(96,165,250,0.22);
                padding: 12px;
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 13pt;
                color: white;
                margin-top: 24px;          /* adds space above for title */
            }
            QGroupBox::title {
                subcontrol-origin: margin;  /* adds title above the frame */
                left: 12px;
                top: 4px;
                padding: 0 4px;
                color: rgb(180,200,255);
                font-size: 14pt;
            }
        """)


        # Glow effect:
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(40)
        glow.setColor(QColor(96,165,250))  #color of glow
        glow.setOffset(0, 0)
        control_frame.setGraphicsEffect(glow)


        # Layout inside the glowing group box:
        control_layout = QVBoxLayout(control_frame)
        control_layout.setSpacing(10)


        # Adding buttons
        for button in (
            self.ready_button, self.cancel_button, self.launch_button,
            self.stop_button, self.e_stop_button, self.reset_fault_button
        ):
            button.setParent(control_frame)
            button.setFixedHeight(42)
            # button.setStyleSheet(button.styleSheet() + """
            #     QPushButton {
            #         border-radius: 10px;
            #         border: 1px solid rgba(0, 0, 0, 0.15);
            #     }
            #     QPushButton:pressed { padding-left: 2px; }
            # """)
            control_layout.addWidget(button)


        control_layout.addStretch(1)


        # adding frame as a widget the right layout
        right_layout.addWidget(control_frame)
        right_layout.addStretch(1)




        # # Put left and right into main ------------------------------------------
        # main_layout.addLayout(main_layout, stretch=3)
        # main_layout.addLayout(left_layout, stretch=3)
        # main_layout.addLayout(right_layout, stretch=3)
        # central_widget.setLayout(main_layout)     #displaying everthing


        # ---------- Combine everything ----------
        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, stretch=3)
        content_layout.addLayout(right_layout, stretch=3)


        # State frame layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_frame)
        main_layout.addLayout(content_layout)
        central_widget.setLayout(main_layout)
        
        #------------------------------------------------------------------------------------------
        
        # small debug print to confirm constructor completed:
        print("GUI constructed")

        # ------------------- Add terminal-style logs -------------------
        # Group boxes + terminal text areas placed at bottom of the window
        system_group = QGroupBox("SYSTEM LOGS")
        system_group.setStyleSheet("QGroupBox { color: #65ff9c; font-weight: bold; }")
        self.system_logs = QPlainTextEdit()
        self.system_logs.setReadOnly(True)
        self.system_logs.setPlainText("")  # start empty
        self.system_logs.setStyleSheet("""
            QPlainTextEdit {
                background: #0f1216;
                color: #9ef08a;
                border: 1px solid #224;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """)
        sg_layout = QVBoxLayout(system_group)
        sg_layout.addWidget(self.system_logs)

        pod_group = QGroupBox("POD LOGS")
        pod_group.setStyleSheet("QGroupBox { color: #ffb86b; font-weight: bold; }")
        self.pod_logs = QPlainTextEdit()
        self.pod_logs.setReadOnly(True)
        self.pod_logs.setStyleSheet("""
            QPlainTextEdit {
                background: #0f1216;
                color: #ffb86b;
                border: 1px solid #224;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """)
        rg_layout = QVBoxLayout(pod_group)
        rg_layout.addWidget(self.pod_logs)

        # place side-by-side under the main content
        logs_layout = QHBoxLayout()
        logs_layout.addWidget(system_group, stretch=3)
        logs_layout.addWidget(pod_group, stretch=3)
        main_layout.addLayout(logs_layout)
        # ------------------- end logs -------------------
        
        # small debug print to confirm constructor completed:
        print("GUI constructed")


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
            velocity, distance_traveled, state) = data  # New inverter voltage added


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


            # updated brake positions
            self.brake_1_pos.setText("Deployed" if brake1_deployed else "Retracted")
            self.brake_2_pos.setText("Deployed" if brake2_deployed else "Retracted")


            # updated velocity/position
            self.CS_display.setText(f"{velocity} m/s")
            self.Pos_display.setText(f"{distance_traveled} m")


            # updated pod state
            self.state.setText(state)
        except Exception as e:
            self.log_command(f"Error updating GUI with received data: {str(e)}")


#------------------------------------------------------------------------------------------------------
    def log_command(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        line = f"[{timestamp}] {message}"
        # default to system logs; use append helpers so it autoscrolls
        try:
            self.append_system_log(line)
        except Exception:
            # fallback print if GUI not ready
            print(line)

    def append_system_log(self, message: str):
        # Append and autoscroll to end
        self.system_logs.appendPlainText(message)
        cursor = self.system_logs.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.system_logs.setTextCursor(cursor)

    def append_pod_log(self, message: str):
        self.pod_logs.appendPlainText(message)
        cursor = self.pod_logs.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.pod_logs.setTextCursor(cursor)

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











