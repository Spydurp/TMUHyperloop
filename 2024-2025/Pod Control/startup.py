import time
import serial
import StateMachine
import threading
import RpiPinouts

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

curState = SAFE

# Run startup tests here
# Brake test
RpiPinouts.brake_check()

# create mutex lock
sensor_lock = threading.Lock()
commands_lock = threading.Lock()

# initialize connection thread
# initialize state machine thread
stateMachineThread = threading.Thread(StateMachine.main, sensor_lock, commands_lock)
StateMachine.main()
# initialize data input thread
