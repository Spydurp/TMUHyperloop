import time
import serial
import StateMachine
import threading
import RpiPinouts
import RPIServer

# Data Array Definitions
BATVOLT = 0
BATCUR = 1
BATTEMP = 2
LIMVOLT = 3
LIMCUR = 4
LIMTEMP = 5
VEL = 6
LBRAKEON = 7
LBRAKEOFF = 8
RBRAKEON = 9
RBRAKEOFF = 10

# State Definitions
SAFE = 0
LAUNCH_READY = 1
RUNNING = 2
BRAKING = 3
FAULT = -1

# Raspberry Pi IP Info
RPI_IP = "192.168.0.120" # On Hyperloop wifi
RPI_PORT = 15000

curState = SAFE

# create mutex lock
sensor_lock = threading.Lock()
commands_lock = threading.Lock()

# initialize connection thread
commsThread = threading.Thread(None, RPIServer.connection, "connectionThread",(commands_lock, sensor_lock, RPI_IP, RPI_PORT))
commsThread.start()

# Run startup tests here
# Brake test
#RpiPinouts.fans_on()
# initialize state machine thread
stateMachineThread = threading.Thread(None, StateMachine.main, "StateMachineThread",(sensor_lock, commands_lock))

# initialize data input thread (for later implementation)


stateMachineThread.start()

commsThread.join()
stateMachineThread.join()
RpiPinouts.fans_off()
print("POD CONTROL PROGRAM ENDED")