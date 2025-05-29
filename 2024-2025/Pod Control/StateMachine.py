
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

current_state = 0

def StateMachine(State: int, sensorvals: list, commands) -> int:
    curState = State
    if curState == SAFE:
        # Safe to approach stuff
        # If commands are received from station and sensorvals are ok, run Safe -> Launch ready function
        # If anything goes wrong, transition to fault
        # Update curState
        print("Safe to approach")
    if curState == LAUNCH_READY:
        # Ready to launch stuff
        # If commands are received from station and sensorvals are ok, run launch function
        # If anything goes wrong, transition to fault
        # Update curState
        print("Ready to Launch")
    if curState == RUNNING:
        # Running stuff
        # If commands are received from station and sensorvals are ok, or when sensorvals exceed any set limit, run brake function
        # If anything goes wrong, transition to fault
        # Update curState
        print("Running")
    if curState == BRAKING:
        # Braking stuff
        # If once pod reaches a full stop, run safe functions
        # If anything goes wrong, transition to fault
        # Update curState
        print("Braking")
    if curState == FAULT:
        # Fault stuff
        # Safe state the pod and send info dump to control station
        # Transition to safe state only when command is given from the control station
        print("Fault")

    
    return curState

def main():
    while True:
        # Get commands and sensor data from shared file with comms thread and sensor data thread
        sensorvals = {} # insert read function here
        commands = {} # insert command read function here
        # set the current state
        current_state = StateMachine(current_state, sensorvals, commands)