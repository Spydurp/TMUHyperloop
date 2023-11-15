import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

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
        voltage_layout = QHBoxLayout()
        current_layout = QHBoxLayout()
        commandwindow_layout = QVBoxLayout()

        style = "QPushButton { background-color: #ffdc00; color: blue; }"
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(style)
        style = "QPushButton { background-color: #004c9b; color: yellow; }"
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style)

        self.image_label = QLabel()
        image_path = "Hyperloop_logo_W.png"
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.image_label)
        button_layout.addWidget(self.stop_button)

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

        title_layout.addWidget(self.battery_display)
        title_layout.addWidget(self.linear)
        voltage_layout.addWidget(self.voltage_display)
        voltage_layout.addWidget(self.voltage_display2)
        current_layout.addWidget(self.current_display)
        current_layout.addWidget(self.current_display2)

        # Slider for voltage control
        self.voltage_slider = QSlider(Qt.Horizontal)
        self.voltage_slider.setRange(0, 5000)
        self.voltage_slider.setValue(0)
        self.voltage_slider.setTickPosition(QSlider.TicksBelow)
        self.voltage_slider.setTickInterval(10)
        self.voltage_slider.valueChanged.connect(self.update_voltage_display)

        self.image_label = QLabel()
        image_path = "MikuHat.jpg"
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

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

        # Create a dictionary to use as a local scope for code execution
        self.console_locals = {}

        # Add widgets to the layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(title_layout) 
        main_layout.addLayout(voltage_layout)
        main_layout.addLayout(current_layout)
        main_layout.addWidget(self.pod)
        main_layout.addWidget(self.voltage_display3)
        main_layout.addWidget(self.current_display3)
        main_layout.addLayout(commandwindow_layout)
        central_widget.setLayout(main_layout)

    def update_voltage_display(self):
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")

    def start_train(self):
        # Implement code to start the train or perform relevant actions
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: JOEVER A")
        self.voltage_display2.setText(f"Voltage: {voltage} V")
        self.current_display2.setText("Current: JOEVER A")
        self.voltage_display3.setText(f"Voltage: {voltage} V")
        self.current_display3.setText("Current: JOEVER A")


    def stop_train(self):
        # Implement code to stop the train or perform relevant actions
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: 0 A")
        self.voltage_display2.setText(f"Voltage: {voltage} V")
        self.current_display2.setText("Current: 0 A")
        self.voltage_display3.setText(f"Voltage: {voltage} V")
        self.current_display3.setText("Current: 0 A")

    def user_input(self):
        # Implement code to print user input in command block
        print(self.command_window.toPlainText())

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HyperloopControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()