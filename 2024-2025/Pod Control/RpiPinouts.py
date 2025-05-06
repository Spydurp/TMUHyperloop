import RPi.GPIO as GPIO
import time

TIMEOUT = 5 # Seconds before timeout for brake check

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Brake Sensor Input Pins
brake_sensors = {
    "Brake 1 (D)": 17,
    "Brake 1 (R)": 27,
    "Brake 2 (D)": 22,
    "Brake 2 (R)": 23,
    "Brake 3 (D)": 24,
    "Brake 3 (R)": 25,
    "Brake 4 (D)": 5,
    "Brake 4 (R)": 6
}

# Output Pins
led_pins = {
    "LED 1": 12,
    "LED 2": 13,
    "LED 3": 19
}

brake_power_pins = {
    "Brake Control S1": 16,
    "Brake Control S2": 20,
    "Brake Control S3": 21,
    "Brake Control S4": 18 
}

vfd_pin = 26

main_circuit_pins = {
    "Main Switch" : 14,
    "VFD Switch 1" : 15,
    "VFD Switch 2" : 2
}


def pin_init():
    # Set up all output pins
    for pin in led_pins.values():
        GPIO.setup(pin, GPIO.OUT)

    for pin in brake_power_pins.values():
        GPIO.setup(pin, GPIO.OUT)
    
    for pin in main_circuit_pins.values():
        GPIO.setup(pin, GPIO.OUT)

    # Set up input pins with pull-down resistors
    for pin in brake_sensors.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #Default to Low (0v)

    GPIO.setup(vfd_pin, GPIO.OUT)

def brake_check() -> bool:
    # Deploy brakes
    GPIO.output(brake_power_pins["Brake Control S1"], GPIO.HIGH)
    GPIO.output(brake_power_pins["Brake Control S2"], GPIO.HIGH)
    GPIO.output(brake_power_pins["Brake Control S3"], GPIO.HIGH)
    GPIO.output(brake_power_pins["Brake Control S4"], GPIO.HIGH)
    # wait until brakes are fully deployed
    t = time.perf_counter()
    while GPIO.input(brake_sensors["Brake 1 (D)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 1 (R)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 2 (D)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 2 (R)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 3 (D)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 3 (R)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 4 (D)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 4 (R)"]) != GPIO.LOW:
        # Timout after some time, means brakes aren't working properly
        if time.perf_counter() - t > TIMEOUT:
            return False
        time.sleep(0.5)
    # retract brakes
    GPIO.output(brake_power_pins["Brake Control S1"], GPIO.LOW)
    GPIO.output(brake_power_pins["Brake Control S2"], GPIO.LOW)
    GPIO.output(brake_power_pins["Brake Control S3"], GPIO.LOW)
    GPIO.output(brake_power_pins["Brake Control S4"], GPIO.LOW)
    #Wait until brakes are fully retracted
    t = time.perf_counter()
    while GPIO.input(brake_sensors["Brake 1 (D)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 1 (R)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 2 (D)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 2 (R)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 3 (D)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 3 (R)"]) != GPIO.HIGH and GPIO.input(brake_sensors["Brake 4 (D)"]) != GPIO.LOW and GPIO.input(brake_sensors["Brake 4 (R)"]) != GPIO.HIGH:
        # Timeout after some time, means brakes aren't working properly
        if time.perf_counter() - t > TIMEOUT:
            return False
        time.sleep(0.5)
    
    return True