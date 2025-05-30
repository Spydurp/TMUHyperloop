import time
import gpiozero

TIMEOUT = 5 # Seconds before timeout for brake check

# Brake Sensor Input Pins

brake_sensors = {
    "Brake 1 (D)": gpiozero.Button(17), # pull_up by default, connect other side of button to ground.
    "Brake 1 (R)": gpiozero.Button(27),
    "Brake 2 (D)": gpiozero.Button(22),
    "Brake 2 (R)": gpiozero.Button(23)
    #"Brake 3 (D)": gpiozero.Button(24),
    #"Brake 3 (R)": gpiozero.Button(25),
    #"Brake 4 (D)": gpiozero.Button(5),
    #"Brake 4 (R)": gpiozero.Button(6)
}

fans = gpiozero.OutputDevice(5)

# Output Pins
led_pins = {
    "LED 1": gpiozero.LED(12), # Green
    "LED 2": gpiozero.LED(13), # Yellow
    "LED 3": gpiozero.LED(19)  # Red
}

brake_control_pins = { # only 2 pins for ebrakes
    "Brake Control S1": gpiozero.OutputDevice(16),
    "Brake Control S2": gpiozero.OutputDevice(20)
}

vfd_pin = gpiozero.OutputDevice(26)

main_circuit_pins = {
    "Main Switch" : gpiozero.OutputDevice(14),
    "VFD Switch 2" : gpiozero.OutputDevice(2)
}
'''
def brake_check() -> bool:

    retract = retract_brakes()

    deploy = deploy_brakes()
    
    return retract and deploy
'''
def deploy_brakes() -> bool:

    brake_control_pins["Brake Control S1"].on()
    brake_control_pins["Brake Control S2"].on()
    time.sleep(0.5)
    if not brake_sensors["Brake 1 (R)"].is_active and not brake_sensors["Brake 2 (R)"].is_active:
        return True
    
    return False

def retract_brakes() -> bool:
    
    brake_control_pins["Brake Control S1"].off()
    brake_control_pins["Brake Control S2"].off()

    while not brake_sensors["Brake 1 (R)"].is_active and not brake_sensors["Brake 2 (R)"].is_active:
        time.sleep(0.5)
    
    return True

def main_power_on() -> None:
    main_circuit_pins["Main Switch"].on()
    main_circuit_pins["VFD Switch 2"].on()

def main_power_off() -> None:
    main_circuit_pins["Main Switch"].off()
    main_circuit_pins["VFD Switch 2"].off()

def LIM_run() -> None:
    vfd_pin.on()

def LIM_off() -> None:
    vfd_pin.off()

def fans_on() -> None: # relays work off inverted inputs
    fans.off()

def fans_off() -> None:
    fans.on()

def brakeLeftStatus() -> bool:
    if brake_sensors["Brake 1 (R)"].is_active:
        return False
    return True

def brakeRightStatus() -> bool:
    if brake_sensors["Brake 2 (R)"].is_active:
        return False
    return True