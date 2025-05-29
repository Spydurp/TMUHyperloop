import time
import serial
import StateMachine

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

curState = 0

# Run startup tests here
# Brake test

# use a mutex object to ensure only 1 thread accesses a resource at a time
# pass mutex object into each thread

# initialize connection thread
# initialize state machine thread
StateMachine.main()
# initialize data input thread
