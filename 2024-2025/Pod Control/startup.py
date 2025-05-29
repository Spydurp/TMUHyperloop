import time
import serial
import StateMachine
<<<<<<< HEAD
=======
import threading
import RpiPinouts
import GUI.RPIServer
>>>>>>> parent of 7662bdb (Added test files, tweaked behaviour to match hardware)

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

<<<<<<< HEAD
curState = 0
=======
# Raspberry Pi IP Info
RPI_IP = ""
RPI_PORT = 15000

curState = SAFE

# create mutex lock
sensor_lock = threading.Lock()
commands_lock = threading.Lock()

# initialize connection thread
commsThread = threading.Thread(GUI.RPIServer.connection, commands_lock, sensor_lock, RPI_IP, RPI_PORT)
commsThread.start()
>>>>>>> parent of 7662bdb (Added test files, tweaked behaviour to match hardware)

# Run startup tests here
# Brake test

<<<<<<< HEAD
# initialize connection thread
# initialize state machine thread
StateMachine.StateMachine()
# initialize data input thread
=======
if RpiPinouts.brake_check():
    # initialize state machine thread
    stateMachineThread = threading.Thread(StateMachine.main, sensor_lock, commands_lock)

    # initialize data input thread

    
    stateMachineThread.start()

    commsThread.join()
    stateMachineThread.join()

    print("POD CONTROL PROGRAM ENDED")
else:
    print("BRAKE CHECK FAILED")
>>>>>>> parent of 7662bdb (Added test files, tweaked behaviour to match hardware)
