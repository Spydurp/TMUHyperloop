import threading
import gpiozero
import RpiPinouts
import time

COMMANDS_FILE = "/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/commands.txt"
SENSOR_FILE = "/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/sensorvals.txt"

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

stateToStr = {
    SAFE : "Safe to Approach",
    LAUNCH_READY: "Ready to Launch",
    RUNNING : "Running",
    BRAKING : "Braking",
    FAULT : "Fault"
}

current_state = SAFE

def update_state():
    with open(SENSOR_FILE, "r") as sensorvals:
        data = sensorvals.read().split(',')
        data[19] = stateToStr[current_state]
    with open(SENSOR_FILE, "w") as sensorvals:
        s = ""
        i = 0
        while i < len(data)-1:
            s = s + data[i] + ","
            i += 1
        s = s + data[i]
        sensorvals.write(s)

def StateMachine(State: int, sensorvals: list, commands) -> int:
    curState = State
    if curState == SAFE:
        # Safe to approach stuff
        # If commands are received from station and sensorvals are ok, run Safe -> Launch ready function
        # If anything goes wrong, transition to fault
        # Update curState
        
        # Main circuit power off:
        RpiPinouts.main_power_off()
        
        # deploy brakes
        RpiPinouts.deploy_brakes()

        if commands == "READY":
            # Set main power pins to high
            RpiPinouts.main_power_on()
            curState = LAUNCH_READY  
        if commands == "STOP_NOW":
            curState = FAULT        

    if curState == LAUNCH_READY:
        # Ready to launch stuff

        #keep brakes applied during ready state:
        RpiPinouts.deploy_brakes()

        # If commands are received from station and sensorvals are ok, run launch function
        if commands == "GO":
            # Release Brakes
            RpiPinouts.retract_brakes()
            #close main circuit switches
            RpiPinouts.main_power_on()

            RpiPinouts.LIM_run() # close switch that tells lim to actually start

            # update to running
            curState = RUNNING
        
        # if launch is canceld, go back to safe state
        if commands == "ABORT":
            RpiPinouts.deploy_brakes()
            RpiPinouts.main_power_off()
            curState = SAFE
        if commands == "STOP_NOW":
            curState = FAULT
                      
    if curState == RUNNING:
        # Running stuff
        # If commands are received from station and sensorvals are ok, or when sensorvals exceed any set limit, run brake function
        # If anything goes wrong, transition to fault               

        #keep main power on:
        RpiPinouts.main_power_on()
        #keep brakes released:
        RpiPinouts.retract_brakes()
        

        if commands == "STOP":
            RpiPinouts.LIM_off()
            RpiPinouts.main_power_off()
            RpiPinouts.deploy_brakes()
            curState = BRAKING   # If command says brake, move to BRAKING
        if commands == "STOP_NOW":
            curState = FAULT

    if curState == BRAKING:
        # Braking stuff
        # If once pod reaches a full stop, run safe functions
        # If anything goes wrong, transition to fault
        # Update curState
        RpiPinouts.LIM_off()
        # Turn off main power:
        RpiPinouts.main_power_off()
        # Apply brakes:
        RpiPinouts.deploy_brakes()
        
        #once pod is fully stopped, go back to SAFE
        timer = threading.Timer(10, make_safe) # Might not work
        timer.start()
        def make_safe():
            global current_state
            if current_state == BRAKING:
                current_state = SAFE
            timer.cancel()

        if commands == "STOP_NOW":
            curState = FAULT

    if curState == FAULT:
        # Fault stuff
        # Safe state the pod and send info dump to control station
        # Transition to safe state only when command is given from the control station
        RpiPinouts.LIM_off()
        # Turn off main circuit power:
        RpiPinouts.main_power_off()
        # Apply brakes: 
        RpiPinouts.deploy_brakes()

        while commands != "RESET_FAULT":
            RpiPinouts.led_pins["LED 3"].blink()

        if commands == "RESET_FAULT":   
            curState = SAFE     #ending fault state, go back to SAFE
        
    #print(stateToStr[curState])

    return curState

def main(sensor_lock: threading.Lock, commands_lock: threading.Lock):
    global current_state
    while True:
        # access sensor data file
        # insert read function for data file
        
        if sensor_lock.acquire():
            update_state()
            with open("/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/sensorvals.txt", "r") as sensorvals:
                sensor_data = sensorvals.read()
        sensor_lock.release()
        # put sensor data in an array before using when we finally implement this part

        # access Commands file
        # insert read function for commands file
        if commands_lock.acquire():
            with open("/home/hyperlooop/Desktop/Hyperloop/TMUHyperloop/2024-2025/Pod Control/commands.txt", "r") as commandsFile:
                commands = commandsFile.read()
        commands_lock.release()
    
        current_state = StateMachine(current_state, sensor_data, commands)
        time.sleep(0.1)
    