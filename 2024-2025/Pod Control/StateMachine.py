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

def StateMachine(State: int, sensorvals: list, commands) -> int:
    curState = State
    if curState == SAFE:
        # Safe to approach stuff
        # If commands are received from station and sensorvals are ok, run Safe -> Launch ready function
        # If anything goes wrong, transition to fault
        # Update curState

        # deploy brakes
        RpiPinouts.deploy_brakes()

        if commands == "prep launch":
            # Set main power pins to high
            RpiPinouts.main_power_on()
            

        print("Safe to approach")

        # Run Brake Check function

        #Main circuit power off:
        for pin in RpiPinouts.main_circuit_pins.values():
            GPIO.output(pin, GPIO.LOW)
        #No brakes:
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.LOW)
        print("Safe to approach")

        if commands == "prep launch":
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S1"], GPIO.HIGH) # applying the brakes so pod is safe to approach
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S2"], GPIO.HIGH)
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S3"], GPIO.HIGH)
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S4"], GPIO.HIGH)    
            print("Brakes applied - Launch ready")
            curState = LAUNCH_READY               

    if curState == LAUNCH_READY:


        # Ready to launch stuff
        # If commands are received from station and sensorvals are ok, run launch function
        if commands == "Launch":
            # Release Brakes
            for pin in RpiPinouts.brake_power_pins.values():
                GPIO.output(pin, GPIO.LOW)
            #close main circuit switches
            GPIO.output(RpiPinouts.main_circuit_pins["Main Switch"], GPIO.HIGH)
            GPIO.output(RpiPinouts.main_circuit_pins["VFD Switch 1"], GPIO.HIGH)
            GPIO.output(RpiPinouts.main_circuit_pins["VFD Switch 2"], GPIO.HIGH)

            GPIO.output(RpiPinouts.vfd_pin, GPIO.HIGH) # close switch that tells lim to actually start

            # update to running


        # If anything goes wrong, transition to fault

        # Update curState

        
        #keep brakes applied during ready state:
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.HIGH) 
        #keep main circuit power off:
        for pin in RpiPinouts.main_circuit_pins.values():
            GPIO.output(pin, GPIO.LOW)
        print("Ready to Launch")

        if commands == "launch":
            # Turn on main power:
            for pin in RpiPinouts.main_circuit_pins.values():
                GPIO.output(pin, GPIO.HIGH)
            # Release brakes:
            for pin in RpiPinouts.brake_power_pins.values():
                GPIO.output(pin, GPIO.LOW)
            print("Launching")
            curState = RUNNING    # Question 1: can we remove the code above and replace with curState = RUNNING?
        
        # if launch is canceld, go back to safe state
        if commands == "no launch":
            curState = SAFE               

    if curState == RUNNING:
        # Running stuff
        # If commands are received from station and sensorvals are ok, or when sensorvals exceed any set limit, run brake function
        # If anything goes wrong, transition to fault               

        #keep main power on:
        for pin in RpiPinouts.main_circuit_pins.values():
            GPIO.output(pin, GPIO.HIGH)
        #keep brakes released:
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.LOW)
        print("Running")

        if commands == "brake":
            print("Braking initiated")
            curState = BRAKING   # If command says brake, move to BRAKING

    if curState == BRAKING:
        # Braking stuff
        # If once pod reaches a full stop, run safe functions
        # If anything goes wrong, transition to fault
        # Update curState

        # Apply brakes:
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.HIGH) 
        # Turn off main power:
        for pin in RpiPinouts.main_circuit_pins.values():
            GPIO.output(pin, GPIO.LOW)
        print("Braking")

        if commands == "stop complete": 
            curState = SAFE         #once pod is fully stopped, go back to SAFE
   
    if curState == FAULT:
        # Fault stuff
        # Safe state the pod and send info dump to control station
        # Transition to safe state only when command is given from the control station
        
        # Apply brakes: 
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.HIGH)
        # Turn off main circuit power:
        for pin in RpiPinouts.main_circuit_pins.values():
            GPIO.output(pin, GPIO.LOW)

            # Question 2 - replace above code with curstate = braking?

        # Flash all LEDs to indicate fault:
        while commands != "reset fault":
            for pin in RpiPinouts.led_pins.values():
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.4)
            for pin in RpiPinouts.led_pins.values():
                GPIO.output(pin, GPIO.LOW)
            time.sleep(0.4)
        
        print("Fault")

        if commands == "reset fault":   
            curState = SAFE     #ending fault state, go back to SAFE

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