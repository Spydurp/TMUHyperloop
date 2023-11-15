import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSlider,QHBoxLayout,QStackedLayout,QStackedWidget,QSizeGrip
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class HyperloopControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Naqro Baby Moment")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout

        # Displays for voltage and current
        style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        self.battery_display = QLabel("Battery Display:")
        self.voltage_display = QLabel("Voltage: N/A V")
        self.voltage_display.setStyleSheet(style)
        self.current_display = QLabel("Current: N/A A")
        self.current_display.setStyleSheet(style)
        self.linear = QLabel("Linear Induction Motor:")
        self.voltage_display2 = QLabel("Voltage: N/A V")
        self.voltage_display2.setStyleSheet(style)
        self.current_display2 = QLabel("Current: N/A A")
        self.current_display2.setStyleSheet(style)
        self.pod = QLabel("Pod:")
        self.voltage_display3 = QLabel("Voltage: N/A V")
        self.voltage_display3.setStyleSheet(style)
        self.current_display3 = QLabel("Current: N/A A")
        self.current_display3.setStyleSheet(style)

        # Start and stop buttons
        style = "QPushButton { background-color: #007acc; color: white; }"
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(style)

        style = "QPushButton { background-color: #ff4b4b; color: white; }"
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        self.image_label = QLabel()
        image_path = "MikuHat.jpg"  
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


        # Connect buttons to their respective functions
        self.start_button.clicked.connect(self.start_train)
        self.stop_button.clicked.connect(self.stop_train)


        # Add widgets to the layout
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.stop_button)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.battery_display) 
        main_layout.addWidget(self.voltage_display)
        main_layout.addWidget(self.current_display)
        main_layout.addWidget(self.linear)
        main_layout.addWidget(self.voltage_display2)
        main_layout.addWidget(self.current_display2)
        main_layout.addWidget(self.pod)
        main_layout.addWidget(self.voltage_display3)
        main_layout.addWidget(self.current_display3)
        central_widget.setLayout(layout)

    def update_voltage_display(self):
        self.voltage_display.setText(f"Voltage: {voltage} V")

    def start_train(self):
        # Implement code to start the train or perform relevant actions
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: JOEVER A")

    def stop_train(self):
        # Implement code to stop the train or perform relevant actions
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: 0 A")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    window = HyperloopControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()