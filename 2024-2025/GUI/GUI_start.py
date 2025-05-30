import WorkingGUI
import threading
import GUI_Connection

RPI_IP = "192.168.0.120"
RPI_PORT = 15000
C_LOCK = threading.Lock()
D_LOCK = threading.Lock()

gui_connection = threading.Thread(None, GUI_Connection.connect, "connection",(RPI_IP, RPI_PORT, C_LOCK, D_LOCK))
gui = threading.Thread(None, WorkingGUI.main, "frontend",(D_LOCK, C_LOCK))

gui_connection.start()
gui.start()

gui_connection.join()
gui.join()

print("GUI TERMINATED")