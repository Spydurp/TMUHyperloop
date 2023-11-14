import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class HyperloopControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Naqro Baby Moment")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Displays for voltage and current
        style = "QLabel { border: 1px solid gray; background-color: #1E1E1E; color: white; padding: 5px; }"
        self.voltage_display = QLabel("Voltage: N/A V")
        self.voltage_display.setStyleSheet(style)
        self.current_display = QLabel("Current: N/A A")
        self.current_display.setStyleSheet(style)

        # Slider for voltage control
        self.voltage_slider = QSlider(Qt.Horizontal)
        self.voltage_slider.setRange(0, 5000)  
        self.voltage_slider.setValue(0)
        self.voltage_slider.setTickPosition(QSlider.TicksBelow)
        self.voltage_slider.setTickInterval(10)
        self.voltage_slider.valueChanged.connect(self.update_voltage_display)

        # Start and stop buttons
        style = "QPushButton { background-color: #007acc; color: white; }"
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(style)
        style = "QPushButton { background-color: #ff4b4b; color: white; }"
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style)

        self.image_label = QLabel()
        image_path = "MikuHat.jpg"  
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)


        # Connect buttons to their respective functions
        self.start_button.clicked.connect(self.start_train)
        self.stop_button.clicked.connect(self.stop_train)

        # Add widgets to the layout
        layout.addWidget(self.image_label)  
        layout.addWidget(self.voltage_display)
        layout.addWidget(self.voltage_slider)
        layout.addWidget(self.current_display)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        central_widget.setLayout(layout)

    def update_voltage_display(self):
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")

    def start_train(self):
        # Implement code to start the train or perform relevant actions
        voltage = self.voltage_slider.value()
        self.voltage_display.setText(f"Voltage: {voltage} V")
        self.current_display.setText("Current: JOEVER A")

    def stop_train(self):
        # Implement code to stop the train or perform relevant actions
        voltage = self.voltage_slider.value()
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
