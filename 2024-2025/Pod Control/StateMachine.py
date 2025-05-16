import threading
import gpiozero
import RpiPinouts
import time


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

def StateMachine(State: int, sensorvals: list, commands) -> int:
    curState = State
    if curState == SAFE:
        # Safe to approach stuff
        # If commands are received from station and sensorvals are ok, run Safe -> Launch ready function
        # If anything goes wrong, transition to fault
        # Update curState

        # deploy brakes
        RpiPinouts.deploy_brakes()

        # Main circuit power off:
        RpiPinouts.main_power_off()

        if commands == "prep launch":
            # Set main power pins to high
            RpiPinouts.main_power_on()
            curState = LAUNCH_READY  
            
        print(stateToStr[curState])
                         

    if curState == LAUNCH_READY:


        # Ready to launch stuff

        #keep brakes applied during ready state:
        RpiPinouts.deploy_brakes()

        # If commands are received from station and sensorvals are ok, run launch function
        if commands == "Launch":
            # Release Brakes
            RpiPinouts.retract_brakes()
            #close main circuit switches
            RpiPinouts.main_power_on()

            RpiPinouts.LIM_run() # close switch that tells lim to actually start

            # update to running
            curState = RUNNING
        
        # if launch is canceld, go back to safe state
        if commands == "no launch":
            RpiPinouts.deploy_brakes()
            RpiPinouts.main_power_off()
            curState = SAFE 

        # If anything goes wrong, transition to fault

        print(stateToStr[curState])
                      

    if curState == RUNNING:
        # Running stuff
        # If commands are received from station and sensorvals are ok, or when sensorvals exceed any set limit, run brake function
        # If anything goes wrong, transition to fault               

        #keep main power on:
        RpiPinouts.main_power_on()
        #keep brakes released:
        RpiPinouts.retract_brakes()
        

        if commands == "brake":
            RpiPinouts.main_power_off()
            RpiPinouts.deploy_brakes()
            curState = BRAKING   # If command says brake, move to BRAKING
        
        print(stateToStr[curState])

    if curState == BRAKING:
        # Braking stuff
        # If once pod reaches a full stop, run safe functions
        # If anything goes wrong, transition to fault
        # Update curState

        # Turn off main power:
        RpiPinouts.main_power_off()
        # Apply brakes:
        RpiPinouts.deploy_brakes()

        if commands == "stop complete": 
            curState = SAFE         #once pod is fully stopped, go back to SAFE
        
        print(stateToStr[curState])

        
   
    if curState == FAULT:
        # Fault stuff
        # Safe state the pod and send info dump to control station
        # Transition to safe state only when command is given from the control station
        
        # Turn off main circuit power:
        RpiPinouts.main_power_off()
        # Apply brakes: 
        RpiPinouts.deploy_brakes()

        # Flash all LEDs to indicate fault:
        while commands != "reset fault":
            RpiPinouts.led_pins["LED 3"].blink()

        if commands == "reset fault":   
            curState = SAFE     #ending fault state, go back to SAFE
        
        print(stateToStr[curState])

    return curState

current_state = SAFE

def main(sensor_lock: threading.Lock, commands_lock: threading.Lock):
    commandsFile = open("2024-2025\Pod Control\commands.txt", "r")
    sensorvals = open("2024-2025\Pod Control\sensorvals.txt", "r")
    RpiPinouts.pin_init()
    while True:
        # access sensor data file
        # insert read function for data file
        sensor_lock.acquire()
        with sensor_lock:
            sensor_data = sensorvals.read()
        sensor_lock.release()

        # access Commands file
        # insert read function for commands file
        commands_lock.acquire()
        with commands_lock:
            commands = commandsFile.read()
        commands_lock.release()
        
        current_state = StateMachine(current_state, sensor_data, commands)