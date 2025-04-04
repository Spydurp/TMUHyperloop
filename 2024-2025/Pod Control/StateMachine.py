import threading
import RPi.GPIO as GPIO
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

def StateMachine(State: int, sensorvals: list, commands) -> int:
    curState = State
    if curState == SAFE:
        # Safe to approach stuff
        # If commands are received from station and sensorvals are ok, run Safe -> Launch ready function
        # If anything goes wrong, transition to fault
        # Update curState

        # Run Brake Check function
        # Set Brake Pins to Low
        for pin in RpiPinouts.brake_power_pins.values():
            GPIO.output(pin, GPIO.LOW)
        # ...

        if commands == "prep launch":
            # deploy brakes
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S1"], GPIO.HIGH)
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S2"], GPIO.HIGH)
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S3"], GPIO.HIGH)
            GPIO.output(RpiPinouts.brake_power_pins["Brake Control S4"], GPIO.HIGH)

            # Set main power pins to high
            for pin in RpiPinouts.main_circuit_pins.values():
                GPIO.output(pin, GPIO.HIGH)
            

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