from PySide6 import uic
from PySide6.QtWidgets import QApplication

Form, Window = uic.loadUiType("2023-2024/GUI/GUI.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()
